---
title: python > regular expressions
categories: python
---

Let's learn some bits of regular expression here, hope you are already familiar with strings in Python.

Regular expressions are a powerful way of pattern matching in a given string. The 're' module should be imported first to used regular expressions in Python.

We are importing 're' and then define a multiline string.
```
>>> import re
>>>
>>> multilineString = '''
... America
... Australia
... 1800-123-345
... 192.168.1.100
... India
... Asia
... Newzealand
... Ahmed
... United kingdom
... dummy@email.com
... Pakistan
... Zimbabwe
... 10.0.0.1
... me@myself.com
... India
... 1800-300-102
... Korea
... China
... Ahmed
... Shakir
... hi_there
... Aa
... '''
>>>
```

A regular expression is prefixed by 'r', lets define one
```
>>> pattern = r'Ahmed'
```
So here, the variable pattern is a regular expression.

We can use the findall method to find all the occurences of pattern, in the multlineString.
```
>>> print(re.findall(pattern, multilineString))  # List
['Ahmed', 'Ahmed']
```
We may also directly define a pattern instead of assigning it to a variable, and then search.
```
>>> print(re.findall(r'Shakir', multilineString))  # List
['Shakir']
>>> print(re.findall(r'k', multilineString))  # List
['k', 'k', 'k']
>>> print(re.findall(r'Africa', multilineString))  # List
[]
>>>
```
\w referes to digits 0-9, alphabets a-z, A-Z, and underscore(_). In the following example we are only finding one occurence of \w.
```
>>> # \w [0-9a-zA-Z_]
>>> print(re.findall(r'\w', multilineString))
['A', 'm', 'e', 'r', 'i', 'c', 'a', 'A', 'u', 's', 't', 'r', 'a', 'l', 'i', 'a', '1', '8', '0', '0', '1', '2', '3', '3', '4', '5', '1', '9', '2', '1', '6', '8', '1', '1', '0', '0', 'I', 'n', 'd', 'i', 'a', 'A', 's', 'i', 'a', 'N', 'e', 'w', 'z', 'e', 'a', 'l', 'a', 'n', 'd', 'A', 'h', 'm', 'e', 'd', 'U', 'n', 'i', 't', 'e', 'd', 'k', 'i', 'n', 'g', 'd', 'o', 'm', 'd', 'u', 'm', 'm', 'y', 'e', 'm', 'a', 'i', 'l', 'c', 'o', 'm', 'P', 'a', 'k', 'i', 's', 't', 'a', 'n', 'Z', 'i', 'm', 'b', 'a', 'b', 'w', 'e', '1', '0', '0', '0', '1', 'm', 'e', 'm', 'y', 's', 'e', 'l', 'f', 'c', 'o', 'm', 'I', 'n', 'd', 'i', 'a', '1', '8', '0', '0', '3', '0', '0', '1', '0', '2', 'K', 'o', 'r', 'e', 'a', 'C', 'h', 'i', 'n', 'a', 'A', 'h', 'm', 'e', 'd', 'S', 'h', 'a', 'k', 'i', 'r', 'h', 'i', '_', 't', 'h', 'e', 'r', 'e', 'A', 'a']
```
Let's now try to find four occurences of \w, so we get four character alphanumerics(including underscore as well).
```
>>> print(re.findall(r'\w\w\w\w', multilineString))
['Amer', 'Aust', 'rali', '1800', 'Indi', 'Asia', 'Newz', 'eala', 'Ahme', 'Unit', 'king', 'dumm', 'emai', 'Paki', 'stan', 'Zimb', 'abwe', 'myse', 'Indi', '1800', 'Kore', 'Chin', 'Ahme', 'Shak', 'hi_t', 'here']
>>>
```
\d stands for numbers 0-9
```
>>> # \d [0-9]
>>> print(re.findall(r'\d', multilineString))
['1', '8', '0', '0', '1', '2', '3', '3', '4', '5', '1', '9', '2', '1', '6', '8', '1', '1', '0', '0', '1', '0', '0', '0', '1', '1', '8', '0', '0', '3', '0', '0', '1', '0', '2']
>>> print(re.findall(r'\d\d\d\d-\d\d\d-\d\d\d', multilineString))
['1800-123-345', '1800-300-102']
```
Few examples with special symobls '\.', '+', '*'
```
>>> # + more than one occurence
>>> # \. refers to '.' char
>>> print(re.findall(r'\d+\.\d+\.\d+\.\d+', multilineString))
['192.168.1.100', '10.0.0.1']
>>>
>>> print(re.findall(r'A\w+a', multilineString))
['America', 'Australia', 'Asia']
>>> # * refers to 0 or more occurence
>>> print(re.findall(r'A\w*a', multilineString))
['America', 'Australia', 'Asia', 'Aa']
>>>
>>> print(re.findall('\w+@\w+\.\w+', multilineString))
['dummy@email.com', 'me@myself.com']
>>> 
```

--end-of-post--