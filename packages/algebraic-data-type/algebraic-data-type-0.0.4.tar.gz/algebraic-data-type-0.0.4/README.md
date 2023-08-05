Algebraic Data Type
===================

To install the package `pip install  algebraic-data-type`

ADT
---
[To be written]

Pattern Matching
----------------
```
from adt import Multimethod

 with Multimethod() as fib: 
        fib[1] = 1 
        fib[2] = 1 
        fib[int] =  lambda x: fib(x-1) + fib(x-2)
```

![example](./images/example1.png)

Test
----
To run the tests, clone the repo and use pytest

```
>>> git clone https://github.com/catethos/adt.git

>>> cd adt/

>>> pytest
```
