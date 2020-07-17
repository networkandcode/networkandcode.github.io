---
title: python > classes and instances
categories: python
...

We are going to see some object oriented programming here. 
Its nice to have fundamental understanding of Python functions or methods, datatypes for better understanding of this post.

Python is an object oriented programming langugage like many other languages today. 
Everything we define in Python is an object. 
They are objects as they have their set of attributes and methods. 

There are built in classes such as 'str', 'list', etc. and we can also create user defined classes. 
An object, when created would become an instance of a class under which it's being created. 
So if we create a string object, it means we are actually creating an instance of string class 'str'. 

For that matter a class is also an object technically, cause it can be accessed with its attributes and methods too. 
But its most common to call the instance of the class, as an object, and the class as just class. 
To be more specific, everything is an object, no matter its a function, class, or an instance of a class.

### Built in classes
Let's create a string variable with name text
```
>>> text = 'Hello World!'
```
As said, everything is an object, so here if the text is the object name, 
the object type would be string or 'str' to be specific. Note that we can also say text is an instance of the str class.
```
>>> print(type(text))
<class 'str'>
```

Let's create a string object
```
>>> text = 'Hello World!'
```
So we created a string object and gave the object name ```text```. If we try accessing the type of this object, it says it belongs to 'str' which is a built in class in Python
```
>>> print(type(text))
<class 'str'>
```
However the class ```str``` also belongs to a different built in class called ```type```
```
>>> print(type(str))
<class 'type'>
```
Similarly, other built in classes such as ```list, set, tuple, dict``` all belong to the class ```type```
```
>>> print(type(int))
<class 'type'>
>>> print(type(list))
<class 'type'>
>>> print(type(tuple))
<class 'type'>
>>> print(type(set))
<class 'type'>
>>> print(type(dict))
<class 'type'>
```

Well, if we try to further access the class of type of 'type' itself, we just get 'type' which means, it doesnt have any base class above it.
```
>>> print(type(type))
<class 'type'>
```

Likewise we can also check the class of functions too
```
>>> print(type(print))
<class 'builtin_function_or_method'>
>>>
>>> print(type(dir))
<class 'builtin_function_or_method'>
```
The above snippet shows the function objects print and dir belong to the class 'builtin_function_or_method'

### Contents of an object
The 'dir' function is used to retrieve the contents of an object, i.e. the list of its attributes and methods, 
let's check the contents of the 'type' class
```
>>> print(dir(type))
['__abstractmethods__', '__base__', '__bases__', '__basicsize__', '__call__', '__class__', '__delattr__', '__dict__', '__dictoffset__', '__dir__', '__doc__', '__eq__', '__flags__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__instancecheck__', '__itemsize__', '__le__', '__lt__', '__module__', '__mro__', '__name__', '__ne__', '__new__', '__prepare__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasscheck__', '__subclasses__', '__subclasshook__', '__text_signature__', '__weakrefoffset__', 'mro']
```
And now, lets  check the contents of the 'str' class
```
>>> print(dir(str))
['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
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
So we defined a class with the name 'Furniture' above, and gave it two attributes color and weight. 
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

### Other built in methods
Let's create a class with name Rectangle, and we are going to define a user defined method called area and additional built in methods such as 
__str__, __add__, and __del__
```
class Rectangle():
    'This is a class for rectange objects'    # can output this with __doc__
    # has to be at the very first line

    # unit and name are class attributes
    unit = 'sq.cm'  # this becomes self.unit
    name = 'rectangle'

    # __init__ is a constructor
    def __init__(self, length, breadth):
        self.length = length
        self.breadth = breadth
        self.unit = 'sq.m'  # takes precedence
        print(self.name)
    def area(self):
        self.area = self.length * self.breadth
        return(str(self.area) + self.unit)

    def __str__(self):
        return ("Hello this gets printed, when you print the object, this rectangle's area is %s sq.m" %(self.area))

    # to define addition of two instances of a class
    def __add__(self, other):
        totalLength =  self.length + other.length
        totalBreadth = self.breadth + other.breadth
        print(totalLength, totalBreadth)

    # destructor method of the class, called when the class is about to get destroyed
    def __del__(self):
        print('end of class')
```

An instance can created from this class
```
rectangle1 = Rectangle(2, 10)
```
output: *rectangle*

Let's check the contents of the Class and Instance
```
print(dir(Reactangle))
```
output: *['__add__', '__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'area', 'name', 'unit']*
```
print(dir(reactangle1))
```
output: *['__add__', '__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'area', 'breadth', 'length', 'name', 'unit']*

We could now access the instance attributes and methods
```
print(rectangle1.unit)
```
output: *sq.m*

```
print(rectangle1.area())
```
output: *20sq.m*
```
print(rectangle1.name)
```
output: *rectangle*


And let's access few built in methods
```
print(Rectangle.__doc__)
```
output: *This is a class for rectange objects*

```
print(rectangle1.__doc__)
```
output: *This is a class for rectange objects*

```
# works only with class
print(Rectangle.__name__)
```
output: *Rectangle*
```

```
print(Rectangle.__module__)  # name of the module in which the class is defined
print(rectangle1.__module__)
```
output: *
__main__
__main__
*

```
# works only with class
print(Rectangle.__bases__)  # base classes of the class
```
output: *(<class 'object'>,)*

```
# dictionary holding the class namespace
print(Rectangle.__dict__)
print('~' * 25 )
print(rectangle1.__dict__)

print(rectangle1)  # calls the __str__ method of the class

rectangle2 = Rectangle(1, 3)

print(rectangle1 + rectangle2)

```
output:
```
{'__module__': '__main__', '__doc__': 'This is a class for rectange objects', 'unit': 'sq.cm', 'name': 'rectangle', '__init__': <function Rectangle.__init__ at 0x7f68cdb25f70>, 'area': <function Rectangle.area at 0x7f68cdb30040>, '__str__': <function Rectangle.__str__ at 0x7f68cdb300d0>, '__add__': <function Rectangle.__add__ at 0x7f68cdb30160>, '__del__': <function Rectangle.__del__ at 0x7f68cdb301f0>, '__dict__': <attribute '__dict__' of 'Rectangle' objects>, '__weakref__': <attribute '__weakref__' of 'Rectangle' objects>}
~~~~~~~~~~~~~~~~~~~~~~~~~
{'length': 2, 'breadth': 10, 'unit': 'sq.m', 'area': 20}
Hello this gets printed, when you print the object, this rectangle's area is 20 sq.m
rectangle
3 13
None
end of class
end of class
```

### Class Inheritance
We are gonna see some multiple inheritance examples. Multiple inheritance means we can create multiple derived classes from the same base class. 
We can first create base / parent classes and then create sub classes under them
```
# Parent or Base class
# The first letter of a class name is usually in capital
class Person():
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName
    def print(self):
        print(self.firstName, self.lastName)
```
We can now create an instance in this base class
```
# create object in Base class
personName = Person('James', 'Watson')
# This print is different from the usual print function
# as it comes after '.'
personName.print()
```
output: *James Watson*

We are now going to create a Derived class that should inherit properties from the base class
```
# Child or Derived class
# Inherits properties and methods from Base class
class Employee(Person):
    pass  #  pass used when we don't to add any extra properties or methods to this class
```
This is just a derived class with no unique properties, it inherits everything from the base class. 
Subsequently, we would create an instance under the derived class
```
# create object in Dervied class
employeeName = Employee('Michael', 'Jones')
employeeName.print()
```
output: *Michael Jones*

Let's create another derived class, but with the __init__ method. 
And, also an instance under this new derived class.
```
# create another derived class with __init__
class Engineer(Person):
    def __init__(self, firstName, lastName):
        # for inheritance, we need to call the __init__ method of base class
        Person.__init__(self, firstName, lastName)

engineerName = Engineer('Clark', 'Peters')
engineerName.print()
```
output: *Clark Peters*

So in the snippet above, we have initialized the base class, by calling the __init__ method of the base class.

Let's try one other derive class, but this time we would use the super() function to call the base call. 
```
# An alternative way is use the super() function instead of the Class name
class Pilot(Person):
    def __init__(self, firstName, lastName):
        # We use super() this time for inheritance
        # and there is no need for self inside __init__ when we use super()
        super().__init__(firstName, lastName)

pilotName = Pilot('Steven', 'Williams')
pilotName.print()
```
output: *Steven Williams*

Let's create a derived class and add an extra property to it
```
class Chauffeur(Person):
    def __init__(self, firstName, lastName, age):
        super().__init__(firstName, lastName)
        self.age = age
chauffeurData = Chauffeur('Jackson', 'Noah', 30)
chauffeurData.print()
```
output: *Jackson Noah*

So the derived class Chauffer inherited attributes and methods from the base class Person, and it now also has an extra attribute called age. 
We may now try creating a derived class and both an extra attribute and an extra method. 

Let's create a derived class and add an extra property to it
```
class Helmsman(Person):
    def __init__(self, firstName, lastName, age):
        super().__init__(firstName, lastName)
        self.age = age
    # This print overrides the print() method of the Base class
    def print(self):
        print(self.firstName, self.lastName, self.age)
helmsmanData = Helmsman('Stephen', 'Kenneth', 30)
helmsmanData.print()
```
output: *Stephen Kenneth 30*

In the code above, we have defined a method called print, which uses the same name as the method defined in the derived class Person. 
However the method defined in the derived class takes precedence as it's more specific. 

And this time, with one other method
```
# add an extra method to the derived class
class Bearer(Person):
    def __init__(self, firstName, lastName, age):
        super().__init__(firstName, lastName)
        self.age = age
    def print(self):
        print(self.firstName, self.lastName, self.age)
    def prettyPrint(self):
        print('Hi, My  name is {} {}, and I am {} years old.' .format(self.firstName, self.lastName, self.age))
bearerData = Bearer('Williams', 'Goodman', '40')
bearerData.print()
bearerData.prettyPrint()
```
output: *Williams Goodman 40*

--end-of-post--
