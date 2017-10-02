# Train_Sudoku

A) If you are here to download a dataset of train sudokus go to the folder dataset. There you can find the datasets having names in the following format: "dataset_grid-size_maximum-number-of-tests".  Each dataset file has the following properties:
  - each line consists of one game example
  - any example has the following form: 
  
        -> first, there are the values of n, m, k separated by commas  
        -> then, there are k pairs of numbers in the form (r, c) corresponding to the coordinates of the k stations
  - the examples are ordered by the value of k
  - for each value of k there are at most the maximm-number-of-tests many examples (as in the file name)
  - if the size of the board is not 9 by 9 then there are exactly the maximm-number-of-tests many examples for each k

B) If you are here to create a new dataset of train sudokus, then use  TS_generator.py (written in python 2.7), in the following way:
  - for creating one train sudoku example with a board of size n by m and k stations, use the function sudo_train_gen passing the tuple (n, m, k) as an argument
  - for creating a dataset file of sudoku train examples with board size n by m, and t many examples for each value of k between 2 and n*m use the function st_dataset passing n, m, and t as arguments

C) If you are here to use PycoSAT for solving train sudokus, plese start by insuring that you have the relevant packages installed:
  - pycosat
  - pandas
You can use encoding.py (written in python 2.7) in one of the following ways:
  - use the function solve_and_print with a game g as an argument to solve g and print both the completed and uncompleted board
  - call the function example_solve without any arguments to see the outputs for 4 examples

D) If you are here to generate plots picturing the dependency between the number of stations and the number of conflicts use table_TS.py (also written in python 2.7). For running this you need to install the following packages: os, sys, pycosat, time, and matplotlib. Also, make sure that encoding.py and the relevant dataset (named as in A) are in the same folder.

To generate the plot call graph_gen with n, m and the maximum number of tests as argument. 
