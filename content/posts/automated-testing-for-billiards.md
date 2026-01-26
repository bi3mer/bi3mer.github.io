+++
date = '2026-01-26T09:37:04-05:00'
draft = false
title = 'Automated Testing for Billiards'
+++

{{< youtube 4PDm8JZTNhw >}}

----

I'm working on a game, and I want to ship that game bug-free. The best way to ensure that is to test, test, and test.

Game testing—sometimes called QA or quality assurance—is simple in theory: play the game, try to break it, fix what breaks. The problem is that _you_ built the thing. You play it the way it's meant to be played. Your players won't.

That's why companies have whole departments dedicated to testing their games to find bugs and document exactly how to trigger them. If you're like me, though, hiring a team of people to break my game is a bit much. So, if testing the game you made yourself is fraught and hiring other people is too much, what should you do?

Automated testing.

Tyler Glaiel, a programmer behind several games including the upcoming game *Mewgenics* has recently been discussing on Twitter how he's testing *Mewgenics*: "the fuzz tester is like 100 lines of code. remove the framerate limit, replace "Player Brain" with the enemy AI brain instead (or the "target randomly" brain, some of the time). save the random seed before each test. if crash, save the random seed to a file for inspection later."

For some games, this is too simple. One really nice example of something more complex is how they did automated testing with bots for *Division 2*, which was covered by *AI and Games* and the link to their video is below. For the game that I'm making, though, something simple is perfect.

Just to repeat Tyler's idea, what I'm going to do is make a simple Python script, and it is going to run an instance of the game I'm working on. Before we get to how to modify the game, let's first talk about the Python script.

```python
def update_progress(progress, message=None):
    """
    modifed from: https://stackoverflow.com/questions/3160699/python-progress-bar
    NOTE: tqdm is better but avoiding dependencies for pypy
    """
    barLength = 20  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)

    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    elif progress < 0:
        progress = 0
        status = "Halt...\r\n"
    elif progress >= 1:
        progress = 1
        status = "Done\r\n"

    block = int(round(barLength * progress))

    if message != None:
        text = f"\rPercent [{'#' * block + '-' * (barLength - block)}] {round(progress * 100, 2)}% {status} :: {message}"
    else:
        text = f"\rPercent [{'#' * block + '-' * (barLength - block)}] {round(progress * 100, 2)}% {status}"

    sys.stdout.write(text)
    sys.stdout.flush()
```

The first part of the code is dedicated to this `update_progress` function, but it isn't relevant to the topic, so let's move on.

```python
if __name__ == "__main__":
    main()
```

This next part is where the "magic" happens. The first thing to do is to handle the entry point of the script. For a script this simple, it is a bit unnecessary, but it feels like best practice, so that's why it is there.

```python
def main():
	res = subprocess.run(["./r.sh", "fuzz", "--no-run"])
	if res.returncode != 0:
		print(f"Error running build script: {res.returncode}")
		sys.exit(1)

	#...
```

The next part of the script goes into the `main` function and starts a subprocess using a shell script called `r.sh`. This script is a helper script for building my game, and you can see that there is a special flag "fuzz". We'll come back to this. Once the subprocess is complete, we check the return code and if it is not zero that means compilation failed and the fuzz test shouldn't be run.

```python
random.seed(time.time())

with open(os.path.join("..", "fuzz_results.csv"), "w") as f:
	# ...
```

Assuming successful compilation, we seed Python's random number generator with the current time. This guarantees every run will produce different seeds. After, a file is opened to store the results in.

```python
for level_name in os.listdir(os.path.join("..", "levels")):
	for i in range(NUM_RUNS):
		#...
```

Now we get to something game specific. This first line lists every file in a directory called "levels," and is where I store all the levels in my game. That takes us to the second `for` loop, and this is where we get to the real value of automated testing. In the script, I have `NUM_RUNS` set to $10,000$. Meaning, the level will be tested ten thousand times—way more than you could ever do by hand.

```python
current_seed = random.randint(0, 4_294_967_294)
update_progress(i / NUM_RUNS, f"Processing {current_seed} {level_name}")

res = subprocess.run(
	[exec_path, str(current_seed), level_name],
	stdout=subprocess.DEVNULL,
	stderr=subprocess.DEVNULL,
)

f.write(f"{level_name}|{current_seed}|{res.returncode}\n")
f.flush()
```

Here is the real code for testing. First, we get a random seed. The large number there is $2^{32} - 2$, and this is to match the range of `srand` in C. Then we update the progress bar for a visual indication that something is happening. After, we start another subprocess where `exec_path` is a path to the executable that was compiled at the start of the program. We pass as command line arguments the seed and the level name that we are testing. Then, you'll notice that `stdout` and `stderr` are forwarded to `DEVNULL` and this is to suppress the output. I'm doing this because the output really isn't important, just the results. Finally, I output the results to a csv file, where I'm using the return code to indicate the result of running the game with the given level and seed.

And that takes us to the game side of things. Now, I'm going to show you two different versions of building with my script `r.sh`. This first one is when I run it with no command line arguments, and you can see the game starts with a GUI. Now, this is when I run it with `fuzz`, and you can see that the GUI is gone. The way this is accomplished in the code is by conditionally compiling the code in main.c with a preprocessor flag set during the build process:

```c
#ifdef FUZZ_BUILD

// Code for fuzz testing

#else

// Code for regular game

#endif
```

Now a reasonable question you may have is: Why do we care about the GUI? The answer is speed. If I'm going to run a level ten thousand times, and the graphics aren't important, then I shouldn't waste compute cycles on graphics.

```c
int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Usage: exe {SEED :: U32} {LEVEL_NAME :: STRING}\n");
        return 0;
    }

	// ...
}

```

The fuzz build code starts by checking if the required arguments are present. If not, it prints an error and returns a 0. As a note, returning a 0 typically indicates no error, so this decision by me is not best practice. However, I am using the return code for a very specific purpose where an exception will cause 1 to be returned. If the agent wins, 2 is returned. If they lose, 3 is returned. If the game is incomplete by the end of the simulation, 4 is returned.

```c
u16 iterations = 0;
while (sm_data.state == SM_PLAYING &&
	   sm_data.play_data.state == PLAY_STATE_PLAYER_MOVE)
{
	sm_data.play_data.state = PLAY_STATE_SIMULATING;
	table_random_impulse_update(&sm_data.table);

	while (sm_data.play_data.state == PLAY_STATE_SIMULATING)
	{
		sm_update(&sm_data, 0.016);
	}

	++iterations;
	if (iterations == 1000)
	{
		return 4;
	}
}

return sm_data.play_data.state == PLAY_STATE_WON ? 2 : 3;
```

The next bit of code is about initializing the game which we'll skip, but I do want to note that the command line arguments are used to seed the game and load the correct level file. Further you'll see in the code on the screen the use of `sm_data`, and this represents the data that is part of the game's state machine.

```c
void table_random_impulse_update(Table *t)
{
    Ball *b;
    for (u8 i = 0; i < MAX_BALLS; ++i)
    {
        b = &t->balls[i];
        if (b->color == COLOR_WHITE)
        {
            const double angle = f_rand_d(0, F_PI);
            b->velocity.x = cos(angle) * IMPULSE_MULTIPLER;
            b->velocity.y = sin(angle) * IMPULSE_MULTIPLER;
        }
    }
}
```

Running the game is pretty simple. In the first part, we have our agent do something, which in this case is to randomly set the impulse of every ball in the simulation that the player can interact with. Then, we run the game with a fixed delta time, which is hardcoded to $0.016$ or one over sixty, for sixty frames per second. Then, the last part of the loop is to make sure that the number of iterations hasn't exceeded 1000. If so, we stop the simulation because the random agent isn't getting anything done, but, more importantly, the game isn't crashing.

```
============================================================
OVERALL STATISTICS
============================================================
Total games: 30000

Won           1889 (  6.3%)
Lost         28111 ( 93.7%)

============================================================
PER-LEVEL STATISTICS
============================================================

lvl_1 (Total: 10000)
----------------------------------------
  Won           1397 ( 14.0%)
  Lost          8603 ( 86.0%)
  Inconclusive     0 (  0.0%)
  Crash            0 (  0.0%)

try (Total: 10000)
----------------------------------------
  Won            452 (  4.5%)
  Lost          9548 ( 95.5%)
  Inconclusive     0 (  0.0%)
  Crash            0 (  0.0%)

two_balls (Total: 10000)
----------------------------------------
  Won             40 (  0.4%)
  Lost          9960 ( 99.6%)
  Inconclusive     0 (  0.0%)
  Crash            0 (  0.0%)

============================================================
```

The last step is to analyze the results. The script to do so is neither interesting nor important, so let's just see what we get. Thirty thousand games, zero crashes. That's the kind of confidence you can't get from manual testing. And the whole thing—Python script, fuzz build flag, random agent—took an afternoon to set up.

Anyways, that's all for this video. If you liked it, please consider liking and subscribing. If you didn't, let me know why in the comments below. See you in the next one!


____
- Tyler Glaiel Twitter post on fuzzer: https://x.com/TylerGlaiel/status/2011159126311612661
- Automated testing for *Division 2*: https://www.youtube.com/watch?v=JpQd1Y7gYug

