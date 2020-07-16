---
title: python > classes and instances
categories: python
...

We are going to see some object oriented programming here. 
Its nice to have some fundamental understanding of Python functions or methods, datatypes for better understanding of this post.

Everything we define in Python is an object. 
They are objects as they have their set of attributes and methods. 
There are built in classes such as 'str', 'list', etc. and we can also create user defined classes.

### Built in classes
Let's create string variable with name text
```
>>> text = 'Hello World!'
```
As said, everything is an object, so here if the text is the object name, 
the object type would be string or 'str' to be specific. Note that we can also say text is an instance of the str class.
```
>>> print(type(text))
<class 'str'>
```

### Create an instance
The actual format for creating an instance, would be instanceObjectName = classObjectName(optionalArguments). 
We haven't followed this method in the previous case. We can redo it now as follows.
```
>>> text = str('Hello World!')

>>> print(text)
Hello World!
>>> print(type(text))
<class 'str'>
```
So to be clear, if text is the instanceObjectName, str is the classObjectName, and 'Hello World!' is the argument.

### User defined class
Let's define our own class, note that it's common to use capitalized names for user defined classes. 
The keyword or statement 'class' is used to create a class as follows
```
class Furniture():
    color = 'Brown'  # class attributes
    weight = '10Kg'
    def __init__(self):
        self.length = '1m'  # instance attributes
        self.width = '3m'
        self.height = '5m'
        self.material = 'Teak'
        self.color = 'Black'  # instance attribute wil be preferred
```
#### Class Attributes
So we define a class with the name 'Furniture' above, and gave it two attributes color and weight. 
We should be able to access these attributes now, but with out typing ```()``` after the class name
```
>>> Furniture.color
'Brown'
>>> Furniture.weight
'10Kg'
```
Note that if you include ```()```, that would actually refer to the instance of the class and not the class.

#### Init and Instance Attributes
Whats the __init__ all about, its a special method in the class, that gets called when an instance of the class is being created, 
recall that the format for creating an instance is ```instanceObjectName = classObjectName(arguments)```. So lets create an instance.
```
chair = Furniture()  # creating an instance
```
So we are creating an instance object called ```chair```. 
When an instance gets created it first inherits all the class attributes that we saw earlier, i.e. color and weight, 
and then it triggers the __init__ method, but without any arguments. 
Note that even when there is no argument, the __init__ would still consider one argument which is the name of the instance itself. 
So the instance name gets mapped with the parameter 'self' which is the first parameter of the __init__ method. 
Now the code inside __init__ gets executed, where ever you see 'self' just replace that with your instance name i.e. chair. 

So, now, we can access the instance attributes.
```
>>> print(chair.length, chair.width, chair.height, chair.material, chair.weight)  # instance attributes
1m 3m 5m Teak 10Kg
```
If you revisit the code, there isnt anything like self.weight in __init__, but we were still able to print ```chair.weight``` 
cause it got that attribute from the class itself.

Next if you try printing the color attribute, you would get 'Black' even though the same attribute was defined directly under the class, 
this is because if attribute exists in both class and instance level, the instance level will be preferred as its more specific
```
>>> print(chair.color)
Black
```
Note that an instance can access a class attribute but a class cannot access the instance attribute, to be clear if Furniture is the class, 
Furniture() would be the instance, the 'parantheses' makes the difference. 
For example, the attribute 'material' is an instance attribute, and couldn't be accessed directly from the class, 
and would throw an exception error of type 'AttributeError'
```
>>> print(Furniture.material) # class attribute only, AttributeError: type object 'Furniture' has no attribute 'material'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: type object 'Furniture' has no attribute 'material'
```
--end-of-post--
