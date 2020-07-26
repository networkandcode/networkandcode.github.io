/---
title: python > numbers
categories: python
---

We shall try few examples in this post for doing some mathematical operations 
using Python. There is no much prerequisite except that You should know 
how to run Python code.

## Assign numbers to variables
'*' is used for multiplication and '+' is used for addition.
```
$ cat arithmetic.py
print("Example for arithmetic operation")

number1 = 90
number2 = 10

print(number1 * number2)
print(number1 + number2)
$ python3 arithmetic.py
Example for arithmetic operation
900
100
```

### Addition, Subtraction, Multiplication, Division, and Remainder
Note that '%' is used for modulus operation which returns the remainder 
after division. 
```
$ cat ex1.py
# Math operations on numbers

print ( 1 + 2 )

print ( 2 - 1)

print ( 2 * 1 )

print ( 10 / 2 )

print ( 10 % 3 )

$ python3 ex1.py
3
1
2
5.0
1
```

## Type, Id and Multi operations
The type function is used to identify the type of a variable, it should 
say 'int' for all numbers with out decimal points. The id function returns 
the location in memory where the variable will be stored.
```
$ cat ex2.py

a = 1
b = 2
c = 3

print (type(a), type(b), type(c))

print (id(a), id(b), id(c))

print ( a + b + c )  # 6
print ( a * b * c )  # 6
print ( b * c / a )  # 1
print (  c % 2 )     # 1

$ python3 ex2.py
<class 'int'> <class 'int'> <class 'int'>
9756192 9756224 9756256
6
6
6.0
1
```

### Float
Floats are numbers with decimal points.
```
$ cat ex3.py
number = 100
print(type(number))
print(number)

floatNumber = 10.6
print(type(floatNumber))
print(floatNumber)

floatNumber = 100.0
print(type(floatNumber))
print(floatNumber)

$ python3 ex3.py
<class 'int'>
100
<class 'float'>
10.6
<class 'float'>
100.0
```

## Odd or Even numbers
Let's write code to find if a number is odd or even, note that the input function is used to get some input from the user as string.
```
$ cat odd-or-even.py
numberString = input('Please input the number ')    # this is always a string

number = int(numberString)   # converting string to integer

if (number == 0):
    print('Neither odd nor even')
elif (number % 2 == 0):
    print('This is even')
else:
    print('This is odd')
```

```
$ python3 odd-or-even.py
Please input the number 7
This is odd

$ python3 odd-or-even.py
Please input the number 4
This is even
```

```
$ python3 odd-or-even.py
Please input the number 0
Neither odd nor even
```
--end-of-post--

