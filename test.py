import subprocess as sp
import shlex

#################################################
# To add a target, add its compilation line to
# the compile_strings list and the name of the
# executable to the exe list. If there are more
# than three executables, add colors.
#################################################

def generate_plot_config(name, mode):
  fullname = name
  what=''
  units=''
  if mode == 0:
    fullname = fullname + '-time'
    what='time'
    units='sec'
  elif mode == 1:
    fullname = fullname + '-speed'
    what='speed'
    units='Mpix/sec'
  config = open(name+".gp", 'w')
  config.write("set term png\n")
  config.write("set output \"{}.png\"\n".format(fullname))
  config.write("set grid\n")
  config.write("set xlabel \"resolution (x*x Mpix)\"\n")
  config.write("set ylabel \"{} ({})\"\n".format(what, units))
  config.write("set title \"Mandelbrot set build {} for {}\"\n".format(what, name))
  config.write("plot \"{}-{}.log\" with lines title \"{}\"\n".format(name, what, name))
  config.close()
  return name+'.gp'

def generate_plot_config_comparison(names, mode):
  fullname = 'comparison-of'
  what=''
  units=''
  if mode == 0:
    fullname = fullname + '-time'
    what='time'
    units='sec'
  elif mode == 1:
    fullname = fullname + '-speed'
    what='speed'
    units='Mpix/sec'
  config = open(name+".gp", 'w')
  config.write("set term png\n")
  config.write("set output \"{}.png\"\n".format(fullname))
  config.write("set grid\n")
  config.write("set xlabel \"resolution (x*x Mpix)\"\n")
  config.write("set ylabel \"{} ({})\"\n".format(what, units))
  config.write("set title \"Mandelbrot set build {} comparison\"\n".format(what))
  plot_str = "plot "
  colors = ["red", "green", "blue", "magenta"]
  for nm in names:
    plot_str += "\""+nm+"-"+what+".log\""+" with lines title \""+nm+"\" linecolor rgb \""+ colors[names.index(nm)] +"\", "
  plot_str = plot_str[:len(plot_str) - 2]
  config.write(plot_str)
  config.close()
  return name+'.gp'

def get_log(name, mode):
  what = ''
  if mode == 0:
    what = 'time'
  else:
    what = 'speed'
  source = open(name+'.log', 'r')
  dest = open(name+'-{}.log'.format(what), 'w')

  for line in source:
    lst = line.split()
    dest.write(lst[0]+' '+lst[1+mode]+'\n')

  source.close()
  dest.close()



if __name__ == '__main__':
  #compilation section
  compile_strings = [
    "/usr/local/cuda-6.5/bin/nvcc /export/users/mblument/BachelorPaper/source/mandelbrot-dynamic.cu -O3 -arch=sm_35 -rdc=true -lcudadevrt -Xcompiler -fopenmp -lpng -o dynamic",
    "/usr/local/cuda-6.5/bin/nvcc /export/users/mblument/BachelorPaper/source/mandelbrot-ignore.cu -O3 -arch=sm_35 -rdc=true -lcudadevrt -Xcompiler -fopenmp -lpng -o ignore",
    "/usr/local/cuda-6.5/bin/nvcc /export/users/mblument/BachelorPaper/source/mandelbrot-predictor.cu -O3 -arch=sm_35 -rdc=true -lcudadevrt -Xcompiler -fopenmp -lpng -o predictor",
    "/usr/local/cuda-6.5/bin/nvcc /export/users/mblument/BachelorPaper/source/mandelbrot-optimized.cu -O3 -arch=sm_35 -rdc=true -lcudadevrt -Xcompiler -fopenmp -lpng -o optimized",
  ]
  compile_log = open("compile.log", "w")

  for c in compile_strings:
    compile_log.write("Compiling: "+c+"\n")
    compile_log.flush()
    sp.call(shlex.split(c), stdout=compile_log, stderr=compile_log)
  
  compile_log.close()

  #run section
  args = [i for i in range(1,17)]
  exe = [
    'dynamic',
    'ignore',
    'predictor',
    'optimized',
  ]

  run_logs = [open(ex+".log", "w") for ex in exe]

  for i in range(len(exe)):
    rl = run_logs[i]
    for arg in args:
      arg_lst = ['./'+exe[i], str(arg)]
      print('{0} builds {1}x{1} Mpix'.format(exe[i], arg))
      rl.write(str(arg)+'\t')
      rl.flush()
      sp.call(arg_lst, stdout=rl)
    rl.close()

  #data processing: prepare tables for gnuplot
  for name in exe:
    get_log(name, 0)
    get_log(name, 1)
  
  #plot comparison graphs
  pconf = generate_plot_config_comparison(exe, 0)
  sp.call(['gnuplot', pconf])
  sp.call(['rm', pconf])
 
  pconf = generate_plot_config_comparison(exe, 1)
  sp.call(['gnuplot', pconf])
  sp.call(['rm', pconf])
  
  for ex in exe:
    sp.call(['rm', ex])
    sp.call(['rm', ex+'-speed.log'])
    sp.call(['rm', ex+'-time.log'])
