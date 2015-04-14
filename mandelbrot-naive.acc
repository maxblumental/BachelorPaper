#include <assert.h>
#include <png.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/** gets the color, given the dwell */
void dwell_color(int *r, int *g, int *b, int dwell);

/** save the dwell into a PNG file 
		@remarks: code to save PNG file taken from here 
		  (error handling is removed):
		http://www.labbookpages.co.uk/software/imgProc/libPNG.html
 */
void save_image(const char *filename, int *dwells, int w, int h) {
	png_bytep row;
	
	FILE *fp = fopen(filename, "wb");
	png_structp png_ptr = png_create_write_struct(PNG_LIBPNG_VER_STRING, 0, 0, 0);
	png_infop info_ptr = png_create_info_struct(png_ptr);
	// exception handling
	setjmp(png_jmpbuf(png_ptr));
	png_init_io(png_ptr, fp);
	// write header (8 bit colour depth)
	png_set_IHDR(png_ptr, info_ptr, w, h,
							 8, PNG_COLOR_TYPE_RGB, PNG_INTERLACE_NONE,
							 PNG_COMPRESSION_TYPE_BASE, PNG_FILTER_TYPE_BASE);
	// set title
	png_text title_text;
	title_text.compression = PNG_TEXT_COMPRESSION_NONE;
	title_text.key = "Title";
	title_text.text = "Mandelbrot set, per-pixel";
	png_set_text(png_ptr, info_ptr, &title_text, 1);
	png_write_info(png_ptr, info_ptr);

	// write image data
	row = (png_bytep) malloc(3 * w * sizeof(png_byte));
	for (int y = 0; y < h; y++) {
		for (int x = 0; x < w; x++) {
			int r, g, b;
			dwell_color(&r, &g, &b, dwells[y * w + x]);
			row[3 * x + 0] = (png_byte)r;
			row[3 * x + 1] = (png_byte)g;
			row[3 * x + 2] = (png_byte)b;
		}
		png_write_row(png_ptr, row);
	}
	png_write_end(png_ptr, NULL);

  fclose(fp);
  png_free_data(png_ptr, info_ptr, PNG_FREE_ALL, -1);
  png_destroy_write_struct(&png_ptr, (png_infopp)NULL);
  free(row);
}  // save_image


/** a simple complex type */
struct complex {
	complex(float re, float im = 0) {
		this->re = re;
		this->im = im;
	}
	/** real and imaginary part */
	float re, im;
}; // struct complex

// operator overloads for complex numbers
inline complex operator+
(const complex &a, const complex &b) {
	return complex(a.re + b.re, a.im + b.im);
}
inline complex operator-
(const complex &a) { return complex(-a.re, -a.im); }
inline complex operator-
(const complex &a, const complex &b) {
	return complex(a.re - b.re, a.im - b.im);
}
inline complex operator*
(const complex &a, const complex &b) {
	return complex(a.re * b.re - a.im * b.im, a.im * b.re + a.re * b.im);
}
inline float abs2(const complex &a) {
	return a.re * a.re + a.im * a.im;
}
inline complex operator/
(const complex &a, const complex &b) {
	float invabs2 = 1 / abs2(b);
	return complex((a.re * b.re + a.im * b.im) * invabs2,
								 (a.im * b.re - b.im * a.re) * invabs2);
}  // operator/

#define MAX_DWELL 512

/** gets the color, given the dwell (on host) */
#define CUT_DWELL (MAX_DWELL / 4)
void dwell_color(int *r, int *g, int *b, int dwell) {
	// black for the Mandelbrot set
	if(dwell >= MAX_DWELL) {
		*r = *g = *b = 0;
	} else {
		// cut at zero
		if(dwell < 0)
			dwell = 0;
		if(dwell <= CUT_DWELL) {
			// from black to blue the first half
			*r = *g = 0;
			*b = 128 + dwell * 127 / (CUT_DWELL);
		} else {
			// from blue to white for the second half
			*b = 255;
			*r = *g = (dwell - CUT_DWELL) * 255 / (MAX_DWELL - CUT_DWELL);
		}
	}
}  // dwell_color

/** data size */
#define H (16 * 1024)
#define W (16 * 1024)
#define IMAGE_PATH "./images/mandelbrot-omp.png"

#pragma omp declare simd simdlen(16)
int mandelbrot(complex c)
{
  // Computes number of iterations(count variable)
  // that it takes for parameter c to be known to
  // be outside mandelbrot set
  int count = 1;
  complex z = c;  
  
  while ((abs2(z) < 4.0f) && (count < MAX_DWELL))
  {
      z = z * z + c;
      count++;
  }
  return count;
}

int main()
{
  //specify corner complex numbers
  //derive max_image and max_real from them
  int w = W, h = H;
  size_t dwell_sz = w * h * sizeof(int);
  int *dwells = (int*)malloc(dwell_sz);
  complex lb = complex(-1.5, -1),
          rt = complex(0.5, 1);
  
  double t1 = omp_get_wtime();

  #pragma acc parallel loop
  for (int y = 0; y < H; ++y)
  {
    float c_im = lb.im + (H-y)*(rt.im - lb.im)/H;
    
    #pragma acc parallel loop vector(32)
    for (int x = 0; x < W; ++x)
    {
      float c_re = lb.re + x*(rt.re - lb.re)/W;
      complex in_val = complex(c_re, c_im);
      dwells[y*W+x] = mandelbrot(in_val);
    }
  }

  double t2 = omp_get_wtime(),
         gpu_time = t2 - t1;

  // print performance summary
  printf("Mandelbrot set computed in %.3lf s, at %.3lf Mpix/s\n", gpu_time, 
  h * w * 1e-6 / gpu_time);
  // save the image to PNG file
  save_image(IMAGE_PATH, dwells, w, h);
  // free allocated memory
  free(dwells);

  return 0;
}
