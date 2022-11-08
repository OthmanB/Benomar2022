### What is it? ###
There is a (1) routine in c++ that make a Lorentzian from functions defined in the build_lorentzian.cpp file of TAMCMC
and (2) a python program that call that routine in order to visualise the Lorentzian along with the expected input values.
This allows the user to verify that the functions that make the Lorentzians are behaving as expected.

### How to use it? ###
   Ensure that you have Eigen3 properly loaded in your bash/csh file. Then,
  (1) Compile the c++ routine
   mkdir build
   cd build
   cmake ..
  
   You will get the 'lorentzian_test' executable within the root directory of the project. If you want to run it yourself, just execute it and it will show you how to use it
   
   To get the plots created for the Benomar+2022 paper use,
   (2) python3 show_aj_l12.py
