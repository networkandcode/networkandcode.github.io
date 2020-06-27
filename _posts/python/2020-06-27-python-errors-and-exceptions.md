---
title: python >  errors and exceptions
categories: python
---

A Python program can break due to various types of Errors. We shall explore few of these errors in the post. To make best use of use this post, you should know certain topics in Python3 such as datatypes, expression, pass statement, etc.

Not all errors are significant, and hence there would be cases where we can skip certain errors to uninterrupt execution of our code, and this achieved with ```try except``` blocks.

### ZeroDivisionError
This error is returned when we try divide any number by 0
```
>>> 50 / 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
```
This time we tell Python not to break execution, by including things in a ```try except``` block.
```
>>> try:
...     0 /0
... except ZeroDivisionError:
...     pass
...
```
The expression 00/0 in the try block should have produced a ZeroDivisionError, but since we are saying ```except ZeroDivisionError```, that error would be excepted. So there wont be any error and there should'nt be any output as well as we have included ```pass``` in the except block. Note that ```pass``` is used as a placeholder where you don't want the program to any program, and just to go the next line of the code in sequence if any.

Let's try a different example, and also try printing some info instead of pass.
```
>>> try:
...     120 / 0
... except:
...     print('oh there was an exception')
...
oh there was an exception
```

### TypeError
We can try  to do an unsupported math operation, for example division, between a string and an integer, to trigger this error
```
>>> 30 / 'hello'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for /: 'int' and 'str'
```
Another example, but we include an exception for the error this time
```
>>> try:
...    'text' + 20
... except TypeError:
...     print('There was a type error')
...
There was a type error
```

### NameError
When we try calling a variable a.k.a object name, that was not defined before, we should get a NameError
```
>>> print(name)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'name' is not defined
```

### Error on improper exception
Error would still occur if the except statement doesn't include the correct error type.
```
>>> try:
...    'text' + 20
... except ValueError:  # wont process as we get TypeError above
...     print('There was a value error')
...
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: can only concatenate str (not "int") to str
```
We get an error cause, as we tried to except ValueError, where as the statement in try block was producing TypeError


### Except Multiple Errors
We can include exceptions for multiple error types by separating each error type by a comma. The following example should have produced NameError.
```
>>> try:
...     print(name)
... except(NameError, TypeError):
...     print('There was a NameError or TypeError')
...
There was a NameError or TypeError
>>>
```
Another example for multiple exceptions, however it should have generated a TypeError
```
>>> name = 'Michael'
>>>
>>> try:
...     print(name)
...     'text' - 20
... except(NameError, TypeError):
...     print('There was a NameError or TypeError')
...
Michael
There was a NameError or TypeError
```    

Or we could even provide exceptions for any error by jus saying expect with out any error type. Let's try printing the variable city, which is not defined before, this should have caused a NameError
```
>>> try:
...     print(city)
... except:
...     print('oh! there was an exception error')
...
oh! there was an exception error
```
Note that in the snippet above, we have excepted all types of Errors and not just NameError.

One more example for providing exception to all errors
```
try:
    print(y)
except:
    print('There was an error, But that\'s ok, go ahead with the rest of the code')

print('Thank you')
```
>>> try:
...     print(y)
... except:
...     print('There was an error, But that\'s ok, go ahead with the rest of the code')
...
There was an error, But that's ok, go ahead with the rest of the code
>>> print('Thank you')
Thank you
>>>
```
### Print the standard message
Its sometimes much apt to print the message the error would have been generated for, instead of printing a user defined message
```
>>> try:
...    print(name)
... except NameError as n:
...     print(n)
...
name 'name' is not defined
```
So the mesage ```name 'name' is not defined``` is coming straight from the NameError itself, and says why there was a NameError. Here we have caught the error message as variable ```n``` by saying ```NameError as  n```, and then we ```print(n)``` it displays the error message or reason stored.

One more example
```
>>> try:
...     'string ' + 2
... except TypeError as t:
...     print(t)
...
can only concatenate str (not "int") to str
```
This time it printed the reason for the TypeError

### Raise Errors
We could even raise errors manually with the ```raise``` statement.
```
>>> try:
...     raise TypeError()
... except TypeError as t:
...     print(t)
...

```
It shouldn't print anything cause we raised the error manually, and there wasn't any standard error message, providing the reason on why it was generated.

We could however print a user defined message.
```
>>> try:
...     raise TypeError()
... except TypeError:
...     print('The type error was raised manually')
...
The type error was raised manually
```
--end-of-post--