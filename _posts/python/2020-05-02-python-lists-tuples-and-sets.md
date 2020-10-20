---
title: python > lists, tuples, and sets
categories: python
---

A comparitive study of Lists, Tuples, and Sets should help in better understanding of these objects as they look kind 
of similar. Few prerequisites for this post, are that You should have Python3 on your system and you know how to 
access the Python interpreter or how to run Python scripts, and you have good understanding of fundamental data types 
such as Strings, Integers, and finally statements such as 'if', 'for' :)

### Ok let's first launch the Python interpreter
```
networkandcode: $ python3
Python 3.8.2 (default, Apr 27 2020, 15:53:34)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
```

### We are now to going to initialize and add content to three objects, one of each type
```
>>> sampleList = [ 'hey', 'hi', 'hello', 'hi', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar' ]
>>> sampleTuple = ( 'hey', 'hi', 'hello', 'hi', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar' )
>>> sampleSet = { 'hey', 'hi', 'hello', 'hi', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar' }
```

So, you got it, the first difference what we saw among these objects is the way the contents in them are enclosed. 
*Lists use Square brackets [], Tuples use parantheses (), Sets use curly braces{}*, however people call these
enclosing elements with different names.

### All good, let's ask Python to print the data types (or classes) of these objects
```
>>> print(type(sampleList))
<class 'list'>
>>> print(type(sampleTuple))
<class 'tuple'>
>>> print(type(sampleSet))
<class 'set'>
```
It shows we defined them correctly as 'list', 'tuple', and 'set'.

### We may print the content of these objects
```
>>> print(sampleList)
['hey', 'hi', 'hello', 'hi', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar']
>>> print(sampleTuple)
('hey', 'hi', 'hello', 'hi', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar')
>>> print(sampleSet)
{'hey', 4, 5, 'jaguar', 'banana', 'apple', 'hi', 'hello'}
```
Is there a difference in these contents than what we provided? Scrollup and analyse...

Well, List and Tuple objects are printed asis, however Set is not so, there are two worthy differences to note: 
1. The contents of the Set object are not in the same order like we gave 
2. The number of contents in Set are also reduced.
B
*This is because Sets are UnOrdered and Unique (means no Duplicate items), where are Lists and Tuples are ordered and 
not necessarily unique*

### Check the number of contents or length of these objects using 'len'
```
>>> print(len(sampleList))
11
>>> print(len(sampleTuple))
11
>>> print(len(sampleSet))
8
```
You may count the contents manually to check if your understanding is correct. Note that each item, each item adds 1 to the length of the overall object. 
So, the string 'banana' and the number 5 would both add 1 to the length of their respective data structure objects. What I mean by data structure is a List, Tuple, 
or Set as they store some collection of data. A Dictionary is also a Data Structure which we are not covering in this post.

### Try some indexing
Index starts from 0, until the length of the object minus 1. In our case, since the length of the List and Tuple is 11 each, the Index would range from 0 to 10.
Negative Indexing is also possible, where in the last item will be considered -1 and the first item -11, i.e. it ranges from -1 to -11 in reverse

*Note that Indexing works only with Lists and Tuples but not with Sets as they are unordered, i.e. each time when we print a Set we may see the items in it in some
 random order.*

#### Access the first item with positive and negative indexing
```
>>> print(sampleList[0], sampleList[-11])
hey hey
>>> print(sampleTuple[0], sampleTuple[-11])
hey hey
```

#### Access the last item likewise
```
>>> print(sampleList[10], sampleList[-1])
jaguar jaguar
>>> print(sampleTuple[10], sampleTuple[-1])
jaguar jaguar
```

#### Access the seventh item
```
>>> print(sampleList[6], sampleList[-5])
apple apple
>>> print(sampleTuple[6], sampleTuple[-5])
apple apple
```
*Math to convert positive to negative index: if i is the index, and l is the length, then i-l is the negative index
so if 6 is the index, 11 is the length, 6-11 = -5 is the negative index.*

### Using the index method
We can also check the index, based on a value being searched. Works with lists and tuples, but not sets, as sets are unordered. 
Note that when the value is repeated in more than one index, only the first index will be considered.
```
>>> print(sampleList.index('apple'))
6
>>> print(sampleTuple.index('apple'))
6
```

### Modify values

*We can only modify the existing value of item in List, using the index of the item. This isn't achievable with Sets / Tuple cause the former doesn't have index, and 
the later is immutable.*

Immutable means we can't modify it after its created.

#### Modify the 4th item of the list
```
>>> sampleList[3] = 'Hey There'
```

#### Print the List
```
>>> print(sampleList)
['hey', 'hi', 'hello', 'Hey There', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar']
```

So the fourth item is changed from 'hi' to 'Hey There'.

### Iterate and Print each item
Instead of printing the whole datastructure in a single line, we may iterate over the items of the list and print them, one item per line

#### Iterate over items of the List
```
>>> for i in sampleList:
...     print(i)
...
hey
hi
hello
Hey There
5
4
apple
5
banana
apple
jaguar
```

#### Iterate over items of the Tuple
```
>>> for i in sampleTuple: 
        print(i)
...
hey
hi
hello
hi
5
4
apple
5
banana
apple
jaguar
```

#### And finally the Set
```
>>> for i in sampleSet:
...     print(i)
...
hey
4
5
jaguar
banana
apple
hi
hello
```

So we have used the 'for' loop with our data structures to print its contents, well Indentation is very important in Python, else the program breaks, as a best 
practice please *ensure 4 spaces* for code in any block, so the 'for' block above, we have intended the next line of 'print' by 4 spaces.

### Use conditions

We can use 'If else' statements to check certain conditions such as to see if an item exists in the data structure.

#### Lets see if 'hi' exists in the List.
```
if 'hi' in sampleList:
    print ('yes')
else:
    print ('no')
````

#### 'Orange' in Tuple?
```
>>> if 'orange' in sampleTuple:
...     print('yes')
... else:
...     print('no')
...
no
```

#### Another condition in Set
```
>>>> if 'hey' in sampleSet:
    print ('yes')
else:
    print ('no')
```

You may explore this with various other conditions


### Add items
*We know Tuples are immutable and hence we can't add any items to it, we could do this with Lists and Sets in few ways.*
#### Append to List
The 'append' method, adds an item to the end of the List. Append is not applicable to Sets, also logically speaking there isn't any thing like a last item in the Set, 
as its unordered. If you try this with a Set, Python would throw an error like ```AttributeError: 'set' object has no attribute 'append'```
```
>>> sampleList.append('mango')
>>> print(sampleList)
['hey', 'hi', 'hello', 'Hey There', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar', 'mango']
```
So 'mango' now appears at the end of the list

#### Add to List using '+'
```
>>> list = ['apple', 'banana', 'orange']
>>> print(list)
['apple', 'banana', 'orange']
>>> list = list + ['grapes']
>>> print(list)
['apple', 'banana', 'orange', 'grapes']
>>>
>>> # list += is equivalent to list = list +
>>> list += ['pineapple', 'passion fruit']
>>> print(list)
['apple', 'banana', 'orange', 'grapes', 'pineapple', 'passion fruit']
>>>
>>> list = list * 3
>>>
>>> print(list)
['apple', 'banana', 'orange', 'grapes', 'pineapple', 'passion fruit', 'apple', 'banana', 'orange', 'grapes', 'pineapple', 'passion fruit', 'apple', 'banana', 'orange', 'grapes', 'pineapple', 'passion fruit']
```

#### Add to Set
'add' is applicable only to Sets, this adds an item to the Set, and there is no scope of positioning or indexing here
```
>>> sampleSet.add('mango')
>>> print(sampleSet)
{'hey', 4, 5, 'jaguar', 'banana', 'apple', 'hi', 'mango', 'hello'}
```
So 'mango' now is part of the Set

### Extend List
'extend' is used with Lists for adding multiple items at once.
```
>>> sampleList.extend(['friend', 'buddy', 'pal'])
>>> print(sampleList)
['hey', 'hi', 'hello', 'Hey There', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar', 'mango', 'friend', 'buddy', 'pal']
```
### Update Set
'update' is the corresponding method in Sets to add multiple items
```
>>> sampleSet.update(['friend', 'buddy', 'pal'])
>>> print(sampleSet)
{'hey', 'friend', 4, 5, 'jaguar', 'pal', 'banana', 'apple', 'hi', 'mango', 'hello', 'buddy'}
```
### Insert into List
'insert' is based on indexing, and hence only works with Lists. This is used to add an item based on the index.

```
>>> sampleList.insert(3, 'tango')
>>> print(sampleList)
['hey', 'hi', 'hello', 'tango', 'Hey There', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar', 'mango', 'friend', 'buddy', 'pal']
```
'tango' now appears at index 3 which is position 4, as index numbers start with 0


### Remove item
*Items can be removed from Lists and Sets, but not from Tuples as they are immutable*

#### Remove from List
If there are duplicates, only the *first occurence* will be deleted, we have to redo 'remove' to remove other occurences one at a time
```
>>> sampleList.remove('apple')
>>> print(sampleList)
['hey', 'hi', 'hello', 'tango', 'Hey There', 5, 4, 5, 'banana', 'apple', 'jaguar', 'mango', 'friend', 'buddy', 'pal']
>>>
```
#### Remove from Set
We can use 'remove' and 'discard' with sets
```	
>>> sampleSet.remove('apple')
>>> print(sampleSet)
{4, 5, 'mango', 'banana', 'hello', 'jaguar', 'hi', 'pal', 'hey', 'friend', 'buddy'}
```
'discard' can be used when we don't want Python to raise exceptions when the item is not present
Let's try to remove 'apple' again, 'remove' would throw an exception, where as 'discard' wont.
# discard item, only available in sets
# discard doesnt raise exception, remove does
```
>>> sampleSet.remove('apple')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'apple'

>>> sampleSet.discard('apple')
```
However, 'discard' would remove items if the item exists
```
>>> sampleSet.discard('hi')
>>> print(sampleSet)
{4, 5, 'mango', 'banana', 'hello', 'jaguar', 'pal', 'hey', 'friend', 'buddy'}
```
### Pop 
#### Without Index
*Wit out index, Pop can be used to remove the last item in a List or a random item from a Set, it wont work with Tuples as they are immutable*
```
>>> sampleList.pop()
>>> print(sampleList)
['hey', 'hi', 'hello', 'tango', 'Hey There', 5, 4, 5, 'banana', 'apple', 'jaguar', 'mango', 'friend', 'buddy']

```
It would remove a random item from Set, as it's unordered
```
>>> sampleSet.pop()
4
>>> print(sampleSet)
{5, 'mango', 'banana', 'hello', 'jaguar', 'pal', 'hey', 'friend', 'buddy'}
```

#### With Index
*This only works with Lists, as Sets are unordered*
Let's removing the item at index '2' which is the 3rd item from left
```
>>> sampleList.pop(2)
'hello'
>>> print(sampleList)
['hey', 'hi', 'tango', 'Hey There', 5, 4, 5, 'banana', 'apple', 'jaguar', 'mango', 'friend', 'buddy']
```

### Delete
There is lots of flexibility when its come to executing tasks in Python, however the choice is yours. 
*'del' is another way of removing items based on index from Lists, we know Tuples are immutable, and Sets do not support Indexing*
'del' doesn't return the value on screen though, like pop

To remove the item from index 5
```
>>> del sampleList[5]
>>> print(sampleList)
['hey', 'hi', 'tango', 'Hey There', 5, 5, 'banana', 'apple', 'jaguar', 'mango', 'friend', 'buddy']
```

### Remove all items
*We can remove all items with 'clear()', but we can't do any modifications to Tuples*
```
>>> sampleList.clear()
>>> sampleSet.clear()
```

If you try this with a Tuple, Python would raise an 'AttributeError' Exception
```
>>> sampleTuple.clear()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'clear'
```

### Delete the objects
This item we are going to finally delete the objects themselves, not the contents inside, hence, it will work with all 3 datastructures we were discussing
```
>>> del sampleList
>>> del sampleSet
>>> del sampleTuple
```
The objects no longer exist, Python raises 'NameError' Exception, if we try calling them
```
>>> print(sampleList)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'sampleList' is not defined

>>> print(sampleTuple)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'sampleTuple' is not defined

>>> print(sampleSet)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'sampleSet' is not defined
```
### Type casting
We can convert one object type another using keywords representing the object types such as list(), tuple(), set().
Let's create another group of objects for this purpose

```
>>> alternateList = ['hey', 'hi', 'hello', 'hi', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar']
>>> alternateTuple = ('hey', 'hi', 'hello', 'hi', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar')
>>> alternateSet = {'hey', 'hi', 'hello', 'hi', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar'}
```

We can try different combinations for conversion such as list to tuple, tuple to set, list to set
```
>>> print( tuple (alternateList) )
('hey', 'hi', 'hello', 'hi', 5, 4, 'apple', 5, 'banana', 'apple', 'jaguar')

>>> print( set (alternateTuple) )
{4, 5, 'banana', 'apple', 'hello', 'hi', 'jaguar', 'hey'}

>>> print( list (alternateSet) )
[4, 5, 'banana', 'apple', 'hello', 'hi', 'jaguar', 'hey']
```

### Creating empty objects
We can initialize re re-initalize empty objects as follows
```
>>> alternateList = []
>>> alternateTuple = ()
```

There is a slight difference with Sets, as both Sets and Dictionaries(we have not seen in this post) use curly braces
so if you do ```alternateSet = {}``` that would rather create an empty Dictionary
```
>>> print(type(alternateSet))
<class 'dict'>
```

So the right way to create an empty set is:
```
>>> alternateSet =  set()
>>> print(type(alternateSet))
<class 'set'>
```

### Max, Min
We can find the smallest and highest number in a list, tuple, or set using the functions min and max.
```
>>> # numbers
>>> print(max(1, 100, 3))
100
>>> print(min(1, 100, 3))
1
>>>
>>> list = [1, 100, 3]
>>> tuple = (1, 100, 3)
>>> set = {1, 100, 3}
>>>
>>> print(max(list))
100
>>> print(max(tuple))
100
>>> print(max(set))
100
>>> print(min(list))
1
>>> print(min(tuple))
1
>>> print(min(set))
1
```

### Sort
We can sort items in ascending or descending order, however all the items should belong to the same datatype. 
We can sort a list, tuple, or set, however the result is a list.
```
>>> list = ['apple', 'orange', 'banana', 'grapes', 'passion fruit']
>>> tuple = ('apple', 'orange', 'banana', 'grapes', 'passion fruit')
>>> set = {'apple', 'orange', 'banana', 'grapes', 'passion fruit'}
```
### Ascending order
```
>>> print(sorted(list))
['apple', 'banana', 'grapes', 'orange', 'passion fruit']
>>> print(sorted(tuple))
['apple', 'banana', 'grapes', 'orange', 'passion fruit']
>>> print(sorted(set))
['apple', 'banana', 'grapes', 'orange', 'passion fruit']
```
### Descending order
```
>>> print(sorted(list, reverse=True))
['passion fruit', 'orange', 'grapes', 'banana', 'apple']
>>> print(sorted(tuple, reverse=True))
['passion fruit', 'orange', 'grapes', 'banana', 'apple']
>>> print(sorted(set, reverse=True))
['passion fruit', 'orange', 'grapes', 'banana', 'apple']
```

### Reverse
This is only applicable to a list, as tuples are immutable and sets are unordered.
```
>>> list.reverse() # the original list gets changed
>>> print(list)
['passion fruit', 'grapes', 'banana', 'orange', 'apple']
```

### Sum
Sum is a built in function.
```
>>> print(type(sum))
<class 'builtin_function_or_method'>
```

It's used to find the sum of all numbers in a list, tuple, or set.
```
>>> li = [ 1024, 2048, 1, 2, 3, 10 ]
>>> tu = ( 1024, 2048, 1, 2, 3, 10 )
>>> se = { 1024, 2048, 1, 2, 3, 10 }
>>> print(sum(li))
3088
>>> print(sum(tu))
3088
>>> print(sum(se))
3088
```

### Any
It's a built in function, used to find if anyone of the items in a list, tuple, or set is true(boolean).
Note that Values such as 0, False, None, '' are considered False.
```
>>> li = [ 0, False, None, '' ]
>>> tu = ( 0, False, None, '' )
>>> se = { 0, False, None, '' }
```
It should return False, as there is no single True value. All values except those are False would be True, such as integer, string, a Boolean True and so on.
```
>>> print(any(li))
False
>>> print(any(tu))
False
>>> print(any(se))
False
```
We are going to add a True value to each of the variables.
```
>>> li = [ 0, False, None, '', 3 ]
>>> tu = ( 0, False, None, '', 'hello' )
>>> se = { 0, False, None, '', True }
```
The 'any' function should now true for all 3 cause, The integer 3 is True, The string 'hello' is True, and the boolean True is True anyway.
```
>>> print(any(li))
True
>>> print(any(tu))
True
>>> print(any(se))
True
```

### All
This function helps to check if all the values in a list, tuple, and set are True.
```
>>> li = [ True, 100, 3.3 ]
>>> tu = ( True, 100, 'hi' )
>>> se = { True, 100, 1 }
```
We should get True as expected.
```
>>> print(all(li))
True
>>> print(all(tu))
True
>>> print(all(se))
True
```

Let's modify things slightly so that we get False.
```
>>> li = [ True, 100, 3.3, False ]
>>> tu = ( True, 100, 3.3, 0 )
>>> se = { True, 100, 3.3, '' }
```
We should now get False, due to the last element False, 0, and '' added to each object.
```
>>> print(all(li))
False
>>> print(all(tu))
False
>>> print(all(se))
False
```

### Comprehension
We can generate lists with a single line statament, this is like a shortcut for multline loop blocks.
Let' say we have a list of numbers.
```
list = [1, 2, 3]
```
Usually, to find the square of these numbers, we would do something like the following.
```
>>> for i in list:
...     print(i * i)
...
1
4
9
```

With list comprehension, its even more easy.
```
>>> # comprehension
>>> iSquare = [ i * i for i in list ]
>>> print(iSquare)
[1, 4, 9]
```

We can extend the logic for nested lists as well. Let's try with an example to find the common items in two lists.
```
>>> list1 = [ 10, 20, 30, 40 ]
>>> list2 = [ 20, 30, 40, 50]
>>> # comprehension
>>> commonItems = [ i for i in list1 for  j in list2 if i == j ]
>>> print(commonItems)
[20, 30, 40]
>>> commonItems = [ j for i in list1 for  j in list2 if i == j ]
>>> print(commonItems)
[20, 30, 40]
```
An alternate way to do this using for loop would be as follows. However we need to have some extra logic to make the resulting numbers part of a new list.
```
>>> for i in list1:
...     for j in list2:
...          if i == j:
...              print(i)
...
20
30
40
```

### Quiz
Well, some recap to refresh what you have learnt
- Is Tuple ordered or unordered
- Which of the datastructures we have seen in the post, contains Unique items
- Do 'del' and 'pop' both return a value back on screen
- What Exception would you see if you try to clear items from an existing Tuple
- You are trying to print an object that doesn't even exist, what Exception would Python throw
- How would you create an empty set

--end-of-post--
