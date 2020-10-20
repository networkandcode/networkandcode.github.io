---
title: python > important modules
categories: python
---

There could be tasks that we intend to perform in Python, which are not doable straightway by a builtin function or class method, we would have to import specific 
modules for that purpose, a module in its simple terms is nothing but a python file. We are gonna see some important modules in this post.

### Datetime

The datetime module as its name says, is used for performing some date / time related tasks.
We need to import it first to start using it.
```
>>> import datetime
```

Let's check the contents of the datetime module.
```
>>> print(dir(datetime))
['MAXYEAR', 'MINYEAR', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'date', 'datetime', 'datetime_CAPI', 'sys', 'time', 'timedelta', 'timezone', 'tzinfo']
```

There is a datetime object inside the datetime module, lets check what it is, and its contents.
```
>>> print(datetime.datetime)
<class 'datetime.datetime'>
>>> print(dir(datetime.datetime))
['__add__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__radd__', '__reduce__', '__reduce_ex__', '__repr__', '__rsub__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', 'astimezone', 'combine', 'ctime', 'date', 'day', 'dst', 'fold', 'fromisocalendar', 'fromisoformat', 'fromordinal', 'fromtimestamp', 'hour', 'isocalendar', 'isoformat', 'isoweekday', 'max', 'microsecond', 'min', 'minute', 'month', 'now', 'replace', 'resolution', 'second', 'strftime', 'strptime', 'time', 'timestamp', 'timetuple', 'timetz', 'today', 'toordinal', 'tzinfo', 'tzname', 'utcfromtimestamp', 'utcnow', 'utcoffset', 'utctimetuple', 'weekday', 'year']
```
So the datetime object is a class, and its components are shown above.

Let's try one of the components of the datetime object, which is 'now'.
```
>>> print(type(datetime.datetime.now))
<class 'builtin_function_or_method'>
>>> print(datetime.datetime.now)
<built-in method now of type object at 0x923b80>
```
This shows 'now' is a method in the datetime class. Let's try calling it.
```
>>> print(datetime.datetime.now())
2020-10-20 06:52:53.626825
```
So the 'now' method of the 'datetime' class in the 'datetime' module helps display the current date and time.

#### from
We could also directly import the datetime class from the datetime module using the 'from' statement as follows.
```
>>> from datetime import datetime
```
Now the imported 'datetime' object directly refers to the class.
```
>>> print (datetime.now())
2020-10-20 09:01:09.983348
```
So we are able to print the date and time using datetime.now() instead of datetime.datetime.now().

#### formatting
We can print the date and time in a format we desire.

Let's first assign the result of now() to a variable 'd'.
```
>>> d = datetime.now()
```

The object or variable d would be an instance of the datetime class.
```
>>> print(type(d))
<class 'datetime.datetime'>
```

We can see the date and time as we saw before, if we print d.
```
>>> print(d)
2020-10-20 09:02:24.618694
```

The contents of this datetime instance could be checked.
```
>>> print(dir(d))
['__add__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__radd__', '__reduce__', '__reduce_ex__', '__repr__', '__rsub__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', 'astimezone', 'combine', 'ctime', 'date', 'day', 'dst', 'fold', 'fromisocalendar', 'fromisoformat', 'fromordinal', 'fromtimestamp', 'hour', 'isocalendar', 'isoformat', 'isoweekday', 'max', 'microsecond', 'min', 'minute', 'month', 'now', 'replace', 'resolution', 'second', 'strftime', 'strptime', 'time', 'timestamp', 'timetuple', 'timetz', 'today', 'toordinal', 'tzinfo', 'tzname', 'utcfromtimestamp', 'utcnow', 'utcoffset', 'utctimetuple', 'weekday', 'year']
```

Note that strftime is one of the contents listed above, its a method using which we shall try changing the format now.
```
>>> print(d.strftime("%b %d %Y"))
Oct 20 2020
```

In the print function above
- %b stands for Month is shorter version ex. Dec, Apr
- %d for date
- %Y for year in larger version  ex. 2020

Let's try one other formatting.
```
>>> print(d.strftime("%b---%d---%y"))
Oct---20---20
```
Here, %y stands for year (shorter version), ex. 20

### Math
The math module is used for performing certain mathematical calcualtions.

Let's import it.
```
>>> import math
```

Check its contents.
```
>>> print(dir(math))
['__doc__', '__loader__', '__name__', '__package__', '__spec__', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'comb', 'copysign', 'cos', 'cosh', 'degrees', 'dist', 'e', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite', 'isinf', 'isnan', 'isqrt', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'nan', 'perm', 'pi', 'pow', 'prod', 'radians', 'remainder', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau', 'trunc']
```

Lets try ceil, which is one of the methods in the math module, which rounds off the number upwards to the nearest integer.
```
>>> print(math.ceil(9.9))
10
>>> print(math.ceil(10.1))
11
```

And then, floor, which rounds off the number downards to the nearest integer.
```
>>> print(math.floor(9.9))
9
>>> print(math.floor(10.1))
10
```

### Random
We can generate random numbers using the random module. The randint method lets us choose an integer range, and the random method with in the random module helps in 
generating a random float as follows.
```
>>> import random
>>>
>>> print(dir(random))
['BPF', 'LOG4', 'NV_MAGICCONST', 'RECIP_BPF', 'Random', 'SG_MAGICCONST', 'SystemRandom', 'TWOPI', '_Sequence', '_Set', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '_accumulate', '_acos', '_bisect', '_ceil', '_cos', '_e', '_exp', '_inst', '_log', '_os', '_pi', '_random', '_repeat', '_sha512', '_sin', '_sqrt', '_test', '_test_generator', '_urandom', '_warn', 'betavariate', 'choice', 'choices', 'expovariate', 'gammavariate', 'gauss', 'getrandbits', 'getstate', 'lognormvariate', 'normalvariate', 'paretovariate', 'randint', 'random', 'randrange', 'sample', 'seed', 'setstate', 'shuffle', 'triangular', 'uniform', 'vonmisesvariate', 'weibullvariate']
>>>
>>> print(random.randint(1, 9))  # any random number between 1 and 9
2
>>>
>>> print(random.random())  # any random float between 0 and 1
0.8855626065544242
```

### Conclusion
So, we have tried exploring few important modules using the from and import stamentents, checked the contents of the modules, and explored certain methods of the 
modules. Thank you.

--end-of-post--
