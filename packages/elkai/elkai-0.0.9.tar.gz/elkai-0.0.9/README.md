elkai - a Python 3 TSP solver
====

elkai is a Python 3 library for solving [travelling salesman problems](https://en.wikipedia.org/wiki/Travelling_salesman_problem) without external dependencies,
based on [LKH](http://akira.ruc.dk/~keld/research/LKH/) by
Keld Helsgaun.

💾 **To install it** run `pip install elkai`

💻 **Supported platforms:** elkai is available on Windows, Linux, OS X for Python 3.5 and above as a binary wheel.


[![Build status](https://ci.appveyor.com/api/projects/status/agi76gjl3e2m00oq?svg=true)](https://ci.appveyor.com/project/filipArena/elkai)
[![image](https://img.shields.io/pypi/v/elkai.svg)](https://pypi.org/project/elkai/)

Example usage 
----------

```python
import numpy as np
import elkai

M = np.zeros((3, 3), dtype=int)
M[0, 1] = 4
M[1, 2] = 5
elkai.solve_int_matrix(M) # Output: [0, 2, 1]
```

Documentation
-------------


**solve_int_matrix(matrix, runs=10)** solves an instance of the asymmetric TSP problem with integer distances.

* `matrix`:
   *an N\*N matrix representing an integer distance matrix between cities.*
   
   *An example of N=3 city arrangement:*
   ```python
   [                  # cities are zero indexed, d() is distance
       [0, 4,  9],    # d(0, 0), d(0, 1), d(0, 2)
       [4, 0, 10],    # d(1, 0), d(1, 1), ...
       [2, 4,  0]     # ... and so on
   ]
   ```

* `runs`:
  *An integer representing how many iterations the solver should
  perform. By default, 10.*

* Return value: *The tour represented as a list of indices. The indices are
   zero-indexed and based on the distance matrix order.*




**solve_float_matrix(matrix, runs=10)** has the same signature as the previous, but allows floating point distances.
It may be inaccurate.

FAQ
----------------------

**What's the difference between LKH and elkai?**

elkai is a library that contains the [LKH solver](http://akira.ruc.dk/~keld) and has some wrapper code to expose it to Python.
The advantage is that you don't have to compile LKH yourself or download its executables and then manually parse the output.
Note that elkai and its author are not affiliated with the LKH project. **Note:** Helsgaun released the LKH project for non-commercial use only, so elkai must be used this way too.

**How to manually build the library?**

You need CMake, a C compiler and Python 3.5+. You need to install the dev dependencies first: `pip install scikit-build ninja`. To build the library, run `python setup.py build` and `python setup.py install` to install it. To make a binary wheel, run `python setup.py bdist_wheel`.

**How accurately does it solve asymmetric TSP problems?**

Instances with known solutions, which are up to N=315 cities, [can be solved optimally](http://akira.ruc.dk/~keld/research/LKH/Soler_ATSP_results.html).

**Can you run multiple threads?**

The library doesn't not release the GIL during the solution search, so other threads will be blocked. If you want to solve multiple problems
concurrently you may try the [multiprocessing](https://docs.python.org/3.7/library/multiprocessing.html) module. 

*P.S.:* The LKH solver was written in C with one problem per process in mind. We try to clean up the global state before and after solving a problem, but leaks are possible - if you want to help out, run Valgrind or similar diagnostics and submit an issue/PR.
