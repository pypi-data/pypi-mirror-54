# About
Module for checking input parameters by type

# Simple Start

1. Install package from pip
```
pip install checkparam
```

2. Use
```
from checkparam import check_param

@check_param()
def my_func(var_one: int, var_two: typing.Optional[int]): 
  ...
  
my_func(4, None)       # all good
my_func('test', None)  # Exception from check_param, becouse 'test' is not type 'int'

```
