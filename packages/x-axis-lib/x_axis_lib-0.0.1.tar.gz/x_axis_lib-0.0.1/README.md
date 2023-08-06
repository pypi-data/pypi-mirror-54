### check if 2 x axis are overlapping

* python library for checking whether 2  x axis are overlapping
- expected params lists/sets/tuples
- returned value is a `boolean`

### Installation:

`pip3 install x_axis_lib`


### Usage:

```
from x_axis.overlap import overlapping

result1 = overlapping([1, 2], [34, -2]) # True
result2 = overlapping((5, 6,) (1, 4,)) # True
result3 = overlapping({56, 100}, {49, 23}) # False

```
