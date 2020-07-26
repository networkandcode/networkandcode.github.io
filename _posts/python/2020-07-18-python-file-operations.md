---
title: python > file operations
categories: python
---

Python's inbuilt open function could be used to interact with the file system of the underlying operating system. Let's see more on this. You 
should know some fundamentals of Python such as the indentation in each block of code, the for statement etc. to better understand this post.

### Write
Let's create a file with name 'firstfile.txt', note that we give two arguments to the open function, the first one says the filename, and the 
second argument referes to the mode, for example 'w' stands for write. 
So the following code would create a file if it doesn't exist, or overwrite it if it already exists. 
```
# w for write
# to create a file and write
# or to overwrite
with open('firstfile.txt', 'w') as file:    # file is a variable
    file.write('This is my first file\n')
    file.write('created using python\n')
```
output:
```
22
21
```
If we are executing this in the interpreter instead of running it as a script in file, it should display the number of characters added such as 22
 and 21 above.

The 'with' and 'as' statements are the preferred way of dealing with files, as once the block is executed, the file that is opened would 
automatically be closed. If we have interacted with files by calling f = open(filename) with out 'with', then we may also have to it close it 
by saying f.close(), this is eliminated when we use the 'with as' block. 

Let's now read what we have written. 
```
# r for read mode
with open('firstfile.txt', 'r') as f:   # f is a variable
    print(f.read())  # reads up to the max buffer size
    # to read the entire capacity of the system's buffer
    # this would print an error if the file is not existing 
```
output:
```
This is my first file
created using python

```

### Append and Read
Let's try appending this time, which means it would create a new file if it wasn't existing before, and if the file is already existing it would 
append contents at the end of file.
```
# a for append
# doesnt overwrite
with open('secondfile.txt', 'a') as file:    # file is a variable
    file.write('This is my second file\n')
    file.write('created using python\n')
```
And now let's read the contents.
```
# r for read mode
with open('secondfile.txt', 'r') as f:   # f is a variable
    print(f.read())
```
output:	
```
This is my second file
created using python

```

### Read
We can read the complete file, or certain number of characters, or line by line
```
# r for read mode
>>> with open('secondfile.txt', 'r') as f:
...     print(f.read(5))  # reads the first five characters
...     print(f.readline())  # reads rest of the line from the sixth character, as the marker is moved by 5 characters above
...     print(f.read(5))  # reads the next five characters
...     print(f.read())  # reads rest of the file
...
This
is my second file

creat
ed using python

```

Or all the lines at once, and the resulting output would be a list
```
with open('secondfile.txt', 'r') as f:   # f is a variable
    print(f.readlines())  # list
```
output:
```
['This is my second file\n', 'created using python\n']
```

### Loop
We can also loop over the lines of the file using the for statement.
```
with open('secondfile.txt', 'r') as f:   # f is a variable
    for i in f:
        print(i)
```
output:
```
This is my second file

created using python

```

Note that the print statement, adds a new line character, at the end by default, if we need to avoid that, we can say "end=''".
```
with open('secondfile.txt', 'r') as f:   # f is a variable
    for i in f:
        print(i, end='')  # to avoid newline char at the end
```
output:
```
This is my second file
created using python
```

### Another example
Let's create a new file in the system, I am using a Linux instance, and I have the following contents in a file. 
```
$ cat sample-file.txt
Python is one of the
most popular programming languages
today.
Its object
oriented,
easy to learn,
and has libraries for wonderful things such as
web development, machine learning,
data science,
artificial intelligence,
network automation, and
so on.
```
You can put similar content with a filename of choice in your system. Let's now run python code to interact with this file.
#### Seek
seek is used to move the cursor or marker ahead by a certain number of characters
```
>>> # 'r' is the default mode
>>> # the file will automatically close after the with block
>>> # so there is no need for file.close()
>>> with open('sample-file.txt', 'r') as f:
...     f.seek(4)
...     print(f.read())
...
4
on is one of the
most popular programming languages
today.
Its object
oriented,
easy to learn,
and has libraries for wonderful things such as
web development, machine learning,
data science,
artificial intelligence,
network automation, and
so on.

>>> print('-' * 25)
-------------------------
```
So, the output above doesn't contain the first 4 characters 'Pyth', as we have used the seek method to move forward by 4 characters.

#### Tell
We can retrieve the current position of the cursor in the file using the tell method.
```
>>> with open('sample-file.txt', 'r') as f:
...     f.seek(10)  # move from the beginning of the file
...     print(f.tell())  # current position
...     print(f.readline())
...     print(f.readline())
...     print(f.tell())  
...     f.seek(27)  # move forward from the beginnning of the file by 27 characters
...     print(f.readline())
...
10
10
one of the

most popular programming languages

57
27
popular programming languages

>>> print('-' * 25)
-------------------------
```

#### Truncate
The truncate method is used to keep the first few characters as specified, and removes rest of the contents from the file.
```
>>> with open('sample-file.txt', 'a') as f:
...     f.truncate(15)
...
15
>>> with open('sample-file.txt', 'r') as f:
...     string = f.read()
...     print(len(string))
...     print(string)
...
15
Python is one o
>>> print('-' * 25)
-------------------------
```

If truncate is called with out passing any argument, it would keep the contents same.
```
>>> with open('sample-file.txt', 'a') as f:
...     f.truncate()
...
15
>>> with open('sample-file.txt', 'r') as f:
...     string = f.read()
...     print(len(string))
...     print(string)
...
15
Python is one o
>>> print('-' * 25)
-------------------------
```

However if we move the current position using seek, and then truncate, it would remove everything from the right of the marker.
```
>>> with open('sample-file.txt', 'a') as f:
...     f.seek(10)
...     f.truncate()
...
10
10
>>> with open('sample-file.txt', 'r') as f:
...     string = f.read()
...     print(len(string))
...     print(string)
...
10
Python is
```

### write lines
The writelines method could be used to write multiple lines to a file at once
```
>>> with open('new-file.txt', 'w') as f:
...     list = ['hi\n', 'how are you\n', 'how is life\n', 'hope everything is ok\n']
...     f.writelines(list)
...
>>> with open('new-file.txt', 'r') as f:
...     print(f.read())
...
hi
how are you
how is life
hope everything is ok

```
--end-of-post--
