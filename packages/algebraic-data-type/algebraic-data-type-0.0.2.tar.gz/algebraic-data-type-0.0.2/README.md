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

