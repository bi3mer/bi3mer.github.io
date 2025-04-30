+++
date = '2025-04-30T11:16:56-04:00'
draft = true
title = 'Block Randomization'
+++

# Testing the Results

- brief study info
- brief intro to why c++ instead of python
- [JSON library](https://github.com/nlohmann/json/tree/develop)

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

```
distance: 7
mean: 6
random: 7
```