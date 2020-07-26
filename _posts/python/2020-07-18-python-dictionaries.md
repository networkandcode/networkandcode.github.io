---
title: python > dictionaries
categories: python
---
Dictionaries are datastructure objects that can store information in a key value pair format, in this post, we will explore some information about 
dictionaries and their associated methods. The prerequisites are knowledge of boolean, exceptions, float, integers, methods, strings, etc.

### Define a Dictionary
We are going to import the datetime module first, and then create a dictionary.
```
# datetime module in datetime package is required to create datetime objects
from datetime import datetime

# we create a dictionary
dictionary1 = {
    'mainVersion': 3.8,
    'releaseVersion': '3.8.3',

    # strftime is optional and is used to print the date in desired format
    # strtime converts datetime object into string
    # %b for short version of month, % d for date, %Y for full version of year
    'releaseDate': datetime(2020, 5, 13).strftime('%b %d, %Y')
}
```
The dictionary has 3 items in it, each with a key and a value. The keys are 'mainVersion', 'releaseVersion' and 'releaseDate' and the correspoding 
values are written after the ':'. The 3rd value is a datetime object, which is used to print a date in specified format as mentioned by 
the strftime method. 

We may now print the dictionary, see it's data type, and view the contents of the 'dict' class.
```
print(dictionary1)
print(type(dictionary1))
print('All the attributes and methods of the dict class')
print(dir(dict))
print('-' * 50)
```
output:
```
{'mainVersion': 3.8, 'releaseVersion': '3.8.3', 'releaseDate': 'May 13, 2020'}
<class 'dict'>
All the attributes and methods of the dict class
['__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
--------------------------------------------------
```

### Update
#### using update method
The update method can be used to update the dictionary. Let's add few more entries.
```
print('update dictionary')
dictionary1.update ({
    'language' : 'Python',
    'designer': 'Guido Van Rossum',
    'extrakey': 'extravalue',
    'features': ['Interpreted', 'High level'],
    'dummykey': 'dummyvalue'
})
print(dictionary1)
print('-' * 50)
```

output:
```
update dictionary
{'mainVersion': 3.8, 'releaseVersion': '3.8.3', 'releaseDate': 'May 13, 2020', 'language': 'Python', 'designer': 'Guido Van Rossum', 'extrakey': 'extravalue', 'features': ['Interpreted', 'High level'], 'dummykey': 'dummyvalue'}
--------------------------------------------------
```
#### using the key directly
This method is more easy, we could directly add or modify a key as follows.
```
print('update or modify dictionary using key')                                                                                                       # new key and value
dictionary1['developer'] = 'Python software foundation'
# modify existing key's value
dictionary1['extrakey'] = 'EXTRA Value'
print(dictionary1)
print('-' * 50)
```

output:
```
update or modify dictionary using key
{'mainVersion': 3.8, 'releaseVersion': '3.8.3', 'releaseDate': 'May 13, 2020', 'language': 'Python', 'designer': 'Guido Van Rossum', 'extrakey': 'EXTRA Value', 'features': ['Interpreted', 'High level'], 'dummykey': 'dummyvalue', 'developer': 'Python software foundation'}
-------------------------
```

### pop
We can remove a key and values using the pop method.
```
print('pop from dictionary')
poppedValue = dictionary1.pop('extrakey')
print(poppedValue)
print(dictionary1)
print('-' * 25)
# if a key is not found, pop() can return a default value
poppedValue = dictionary1.pop('extrakey', 'no value popped')
print(poppedValue)
print(dictionary1)
print('-' * 50)
```

output:
```
pop from dictionary
EXTRA Value
{'mainVersion': 3.8, 'releaseVersion': '3.8.3', 'releaseDate': 'May 13, 2020', 'language': 'Python', 'designer': 'Guido Van Rossum', 'features': ['Interpreted', 'High level'], 'dummykey': 'dummyvalue', 'developer': 'Python software foundation'}
-------------------------
no value popped
{'mainVersion': 3.8, 'releaseVersion': '3.8.3', 'releaseDate': 'May 13, 2020', 'language': 'Python', 'designer': 'Guido Van Rossum', 'features': ['Interpreted', 'High level'], 'dummykey': 'dummyvalue', 'developer': 'Python software foundation'}
--------------------------------------------------
```

### Length
```
print('Get the length of dictionary')
# prints the no. of keys
print(len(dictionary1))
print('-' * 50)
```

output:
```
Get the length of dictionary
8
--------------------------------------------------
```

### Check for a key
We can use the 'in' statement to check if a key exists in a dictionary. The result will be a boolean, either True or False.
```
print('To check if a specific key exists in the dictionary')
# prints True or False
print('mainVersion' in dictionary1)
print('MainVersion' in dictionary1)
print('-' * 50)
```

output:
```
To check if a specific key exists in the dictionary
True
False
--------------------------------------------------
```

### Check for Keys, Values
```
>>> shirt = {
... 'Brand': 'Louis Philippe',
... 'Size': '40',
... 'Color': 'White'
... }
>>>
>>> # check for a particular key
>>> if 'Brand' in shirt:
...     print('yes')
... else:
...     print('no')
...
yes
>>> if 'Model' in shirt:
...     print('yes, model is there')
... else:
...     print('no, model is not there')
...
no, model is not there
>>> # check for a particular value
>>> print(shirt.values())
dict_values(['Louis Philippe', '40', 'White'])
>>>
>>> if 'White' in shirt.values():
...     print('yes its a white shirt')
... else:
...     print('no, its not white')
...
yes its a white shirt
>>> if 'Black' in shirt.values():
...     print('yes, its black')
... else:
...     print('no, its not black')
...
no, its not black
>>>
```

### Loop

#### Iterate over keys
We can iterate over a dictionary's keys using the 'for' statement. And we can retrieve the value of each key either directly calling the key as 
index or by using the get method.
```
print("To iterate over the dictionary's keys")
for key in dictionary1:
    print('-' * 25)
    print(type(key))
    print(key)
    print('---')
    # retrieve the value of the key
    value = dictionary1[key]
    print(type(value))
    print(value)
    print('---')
    # retrieve the value of key in an alernate way
    value = dictionary1.get(key)
    print(type(value))
    print(value)

print('-' * 50)
```

output:
```
To iterate over the dictionary's keys
-------------------------
<class 'str'>
mainVersion
---
<class 'float'>
3.8
---
<class 'float'>
3.8
-------------------------
<class 'str'>
releaseVersion
---
<class 'str'>
3.8.3
---
<class 'str'>
3.8.3
-------------------------
<class 'str'>
releaseDate
---
<class 'str'>
May 13, 2020
---
<class 'str'>
May 13, 2020
-------------------------
<class 'str'>
language
---
<class 'str'>
Python
---
<class 'str'>
Python
-------------------------
<class 'str'>
designer
---
<class 'str'>
Guido Van Rossum
---
<class 'str'>
Guido Van Rossum
-------------------------
<class 'str'>
features
---
<class 'list'>
['Interpreted', 'High level']
---
<class 'list'>
['Interpreted', 'High level']
-------------------------
<class 'str'>
dummykey
---
<class 'str'>
dummyvalue
---
<class 'str'>
dummyvalue
-------------------------
<class 'str'>
developer
---
<class 'str'>
Python software foundation
---
<class 'str'>
Python software foundation
--------------------------------------------------
```

#### Iterate over both keys and values
The items method could be used to refer to both keys and values.
```
print("To iterate over both keys and values")
for key, value in dictionary1.items():
    print('-' * 25)
    print(key, value)

print('-' * 50)
```

output:
```
To iterate over both keys and values
-------------------------
mainVersion 3.8
-------------------------
releaseVersion 3.8.3
-------------------------
releaseDate May 13, 2020
-------------------------
language Python
-------------------------
designer Guido Van Rossum
-------------------------
features ['Interpreted', 'High level']
-------------------------
dummykey dummyvalue
-------------------------
developer Python software foundation
--------------------------------------------------
```

#### Iterate over values
Or we can just iterate over values with the values method.
```
print("To iterate over values")
for value in dictionary1.values():
    print(value)

print('-' * 50)
```

output:
```
To iterate over values
3.8
3.8.3
May 13, 2020
Python
Guido Van Rossum
['Interpreted', 'High level']
dummyvalue
Python software foundation
--------------------------------------------------
```

### Same value dictionary
If the values for a set of keys are same, the fromkeys method could used to create those entries quickly.
```
print('Create a dictionary with different keys, same value, using fromkeys()')
keys = ('color', 'fruit', 'company', 'extrakey')
value = 'Orange'
# we can initialize a dictionary and use fromkeys method it
dictionary2 = {}
dictionary2 = dictionary2.fromkeys(keys, value)
print(dictionary2)
# we can also use fromkeys() as a direct dict class method
dictionary3 = dict.fromkeys(keys, value)
print(dictionary3)

print('-' * 50)
```

output:
```
Create a dictionary with different keys, same value, using fromkeys()
{'color': 'Orange', 'fruit': 'Orange', 'company': 'Orange', 'extrakey': 'Orange'}
{'color': 'Orange', 'fruit': 'Orange', 'company': 'Orange', 'extrakey': 'Orange'}
--------------------------------------------------
```

### Clear
We can clear a specific key's value, by just setting it to an empty string.
```
print("clear a particular key's value")
dictionary1['dummykey'] = ''
print(dictionary1)
# using ''
dictionary2['extrakey'] = ''
print(dictionary2)

print('-' * 50)
```

output:
```
clear a particular key's value
{'mainVersion': 3.8, 'releaseVersion': '3.8.3', 'releaseDate': 'May 13, 2020', 'language': 'Python', 'designer': 'Guido Van Rossum', 'features': ['I>{'color': 'Orange', 'fruit': 'Orange', 'company': 'Orange', 'extrakey': ''}
--------------------------------------------------
```

### Copy
The copy method can be used to copy a dictionary.
```
print('copy dictionary')
dict1Copy = dictionary1.copy()
print(dict1Copy)
print('-' * 50)
```

output:
```
copy dictionary
{'mainVersion': 3.8, 'releaseVersion': '3.8.3', 'releaseDate': 'May 13, 2020', 'language': 'Python', 'designer': 'Guido Van Rossum', 'features': ['I>--------------------------------------------------
```

### Empty
```
print('Empty the dictionary')
# using clear()
dictionary1.clear()
# or using {}
dictionary2, dictionary3 = {}, {}

print(dictionary1, dictionary2, dictionary3)
print('-' * 50)
```

output:
```
Empty the dictionary
{} {} {}
--------------------------------------------------
```

### Delete
We can delete the objects completely using 'del' statement.
```
print('Delete the dictionary variables')

del dictionary1
del dictionary2
del dictionary3
del dict1Copy

for i in 'dictionary1', 'dictionary2', 'dictionary3':
    try:
        # eval is used to see if a variable exists with the given name
        eval(i)
    except NameError as n:
        print(n)
print('-' * 50)
```

output:
```
Delete the dictionary variables
name 'dictionary1' is not defined
name 'dictionary2' is not defined
name 'dictionary3' is not defined
--------------------------------------------------
```

### Nested dictinoary
A dictionary can also have a sub dictionary inside it.
#### Initialize and check length
```
# nested dictionary

mydetails = {
    'name': 'Peter',
    'surname': 'England',
    'address': {
        'door' : '23',
        'postcode' : '100098',
        'street no': '35',
        'county' : 'Berkshire'
    }
}


# its only 3 coz it has 3 keys - name, surname, and address
print(len(mydetails))
```

output:
```
3
```
#### Access the values of keys
The values of a sub key can also be accesses by calling the sub key appropriately.
```
print(mydetails['address'])
print(mydetails['address']['county'])
print(mydetails['address']['postcode'])
```

output:
```
{'door': '23', 'postcode': '100098', 'street no': '35', 'county': 'Berkshire'}
Berkshire
100098
```

#### Delete this dictionary
```
del mydetails
```

### dict class
We can also create a dictionary using the dict class, this method refers to creating an instance of a class, 
as however it belongs to the 'dict' class.
```
# alternate way of creating a dictionary
# no quotes in keys
# use parantheses
# use the dict keyword
shirt = dict(
Brand = 'Louis Philippe',
Size = '40',
Color = 'White'
)

print(shirt)
del shirt
```

output:
```
{'Brand': 'Louis Philippe', 'Size': '40', 'Color': 'White'}
```
### Another example
One more example for practice.
```
$ cat phone-dictionary.py
emptyDictionary = {}
print(type(emptyDictionary))

sampleDictionary = {
'model': 'iphone7',
'manufacturer': 'apple',
'color': 'space grey'
}

print(type(sampleDictionary))
print(sampleDictionary)

print(sampleDictionary['model'])
print(sampleDictionary['manufacturer'])
print(sampleDictionary['color'])

# change the color to rose gold
sampleDictionary['color'] = 'rose gold'

print(sampleDictionary['color'])
```

```
$ python3 phone-dictionary.py
<class 'dict'>
<class 'dict'>
{'model': 'iphone7', 'manufacturer': 'apple', 'color': 'space grey'}
iphone7
apple
space grey
rose gold
```


--end-of-post--




