# In this routine, for given values of n and m, the program generates for each k
# 100 games, find the average number of conflicts required in solving those games
# and returns a graph of the values of k versus the number of conflicts.

# The following lines of code are from https://stackoverflow.com/questions/
# 4675728/redirect-stdout-to-a-file-in-python/22434262 and have the only purpose
# of redirecting the output given by pycosat in a folder, from where it can be
# later extracted.

import os
import sys
from contextlib import contextmanager

def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd

@contextmanager
def stdout_redirected(to=os.devnull, stdout=None):
    if stdout is None:
       stdout = sys.stdout

    stdout_fd = fileno(stdout)
    # copy stdout_fd before it is overwritten
    #NOTE: `copied` is inheritable on Windows when duplicating a standard stream
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied: 
        stdout.flush()  # flush library buffers that dup2 knows nothing about
        try:
            os.dup2(fileno(to), stdout_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(to, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
        try:
            yield stdout # allow code to be run with the redirected stdout
        finally:
            # restore stdout to its previous value
            #NOTE: dup2 makes stdout_fd inheritable unconditionally
            stdout.flush()
            os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied

# End of imported subroutine

import pycosat
import time
import encoding as ed
# import TS_generator as gen

def extract_stats (game):
  '''This extracts the number of conflicts and the number of seconds'''
  cnf = ed.cnf_encoding(game)
  
  # Next 2 lines also taken from reference given in lines 5 and 6
  stdout_fd = sys.stdout.fileno()
  with open('output.txt', 'w') as f, stdout_redirected(f):
    start_time =time.time()
    sol = pycosat.solve(cnf, verbose = 1)
    end_time= time.time()
    total_time = end_time - start_time
  
  # Now we extract the number of conflicts from the output file
  with open('output.txt', 'r') as f:
    f.seek(-200, 2)
    str_from_f = f.readlines()[-5]
    str_from_f = str_from_f[2:]
    
    nice_str_from_f = ''
    space_before = True
    for char in str_from_f:
      if char == ' ':
        space_before = True
      else:
        if space_before:
          nice_str_from_f = nice_str_from_f + ', ' + char
        else:
          nice_str_from_f = nice_str_from_f + char
        space_before = False
    nice_str_from_f = nice_str_from_f[2:-3]
    
    no_from_f = map(float, nice_str_from_f.split(','))
    conflicts = no_from_f[-5]
  
  k = game[2]
  return (conflicts, total_time)

def interpret_line(line):
  '''Given an example of a train sudoku as a string, it transforms it in a list
  with n, m, k, and the k tuples representing the stations'''
  
  line = line.translate(None, '(')
  line = line.translate(None, ')')
  line = map (int, line.split(','))
  
  game = line[0:3]
  k = game[2]
  for i in range(k):
    game.append((line[3 + 2*i], line[3 + 2*i +1]))
  
  return game

def find_average_no_conflicts (examples):
  '''For the given list of examples it returns the average number of conflicts
  and the average time spend for solving the example'''
  conf_sum = 0
  time_sum = 0
  no_tests = len(examples)
  for game in examples:
    stats = extract_stats(game)
    conf_sum = conf_sum + stats[0]
    time_sum = time_sum + stats[1]
  
  return (conf_sum/no_tests, time_sum/no_tests)

import matplotlib.pyplot as plt

def graph_gen (n, m, no_tests):
  '''Constructs the plots for the average of conflicts and average number of 
  seconds for different values of k'''
  
  y = []
  
  name = 'dataset_' + str(n) + 'by' + str(m) + '_' + str(no_tests) +'.txt'
  with open(name, 'r') as f:
    cur_k = 2
    examples = []
    for line in f:
      game = interpret_line(line)
      new_k = game[2]
      
      if cur_k == new_k:
        examples.append(game)
      else:
        cur_k = new_k
        y.append(find_average_no_conflicts(examples))
        print (cur_k, y[-1])
        examples = [game]
    y.append(find_average_no_conflicts(examples))
  
  y_conf = [val[0] for val in y]
  y_conf_max = max(y_conf)
  y_conf_index = y_conf.index(y_conf_max) + 2
  
  y_time = [val[1] for val in y]
  y_time_max = max(y_time)
  y_time_index = y_time.index(y_time_max) + 2
  
  plt.plot(range(2, n*m + 1), y_conf, 'r')
  plt.plot(y_conf_index, y_conf_max, 'ro')
  max_text = '(' + str(y_conf_index) + ', ' +  str(y_conf_max) + ')'
  plt.annotate(max_text, xy = (y_conf_index, y_conf_max))
  plt.xlabel('Value of k')
  plt.ylabel('Average number of conflicts')
  #c = 'for a grid of ' + str(n) + ' by ' + str(m)
  #plt.title('The average number of conflicts for different number of stations' + c)
  plt.savefig('conf_' + str(n) + 'by' + str(m) + '_' + str(no_tests) + 'tests')
  plt.clf()
  
  plt.plot(range(2, n*m + 1), y_time, 'b')
  plt.plot(y_time_index, y_time_max, 'bo')
  max_text = '(' + str(y_time_index) + ', ' +  str("%.4f" % y_time_max) + ')'
  plt.text(y_time_index * 1.01, y_time_max, max_text)
  plt.xlabel('Value of k')
  plt.ylabel('Average time (s)')
  #plt.title('The average solving time for different number of stations' + c)
  plt.savefig('time_' + str(n) + 'by' + str(m) + '_' + str(no_tests) + 'tests')
  plt.clf()
  
  return y
