+++
date = '2025-10-07T11:33:19-04:00'
draft = false
title = 'Hot Reloading Constants: Tweak Values Without Recompiling'
+++

{{< youtube QAgNCyHa5ic >}}

----

Tired of the compile-restart-test loop when tuning parameters? In this video, I show you a clever technique for hot reloading hardcoded constants. By wrapping values in a TWEAK() macro, you can edit numbers directly in your source code and see them update in real-time while your program is running—no recompiling or restarting needed.

The trick uses `__FILE__` and `__LINE__` to track each parameter, parse the source file when it changes, and update values on the fly. I demonstrate this using a Raylib bouncing ball example, showing how you can tweak physics values, colors, and other parameters on the fly. It's perfect for quickly finding that sweet spot when tweaking game physics, graphics parameters, or any values that need experimentation. And in release builds, the macro compiles away to zero overhead.

- Code: [https://gist.github.com/bi3mer/462de89fe093de5660100b9ae2431eca](https://gist.github.com/bi3mer/462de89fe093de5660100b9ae2431eca)
- Raylib bouncing ball example: [https://www.raylib.com/examples/shapes/loader.html?name=shapes_bouncing_ball](https://www.raylib.com/examples/shapes/loader.html?name=shapes_bouncing_ball)
- Notch using hot reloading in Minecraft: [https://www.youtube.com/watch?v=BES9EKK4Aw4](https://www.youtube.com/watch?v=BES9EKK4Aw4)
- Wookash podcast with Eskil Steenberg: [https://www.youtube.com/watch?v=zqHdvT-vjA0](https://www.youtube.com/watch?v=zqHdvT-vjA0)
- Original blog post: [https://blog.voxagon.se/2018/03/13/hot-reloading-hardcoded-parameters.html](https://blog.voxagon.se/2018/03/13/hot-reloading-hardcoded-parameters.html)


**UPDATE 2025/10/21:** See [adjust.h](https://github.com/bi3mer/adjust.h/blob/main/adjust.h) for an improvement to the approach.