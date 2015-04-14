nvcc="nvcc"

if [ -e "/usr/local/cuda/bin/nvcc" ]; then
  nvcc="/usr/local/cuda/bin/nvcc"
fi

if [ -d "bin/" ]; then
  rm -rf bin
fi

if [ -d "images/" ]; then
  rm -rf images
fi

mkdir bin
mkdir images

echo "[0] Building CUDA C..."
$nvcc -O3 -arch=sm_35 -rdc=true -lcudadevrt -Xcompiler -fopenmp -lpng mandelbrot-naive.cu -o bin/mandelbrot-naive

echo "[0] Building OpenMP..."
gcc -Wno-write-strings -O3 -Wall -fopenmp -lpng mandelbrot-omp.cpp -o bin/mandelbrot-omp

echo "[1] Run CUDA C..."
./bin/mandelbrot-naive

echo "[1] Run OpenMP..."
./bin/mandelbrot-omp
