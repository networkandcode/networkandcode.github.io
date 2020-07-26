---
title: python > loops
categories: python
---

Loops are common in all programmings languages, they help in executing tasks that are recurring in nature. Lets look at these loops in Python with few examples. The prerequisites are: knowing how to Python code through the Interpreter or as a script in a file.

## While
### Infinite Loop
#### With a string
```
# This is an infinite loop
# Ctrl z to stop it
while True:  # True means you dont have any condition set and you jus want to execute the loop    
    print("Hello...")
```
It would keep on printing 'Hello' until its interrupted with Ctrl C.
```
Hello
Hello
Hello
Hello
Hello
^CHello
Traceback (most recent call last):
  File "ex3.py", line 4, in <module>
    print("Hello")
KeyboardInterrupt
```
#### With a number
```
>>> # infinite loop once more
>>> i = 1
>>> while True:
...     print(i, 'hello')
...     i = i + 1
...
--TRUNCATED--
454 hello
455 hello
456 hello
^C457 hello
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
KeyboardInterrupt
```

### No Loop
```
>>> # this loop wont execute, bcause False is not the default condition
>>> while False:
...     print("Hello")
...
>>> 
```

### Finite Loop
The loop would break when the condition i <= 10 becomes false.
In each iteration, we are incrementing the value of i by 1. When i becomes 11, the loop breaks.
```
>>> i = 1
>>> while i <= 10:
...     print(i, 'Hello')
...     i = i + 1
...
1 Hello
--TRUNCATED--
10 Hello
```

### Break
The 'break' statement can also be used to break out of a loop based on certain condition.
```
$ cat break.py
# finite loop with the help of break
# not with the help of a condition after 'while'
i = 1
while True:
    print(i, 'hello')
    i = i + 1
    if i == 11:  # == is the equality condition
        break    # break is part of if, so it has to be indented 4 spaces under if
```
```
$ python3 break.py
1 hello
--TRUNCATED--
10 hello
```

### Continue
The 'continue' statement skips rest of the statements in the current iteration, and moves the loop forward to the next iteration.

Here is a code to find odd and even numbers between 1 and 11. 
When its an even it would continue to the next iteration skipping the processing of rest of the statements after 'continue'.
```
$ cat odd-or-even.py
i = 0
while True:
    i = i + 1
    if (i % 2 == 0):  # condition to check if its even
        print(i, 'even')
        continue # you will go forward with the rest of the loop and skip any statements below
    print(i, 'odd')
    if (i == 11):
```
$ python3 odd-or-even.py
1 odd
2 even
3 odd
4 even
5 odd
6 even
7 odd
8 even
9 odd
10 even
11 odd

## For
### in
The in statement is used with for, to loop over a list of values. Let's try this with the range function, which is used to return a range a numbers, except the last number, for example range(1, 11) actually ranges from 1 to 10. We could loop over this range.
```
$ cat range.py
for i in range(0, 10):   # it will count from 0 to 9, last number is excluded
    print(i)
```
```
$ python3 ex9.py
0
--TRUNCATED--
9
```

### nested
We can use nested blocks in python, same is true for 'for' as well. We are going to nest a for loop with in another for loop as follows.
```
$ cat nested-range.py
for i in range(1, 11):
     for j in range(11, 21):
          print(i, j)
```

```
$ python3 range.py
1 11
1 12
1 13
1 14
1 15
1 16
1 17
1 18
1 19
1 20
2 11
2 12
2 13
--TRUNCATED--
10 11
10 12
10 13
10 14
10 15
10 16
10 17
10 18
10 19
10 20
```

--end-of-post--