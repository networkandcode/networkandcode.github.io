---
title: python > user input
categories: python
---

Sometimes its necessary to take some input from the user and pass it to 
the program, let's explore with few examples. Its assumed you know to write 
functions, for and while statements.

## Example1

```
$ cat ex1.py
# use of input

firstName = input('What\'s your First Name ')
country = input('Which country you belong to ')

print('Hi {}, you are from {}'.format(firstName, country))
print('Hi ' + firstName + ', you are from ' + country)


def simpleFunction(firstName, country):
    print('Hi {}, you are from {}'.format(firstName, country))
    print('Hi ' + firstName + ', you are from ' + country)
    print('~' * 25)

simpleFunction(firstName, country)
```
```
$ python3 ex1.py
What's your First Name Shahul
Which country you belong to India
Hi Shahul, you are from India
Hi Shahul, you are from India
Hi Shahul, you are from India
Hi Shahul, you are from India
~~~~~~~~~~~~~~~~~~~~~~~~~
```

## Example 2

```
$ cat ex2.py
# infinite loop

def simpleFunction(firstName, country):
    print('Hi {}, you are from {}'.format(firstName, country))
    print('Hi ' + firstName + ', you are from ' + country)
    print('~' * 25)

while True:
    firstName = input('What\'s your First Name ')
    country = input('Which country you belong to ')

    simpleFunction(firstName, country)
```
```
$ python3 ex5.py
What's your First Name Mohammed
Which country you belong to America
Hi Mohammed, you are from America
Hi Mohammed, you are from America
~~~~~~~~~~~~~~~~~~~~~~~~~
What's your First Name Hussain
Which country you belong to UK
Hi Hussain, you are from UK
Hi Hussain, you are from UK
~~~~~~~~~~~~~~~~~~~~~~~~~
What's your First Name   
```
The loop would keep continuing, until we press Ctrl C, this is because 
we have written while True, and there is no condition to break the while 
loop. 

## Example 3
```
$ cat ex3.py
# finite loop, integer input

def simpleFunction(firstName, country):
    print('Hi {}, you are from {}'.format(firstName, country))
    print('Hi ' + firstName + ', you are from ' + country)
    print('~' * 25)

n = int(input('How many people are there '))

i = 0  # or put i = 1 and i <= n
while i < n:
    firstName = input('What\'s your First Name ')
    country = input('Which country you belong to ')

    simpleFunction(firstName, country)
    i = i + 1
```
```
$ python3 ex3.py
How many people are there 2
What's your First Name Alexander
Which country you belong to Russia
Hi Alexander, you are from Russia
Hi Alexander, you are from Russia
~~~~~~~~~~~~~~~~~~~~~~~~~
What's your First Name Moses
Which country you belong to Egypt
Hi Moses, you are from Egypt
Hi Moses, you are from Egypt
~~~~~~~~~~~~~~~~~~~~~~~~~
```
Its a finite loop this time, as i increments with each iteration of the 
while loop, and the loop breaks when i < n. It would run twice, as 
we gave 2, i.e. n is 2.

## Example 4
```
$ cat ex4.py
# for loop

def simpleFunction(firstName, country):
    print('Hi {}, you are from {}'.format(firstName, country))
    print('Hi ' + firstName + ', you are from ' + country)
    print('~' * 25)

n = int(input('How many people are there '))

for i in range(0, n):   # you may also use for i in range(1, n+1)
    firstName = input('What\'s your First Name ')
    country = input('Which country you belong to ')

    simpleFunction(firstName, country)
    i = i + 1
```
Its a finite loop, but with 'for'
```
$ python3 ex4.py
How many people are there 1
What's your First Name Samsung
Which country you belong to Finland
Hi Samsung, you are from Finland
Hi Samsung, you are from Finland
~~~~~~~~~~~~~~~~~~~~~~~~~
```

## Example 5
```
# return value from function

def simpleFunction(firstName, country):
    print('Hi {}, you are from {}'.format(firstName, country))
    print('Hi ' + firstName + ', you are from ' + country)
    print('~' * 25)

n = int(input('How many people are there '))

def takeInput(var):
    firstName = input('What\'s your First Name ')
    country = input('Which country you belong to ')

    simpleFunction(firstName, country)
    var = var + 1
    return var

i = 0  # or put i = 1 and i <= n
while i < n:
    i = takeInput(i)
    #takeInput(i)
    #i = i + 1
    print(i)
```
```
# return value from function

def simpleFunction(firstName, country):
    print('Hi {}, you are from {}'.format(firstName, country))
    print('Hi ' + firstName + ', you are from ' + country)
    print('~' * 25)

n = int(input('How many people are there '))

def takeInput(var):
    firstName = input('What\'s your First Name ')
    country = input('Which country you belong to ')

    simpleFunction(firstName, country)
    var = var + 1
    return var

i = 0  # or put i = 1 and i <= n
while i < n:
    i = takeInput(i)
    print(i)
```

--end-of-post--
