# BachelorPaper

In the source/ directory you can find following
programs in CUDA C, computing mandelbrot set:
 
 - mandelbrot-optimized.cu - Mariani-Silver
 algorithm;

 - mandelbrot-dynamic.cu - naive escape time
 algorithm with dynamic parallelism;

 - mandelbrot-ignore.cpp - naive escape
 time algorithm ignoring simd pragma;

mandelbrot-optimized.cu was added just to
illustrate an effective way of using
dynamic parallelism.
Here we basically launch and measure
performance of naive versions.
