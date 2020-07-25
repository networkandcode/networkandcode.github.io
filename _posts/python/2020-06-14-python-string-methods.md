---
title: python > string methods and functions
categories: python
---

Strings are one of the most used datatypes, and some practice on string 
methods should help in shortening lines of code for tasks associated with 
strings. There is no much prerequisite for this topic except knowing how to run 
Python code.

Methods are nothing but functions that are available to objects belonging
to a Class. In Python, string is also a class, so if you are creating a 
string variable, it actually means that you are creating an object or 
an instance that belongs to the string class 'str'. Note that methods are 
followed after the object name and a '.', for ex. if sampleString is the 
object name and strip is the method, we need to call it by executing 
sampleString.strip()

### Initialize
Let's launch the Python terminal and initialize a string
```
networkandcode $ python3
Python 3.8.2 (default, Apr 27 2020, 15:53:34)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> sampleString = '  This World is so Huge !!!  '
```
Anytext that is enclosed with in single or double quotes are considered a string. 
We have used single quotes above. We can check the datatype of this variable
```
>>> print(type(sampleString))
<class 'str'>
```
So Python has assigned this variable to the class 'str' i.e. string.

### Dir
Check the available attributes and methods for our object using the 'dir' 
function
```
>>> dir(sampleString)
['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', 
'__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', 
'__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', 
'__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', 
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', 
'__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 
'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 
'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 
'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 
'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 
'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 
'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 
'translate', 'upper', 'zfill']
```
We are going to try few of these methods
### Strip 
We see that are some space characters at the beginning and ending of the string
```
>>> print(sampleString)
  This World is so Huge !!!
```

The strip method can be used to take off these spaces
```
>>> sampleString.strip()
'This World is so Huge !!!'
```

However the original variable would still be unchanged
```
>>> print(sampleString)
  This World is so Huge !!!
```
However we can assign it to the same variable or a new one
```
>>> sampleString = sampleString.strip()
>>> print(sampleString)
This World is so Huge !!!
```

### Replace
Characters or Words in the String can be replaced with new ones
To replace 'Word' with 'Earth'
```
>>> sampleString = sampleString.replace('World', 'Earth')
>>> print(sampleString)
This Earth is so Huge !!!
```
Note that although we are storing the modified string with the same object 
name i.e. 'sampleString', its treated like a new variable internally, as 
a new location in memory gets assigned each time, we can use the 'id' function 
to check the memory location
```
>>> print(id(sampleString))
140615517003488
```
So this is the existing location in memory, and now let's replace 's' 
with '$' in the string and check the memory location again
```
>>> print(id(sampleString))
140615517001648
>>> print(sampleString)
Thi$ Earth i$ $o Huge !!!
```
### Length
The 'len' function can be used to check the length of the string in terms 
of number of characters in it, including spaces if any. Note that this is 
a global function and not an object method
```
>>> print(len(sampleString))
25
```

### Indexing
We can use positive or negative index to access a particular character of 
the string, We know the overall length is 25 so the index would range from 
0 to 24, or from -25 to -1 in negative
```
>>> print(sampleString[0], sampleString[24])
T !
>>> print(sampleString[-25], sampleString[-1])
T !
```
We may also print a range of characters i.e. slice it
```
>>> print(sampleString[3:6])
$ E
```
The above statement has printed characters 3 to 5, note that last position  
in the range i.e. 6 will not be included

### Convert case
We can covert the case of the string using some methods as follows
#### Lower case
```
>>> print(sampleString.lower())
thi$ earth i$ $o huge !!!
```
We can check if a string is in lower case or not using 'islower' method
```
>>> sampleString = sampleString.lower()
>>> print(sampleString.islower())
True
```
#### Capitalize
The first letter of the statement will be in Capital letter
```
>>> print(sampleString.capitalize())
Thi$ earth i$ $o huge !!!
```

#### Upper case
```
>>> print(sampleString)
THI$ EARTH I$ $O HUGE !!!
>>> print(sampleString.isupper())
True
```

#### Title case
To check if the first letter of each word is capital
```
>>> print(sampleString.istitle())
False
>>> sampleString = sampleString.title()
>>> print(sampleString)
Thi$ Earth I$ $O Huge !!!
>>> print(sampleString.istitle())
True
```
We can also directly include the strings instead of the object names
```
>>> print('Hello World'.istitle())
True
>>> print('H E L L O W O R L D'.istitle())
True
```
#### Swap case
To swap the case of each character
```
>>> print(sampleString.swapcase())
tHI$ eARTH i$ $o hUGE !!!
```

### Split
We can split the string based on a delimiter, the resulting value will be 
a list of multiple strings
Let's split it based on space characters, jus split or split(' ')
```
>>> print(sampleString.split())
['Thi$', 'Earth', 'I$', '$O', 'Huge', '!!!']

>>> print(type(sampleString.split()))
<class 'list'>

>>> print(sampleString.split(' '))
['Thi$', 'Earth', 'I$', '$O', 'Huge', '!!!']
```
We can use indexing, to access elements of the list
```
>>> print(sampleString.split()[0])
Thi$
>>> print(sampleString.split()[1])
Earth
```

And this time let's split with '$'
```
>>> print(sampleString.split('$'))
['Thi', ' Earth I', ' ', 'O Huge !!!']
```
We can use words too, for ex. 'Huge'
```
>>> print(sampleString.split('Huge'))
['Thi$ Earth I$ $O ', ' !!!']
```

We can split multiline strings using split('\n') or splilines(), multiline 
strings are enclosed with in 3 quotes. Note that '\n' stands for new line character
```
>>> sampleMultilineString = '''hi
... hello
...   how are you
... are you
...   fine
... '''
>>> print(sampleMultilineString)
hi
hello
  how are you
are you
  fine
>>> print(sampleMultilineString.split('\n'))
['hi', 'hello', '  how are you', 'are you', '  fine', '']
>>> print(sampleMultilineString.splitlines())
['hi', 'hello', '  how are you', 'are you', '  fine']
```
The difference is that splitlines doesn't include any trailing space characters like split('\n')

### Delete
To delete the objects
```
>>> del sampleString
>>> del sampleMultilineString
```
Trying to call the objects would now throw 'NameError'
```
>>> print(sampleString)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'sampleString' is not defined
>>> print(sampleMultilineString)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'sampleMultilineString' is not defined
```
### Comments
We can add comments to our program to help identifying what the code is 
meant for. Those are like some handy reference or notes for our codes. 
Comments are also strings that do not get processed by the Interpreter. 
'#' can used for single line comments
```
>>> # This is a single line comment
```
If multiline comments are not natively supported by Python, however if 
needed, there is a work aroung to include docstrings 
that are just mutliline strings, not assigned to any variable, so the 
program doesn't really make use of it, it just executes it though as a string
```
>>> ''' This
... is a
... multiline
... docstring'''
' This \nis a \nmultiline \ndocstring'
```
### Script
We can put code in a file and then run it as a script. Here is an example to do concatenation of two strings.
```
$ cat string-concatenation.py
print("Example for string operation")

firstName = "Michael"
lastName = "Jackson"

fullName = firstName + " " + lastName

print(fullName)

$ python3 string-concatenation.py
Example for string operation
Michael Jackson
```
We have used the cat utility in Linux above to display the file's contents, however all we need is a file edited using any text editor in 
any operating system where Python is installed, and then run that file as a script using Python.

### If Else
```
$ cat ex3.py
# Strings with If else, and function

a = '"Hello"'
b = "'World'"
c = "\"Hi All\""
d = '\'How are you\''
e = a + b

print (a)
print (b)
print ( a + ' ' + b )
print (c)
print (d)
print ( e )

print ('\n' * 2 )

print (len(d))

if ('How' in d):
    print ('yes')
else:
    print ('no')

if ('You' in c):
    print ('yes')
else:
    print ('no')

def  findInString(var1, var2):
    if (var1 in var2):
        print('yes')
    else:
        print('no')

findInString('How', d)
findInString('You', c)
findInString(a, e)
findInString(b, e)
findInString('S', 'Shahul')
findInString(a, 'RandomString')
```

```
$ python3 ex3.py
"Hello"
'World'
"Hello" 'World'
"Hi All"
'How are you'
"Hello"'World'



13
yes
no
yes
no
yes
yes
yes
no
```

--end-of-post--
