# BachelorPaper

Here you can find following programs, computing
mandelbrot set:
 
 - mandelbrot-dyn.cu - Mariani-Silver
 algorithm in CUDA C;

 - mandelbrot-naive.cu - naive escape
 time algorithm in CUDA C;

 - mandelbrot-omp.cpp - naive escape
 time algorithm in OpenMP C++;

 - mandelbrot-naive-acc.cpp - naive escape
 time algorithm in OpenACC C++.

mandelbrot-dyn.cu was added just to
illustrate an effective way of using
dynamic parallelism.
Here we basically launch and measure
performance of naive version.
