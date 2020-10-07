---
title: python > functions or methods
categories: python
---

### Topic
We are gonna do some exercises on Functions or Methods which are blocks of code that be can be reused at various parts 
of the program.

### Prerequistes
- Python3 should be installed.
- You should know how the if else statement works.

### BuiltIn
There are certain built-in functions or methods that can be used with any datatype, examples are print(), dir(). 
```
>>> (type(print))
<class 'builtin_function_or_method'>
>>> (type(dir))
<class 'builtin_function_or_method'>
```
Methods are like functions, except that the term method is used to specify a function, which is available to an object that 
is an instance of a Class. So, methods are functions which are defined in Classes. Since, we can use print(), dir() etc. 
with any datatype, these are often referred to as built in functions. 

Another difference to note is that objectnames or values are followed by the functions, for instance ```print('orange')```, 
where as methods are follwoed by the objectname and a dot '.'. 
Let's define a string
```
>>> color = 'orange'
```
So color is our object name and it belongs to the class 'str'
```
>>> print(type(color))
<class 'str'>
```
Since color is an instance of the 'str' class, it should be able to use the methods defined in the 'str' class. 
upper() is one of the valid methods for the 'str' class, so as said earlier, we need to call the method using the format 
objectname.methodname(arguments if any)
```
>> color.upper()
'ORANGE'
```
### Function with defaults
Let's define a function to add three numbers
In the snippet below, def is the keyword that defines a function, sumOfThree is the name of the function, 
a,b,c are parameters of the function. 1,2, and 3 are the default values for a,b, and c.
```
>>> def sumOfThree(a=1, b=2, c=3):
...     print(a + b + c)
...
```
### Call the function
Since the function is defined, we can now call it in our program in different ways...

Note that when we pass values to a function, we call those values as ```arguments```, where as we call the variables 
within our function as ```parameters```.

#### All Defaults
```
>>> sumOfThree()
6
```
#### All Arguments

Next, we would pass all 3 arguments so they take specific values instead of default values.
```
>>> a = 10
>>> b = 20
>>> c = 30
>>> sumOfThree(a, b, c)
60
```
#### Two Arguments, One Default
```
>>> a = 10
>>> b = 20
>>> sumOfThree(a, b)
33
```

#### One Argument, Two Defaults
```
>>> a = 10
>>> sumOfThree(a)
15
```

This way, if we have setup default values in our function for the parameters, we can either pass specific values to 
those, or let them use their default values. Choice is ours. However, its only optional to define default values for 
parameters in a function.

### Function with out parameters
Its not always necessary to define a function with parameters
```
>>> def fn():
...   print('Hello World!')
...
>>> fn()
Hello World!
```
So this function fn() doesn't have any parameters, and hence there was no need to pass any arguments while calling 
the function

### Function with out defaults
Let's define a function with parameters, but with out any default values for those parameters.
```
def findIfMultiple(x, y):  # parameters
    if x % y == 0:
        return 'yes'
    else:
        return 'no'
```
This function should help finding if the value x is an exact multiple of y, note that the math operator '%' is used to 
find the remainder. And the ```return``` statement is passed back to the program, so if we try to print this function, 
the value that gets passed by the ```return``` statement would be printed, in this case ```yes``` or ```no```. Note 
that we can use ```return``` statements for a function irrespective of the function has parameters or not. If we don't have 
a return statement in a function, i.e. if the function is not returning any value, we can call that a ```void``` function.

Alright, let's now call the function
```
>>> a = 100
>>> b = 11
>>> print(findIfMultiple(a, b))  # arguments
no
```
#### Positional arguments
So here we passed ```a``` and ```b``` as arguments, which would become ```x``` and ```y``` respectively with in the function. 
So the names we use for the variables that we pass as arguments doesn't really matter, the position matters, so the 
argument in the first position ```a``` corresponds to the first parameter ```x``` and similarly the second argument ```b``` 
would map with the second paremeter ```y```

Well we got the value as ```no``` cause 100 divided by 11 gives 9 as quotient and remainder is ```1```, so if you take a 
look at the function again, you see that the function should return ```no``` when the remainder is not ```0```.

Let's pass another set of arguments
```
>>> x = 100
>>> y = 5
>>> print(findIfMultiple(x, y))  # arguments
yes
```
So 100 / 5 gives quotient 20 and remainder 0, hence it returns ```yes```.

##### Multiplication example
```
$ cat multiply.py
def mul(number1, number2):
    print(number1 * number2)


mul(100, 10)
mul(10, 90)
mul(15, 50)
```
Here we have kept the code in a file and then would execute it as a script. The example above was done in Linux, however can be tried in any 
operating system where Python is installed. Above, we have used the cat utility in Linux to display the file's contents.

```
$ python3 multiply.py
1000
900
750
```
#### Keyword arguments
Keyword arguments can also be passed to a function as follows
```
>>> findIfMultiple(x = 200, y = 100)
'yes'
>>> findIfMultiple(x = 200, y = 99)
'no'
```
So we pass values for arguments while calling the function itself, by sepcifying the exact parameter,  here position 
doesn't matter
```
>>> findIfMultiple(y = 99, x = 200)
'no'
```

#### Positional and Keyword args
We can also mix positional and arguments while calling the function but the only condition to note is that the postional 
arguments must be mentioned first and the keyword arguments next, if we do vice versa, it would throw an error
```
>>> findIfMultiple(200, y = 99)
'no'
```
The code above executes as the positional argument(200 which maps with x) is specified first, where as the following code 
would break and throws a SyntaxError
```
>>> findIfMultiple(x=200, 99)
--TRUNCATED--
SyntaxError: positional argument follows keyword argument
```
### Another example
Here is another example to try keyword arguments and positional arguments
```
>>> def fn(a, b, c):
...     print(a * b / c)
...
>>> fn(10, 2, 5)
4.0
>>>
>>> fn(a=10, b=2, c=5) # keyword args
4.0
>>>
>>> fn(b=2, c=5, a=10) # keyword args
4.0
>>>
>>> fn(10, c=5, b=2)
4.0
```
```
>>> fn(a=10, 2, c=5)  # SyntaxError: positional argument follows keyword argument
--TRUNCATED--
SyntaxError: positional argument follows keyword argument
```
### Void
We have discussed earlier, that if a function doesn't have a return statement, it can be called a void function. Alternatly 
we can also pass ```retun None``` explicitly to acheieve the same behaviour.
```
>>> def fn2():
...    print('hi')
...    return None  # this is equivalent to having no return statement in the function
...
>>> fn2()
hi
```

### Scope
We can define outside a function in our main program with ```global``` scope, or inside a function with ```local``` scope
#### Local only
```
>>> def fn1():
...    x = 5  # local scope
...    print(x)
...
>>> fn1()
5
```
#### Global only
```
>>> def fn2():
...    print(y)
...
>>> y = 10  # global scope
>>> fn2()
10
```

#### Local and Global
Local will be preferred
```
>>> def fn3():
...    z = 100  # local scope
...    print(z)
...
>>> z = 1  # global scope
>>> fn3()
100
```

#### Use or in format 
A default value can be specified in format, when an argument is passed to a function
```
>>> def howareyou(name=None):
...     return('Hi {}, how are you' .format(name or 'friend'))
...
>>> howareyou('Ahmed')
'Hi Ahmed, how are you'
>>> howareyou()
'Hi friend, how are you'
```

--end-of-post--
