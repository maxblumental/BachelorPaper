import subprocess as sp
import shlex

#################################################
# To add a target, add its compilation line to
# the compile_strings list and the name of the
# executable to the exe list.
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
  config.write("plot \"{}-{}.log\" with lines\n".format(name, what))
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
    "/usr/local/cuda-6.5/bin/nvcc /export/users/mblument/BachelorPaper/mandelbrot-naive.cu -O3 -arch=sm_35 -rdc=true -lcudadevrt -Xcompiler -fopenmp -lpng -o cuda-c",
    ]
  compile_log = open("compile.log", "w")

  for c in compile_strings:
    compile_log.write("Compiling: "+c+"\n")
    compile_log.flush()
    sp.call(shlex.split(c), stdout=compile_log, stderr=compile_log)
  
  compile_log.close()

  #run section
  args = [2**i for i in range(5)]
  exe = [
    'cuda-c',
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

  #data processing: build it with gnuplot
  for name in exe:
    #measure build time
    get_log(name, 0)
    pconf = generate_plot_config(name, 0)
    sp.call(['gnuplot', pconf])
    sp.call(['rm', pconf])
    sp.call(['rm', name+'-time.log'])

    #measure build speed
    get_log(name, 1)
    pconf = generate_plot_config(name, 1)
    sp.call(['gnuplot', pconf])
    sp.call(['rm', pconf])
    sp.call(['rm', name+'-speed.log'])

  for ex in exe:
    sp.call(['rm', ex])
