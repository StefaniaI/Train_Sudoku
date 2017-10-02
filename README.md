# Train_Sudoku

A) If you are here to download a dataset of train sudokus go to the folder dataset. There you can find the datasets having names in the following format: "dataset_grid-size_maximum-number-of-tests".  Each dataset file has the following properties:
  - each line consists of one game example
  - any example has the following form: 
        -> first, there are the values of n, m, k separated by commas  
        -> then, there are k pairs of numbers in the form (r, c) corresponding to the coordinates of the k stations
  - the examples are ordered by the value of k
  - for each value of k there are at most the maximm-number-of-tests many examples (as in the file name)
  - if the size of the board is not 9 by 9 then there are exactly the maximm-number-of-tests many examples for each k

