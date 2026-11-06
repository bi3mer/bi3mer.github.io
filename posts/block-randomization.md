+++
date = '2025-04-30T11:16:56-04:00'
draft = false
title = 'Block Randomization'
+++

Last month I ran an online study with 250 participants. There were 5 possible conditions, and assignment was random. You would expect there to be ~50 participants per condition. In my case, though, one condition had 36 participants, creating an unideal skew in the dataset in terms of participants per condition. The problem was random assignment.

What I should have used instead was [block randomization.](https://www.statsdirect.com/help/randomization/block.htm)

# Block Randomization

Block randomization is super simple to implement, but it comes with a major downside when compared to random assignment. Random assignment is great when you're running an online study because it does not require a server. Every client can call select a random condition on its own. Block randomization needs a server.

The way block randomization works is that it has a list of the possible conditions. Say, for example, we have three conditions.

```python
conditions = ["condition 1", "condition 2", "condition 3"]
```

Block randomization starts by shuffling that array. Then, when the first request for a condition arrives, it sends the first element of that array. Once the next request comes, it sends the second. This continues until the number of requests is greater than the number of conditions in the array.[^conditions] Then, the array of conditions is shuffled, and the index is reset to 0.

# Implementing Block Randomization

Because block randomization requires a server, I decided to use [Go,](https://go.dev/) a language that I have wanted to try for a couple years now. The implementation starts with a `Block`.

```Go
type Block struct {
	index int
	rand  *rand.Rand
	mu    sync.Mutex
	block []string
}
```

The structure is pretty simple. It has an index for the conditions array, a random number generator, a [mutex](https://en.wikipedia.org/wiki/Lock_(computer_science)), and the block of conditions. The first thing we need to do is initialize the block.


```go
func blockNew(sizeMultiple int, conditions []string) *Block {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	block := make([]string, len(conditions)*sizeMultiple)
	index := 0
	for _, c := range conditions {
		for range sizeMultiple {
			block[index] = c
			index++
		}
	}

	r.Shuffle(len(block), func(i, j int) {
		block[i], block[j] = block[j], block[i]
	})

	b := Block{
		index: 0,
		rand:  r,
		mu:    sync.Mutex{},
		block: block,
	}

	return &b
}
```

The block takes in as arguments the multiplier as mentioned in the footnote, and the list of conditions. From there, it creates an array of conditions based on the size multiplier, which is called the `block`. The list is shuffled, and then the `block` struct is initialized with a mutex. The mutex is necessary when we get a condition from the `block`.[^implementation]

```go
func blockGetCondition(block *Block) *string {
	block.mu.Lock()
	defer block.mu.Unlock()

	if block.index >= len(block.block) {
		block.index = 0
		block.rand.Shuffle(len(block.block), func(i, j int) {
			block.block[i], block.block[j] = block.block[j], block.block[i]
		})
	}

	condition := &block.block[block.index]
	block.index++

	return condition
}
```

Getting a condition follows the exact process already described in the above section, but there is the additional element of a mutex. Go's [http server](https://gobyexample.com/http-servers) is threaded by default with [goroutines](https://go.dev/tour/concurrency/1). So, before we interact with the `block` in a way that will affect its state, we need to lock the mutex to avoid a [race condition](https://en.wikipedia.org/wiki/Race_condition) that results in a faulty block randomization implementation.

# Testing the Implementation

As part of my work, I needed a server that stored logs, and I added the block condition code as well.[^github] Before running the code with a real study, though, I wrote a quick test. I set up the block code to work with three conditions: random, mean, and distance. Then, I wrote a go script to request 200 conditions all at about the same time. The script is below.[^changes]

```go
var M = sync.Mutex{}

func getCondition(counts map[string]int) {
	resp, err := http.Post("http://127.0.0.1:8080/condition", "text/plain", nil)
	if err != nil {
		fmt.Println(err)
		M.Lock()
		counts["error"]++
		M.Unlock()
		return
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
		M.Lock()
		counts["error"]++
		M.Unlock()
		return
	}

	M.Lock()
	counts[string(body)]++
	M.Unlock()
}

func main() {
	counts := map[string]int{}
	counts["random"] = 0
	counts["mean"] = 0
	counts["distance"] = 0
	counts["error"] = 0

	var wg sync.WaitGroup
	for range 200 {
		wg.Add(1)

		go func() {
			defer wg.Done()
			time.Sleep(time.Duration(rand.Intn(10)) * time.Millisecond)
			getCondition(counts)
		}()
	}

	wg.Wait()

	println("random:   ", counts["random"])
	println("mean:     ", counts["mean"])
	println("distance: ", counts["distance"])
	println("error:    ", counts["error"])
}
```

I ran the following test script a bunch of times with the server running, and I got output like:

```
random:    66
mean:      67
distance:  67
error:     0
```

# Test with a Real Study

I recently helped run a study with [Recformer](https://bi3mer.github.io/recformer/index.html?default=true) where [paths were logged](https://bi3mer.github.io/posts/logging-for-recformer/) to a server using the golang server that I wrote. As part of it, I added a field to the json logs which was the player's assigned condition, even though condition was meaningless for the study.

The study had 20 participants. So, it wasn't a stress test on the server, but it was a real-world test to make sure that the block randomization code above worked outside of an easy test bed when running on a server, rather than my computer.

I pulled the results down after the study, and I wrote a quick c++ program to get each player's assigned condition, and then count how many players there were per condition. I used c++ not because it was the right choice. (It was definitley not the right choice.) Writing the code in Python would have been a faster and easier activity for me. I went with c++ because (1) I've never used JSON with c++ code before and (2) I wanted to.

To parse the json, I used the first [library](https://github.com/nlohmann/json/tree/develop) I found on GitHub that had a single header file, and then I just copied the file into my local directory. Then I wrote the following c++ code:

```c++
#include <fstream>
#include <iostream>
#include <filesystem>
#include <unordered_map>
#include <string>

#include "json.hpp"

int main() {
    std::unordered_map<std::string, std::string> player_to_condition;
    for (const auto& file : std::filesystem::directory_iterator("logs")) {
        if (!std::filesystem::is_regular_file(file)) {
            continue;
        }

        std::ifstream f(file.path());
        nlohmann::json data = nlohmann::json::parse(f);

        if (player_to_condition.find(data["id"]) == player_to_condition.end()) {
            player_to_condition[data["id"]] = data["condition"];
        }
    }

    std::unordered_map<std::string, int> counts;
    for (const auto& [_, condition] : player_to_condition) {
        if (counts.find(condition) != counts.end()) {
            ++counts[condition];
        } else {
            counts[condition] = 1;
        }
    }

    for (const auto& [condition, count] : counts) {
        std::cout << condition << ": " << count << std::endl;
    }

    return 0;
}
```

The output was:

```
distance: 7
mean: 6
random: 7
```

So, the above block randomization code worked in local testing and in small real world test, and I will be using it in my next two user studies that will have more logs logged and more conditions assigned. Though, I will make some changes, like not [hardcoding the conditions](https://github.com/bi3mer/go-log-study-server/blob/main/src/server.go#L19) and a few other improvements.

**UPDATE 2025/10/21:** I've since made a [YouTube video,](https://www.youtube.com/watch?v=a21U3MzoPpc) showing how the whole thing can be implemented from scratch.



[^conditions]: Block randomization is sometimes implemented with a multiplier. The multiplier, an integer that is greater than or equal to `1`, increases the size of the array of conditions, and adds duplicates. So, a multiplier of `2` would result in the conditions array having two instances of each condition.

[^implementation]: A better implementation would use a `uint` for the size multiplier, and it would make sure that the conditions array was not empty.

[^github]: Code is available on [GitHub.](https://github.com/bi3mer/go-log-study-server/tree/main)

[^changes]: Looking at the script now, I would change the way I used the mutex to just lock it at the top of the function, and then call defer unlock on the line below.