Description
===========

Requirements
------------

* python >= 3.6
* pandas >= 0.23


------------

Module, provides the function DFinfo, which displays general information on the data:
  - Upgrade method info()
  

Install
-------
	$ pip install DF-info

Usage
-----

    $ python3

    from DF-info import *

    d = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])

    DF-info(d)

