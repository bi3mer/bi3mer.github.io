+++
date = '2025-09-01T12:00:00+00:00'
draft = false
title = "Block Randomization Web Server in Go - Participant Assignment, Logging, & Static Serving"
+++

{{< youtube a21U3MzoPpc >}}

----

I live code a Go web server that uses block randomization to assign participants to different conditions in experiments. The server also handles logging and serving static files for the experiment interface.

Block randomization is a technique that ensures you get equal numbers of participants in each group throughout your study, which is important for getting valid results. Instead of pure random assignment, it assigns participants in blocks to keep the groups balanced.

Code & Resources:
GitHub Repository: https://github.com/bi3mer/go-log-study-server
Go Documentation: golang.org/doc/
