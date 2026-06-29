+++
date = '2025-08-20T12:00:00+00:00'
draft = false
title = "Coding Sokoban pt. 29: Ring Buffer (2)"
+++

{{< youtube jwV1VI7t0VU >}}

----

Part 29: Ring Buffer (2)

Part 29 completes our ring buffer implementation and puts it head-to-head with our pooled linked list in speed tests. The results are surprising - ring buffer wins on cold starts, but our object-pooled linked list actually performs better when everything is pre-initialized.

UPDATE: The reason why the linked list was faster than the ring buffer was that I didn't have the linked list behave circularly. Instead, it appended without ever size-checking. The README in the GitHub repo (below) has the correct results, and the ring buffer is faster. You'll also notice that the results are slower when I was recording versus the updated results when I was not recording.

- Project Repository: https://github.com/bi3mer/sokoban
- Series Playlist: https://www.youtube.com/watch?v=1qzPr5OpPOE&list=PLwaZncztKsRckZ0u3sKbwkZMtH1-ABkDR
