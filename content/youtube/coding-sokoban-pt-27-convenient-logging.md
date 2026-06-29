+++
date = '2025-08-15T12:00:00+00:00'
draft = false
title = "Coding Sokoban pt. 27: Convenient Logging"
+++

{{< youtube I_AWdfBew0s >}}

----

Part 27: Convenient Logging

Part 27 upgrades our logging system with modern C++ techniques! We eliminate the need for users to manually call std::format by implementing template parameter packing and perfect forwarding, creating a much more convenient logging experience.

Instead of log(std::format("Player at {}, {}", x, y)), users can now simply write log("Player at {}, {}", x, y).

- Project Repository: https://github.com/bi3mer/sokoban
- Series Playlist: https://www.youtube.com/watch?v=1qzPr5OpPOE&list=PLwaZncztKsRckZ0u3sKbwkZMtH1-ABkDR
