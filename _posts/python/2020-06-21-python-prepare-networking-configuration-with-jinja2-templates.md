---
categories: python
title: python > prepare networking configuration with jinja2 templates
---
### Topic
Jinja2 is a templating language used within Python, and we are going to 
prepare some standard networking configuration using Python and Jinja2. 
### Prerequisites
- You are aware of some network device configuration
- Python3 is already installed
- PIP is already installed

### Install
Install the jinja2 python package, over Internet using PIP
```
networkandcode $ pip3 install jinja2
```

### Launch 
Launch Python3 terminal, if in your system 'python' refers to 'python3' 
you may launch it so using 'python' itself
```
networkandcode $ python3
Python 3.8.2 (default, Apr 27 2020, 15:53:34)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
### Import
Import the 'Template' class from the 'jinja2' package.
```
>>> from jinja2 import Template
```
### Define string
Let's define a string that contains templating variables, enclosed within \{\{ and  \}\}.
```
{% raw %}
>>> interfaceConfiguration = '''
... interface {{ interfaceName }}
...   ip address {{interfaceIP}} {{interfaceMask}}
... '''
{% endraw %}
```
So we have three template variables and the string now contains the 
templating variables as is
```
{% raw %}
>>> print(interfaceConfiguration)

interface {{interfaceName}}
  ip address {{interfaceIP}} {{interfaceMask}}

>>>
{% endraw %}
```

### Define template
We may now define our template, i.e. we are going to make a template 
object from the string we defined earlier, using the ```Template``` Class of the ```jinja2``` package.
```
>>> intConfigTemplate = Template(interfaceConfiguration)
```
If we try printing this template object, it tells us it is a 'Template' 
object and also returns the location in memory allotted to that. 
The 'id' and 'type' functions can also be also used to check the memory 
location and object type respectively.
```
>>> print(intConfigTemplate)
<Template memory:7fff33e832e0>
>>> print(id(intConfigTemplate))
140734064243424
>>> print(type(intConfigTemplate))
<class 'jinja2.environment.Template'>
```
Note that both ```140734064243424``` and ```7fff33e832e0``` refer to the 
same location, however in Decimal and HexaDecimal notations respectively.

### Available methods
The 'dir' function can be used to check the contents of an object i.e. the 
list of available attributes and methods available for our object. 
Note that a method is also a function, however its only available to an object that belongs to a class. So, the 
object ```intConfigTemplate``` can access the methods that belongs to the
Template class.
```
>>> dir(intConfigTemplate)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', 
'__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', 
'__init__', '__init_subclass__', '__le__', '__lt__', '__module__', 
'__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', 
'__setattr__', '__sizeof__', '__str__', '__subclasshook__', 
'__weakref__', '_debug_info', '_from_namespace', 
'_get_default_module', '_get_default_module_async', '_module', 
'_uptodate', 'blocks', 'debug_info', 'environment', 'filename', 
'from_code', 'from_module_dict', 'generate', 'generate_async', 
'get_corresponding_lineno', 'globals', 'is_up_to_date', 'make_module', 
'make_module_async', 'module', 'name', 'new_context', 'render', 
'render_async', 'root_render_func', 'stream']
```
### Actual configuration
```render``` is one of the available methods, that we are going to try. 
The render method takes the values of template variables as arguments. 
We have 3 template variables, and hence we have to pass 3 arguments

```
>>> intConfigTemplate.render(interfaceName='ge-0/0/0', interfaceIP='192.168.100.10', interfaceMask='255.255.255.0')
'\ninterface ge-0/0/0\n  ip address 192.168.100.10 255.255.255.0'
```
We could better save this to a variable to reuse it when required
```
>>> ge000=intConfigTemplate.render(interfaceName='ge-0/0/0', interfaceIP='192.168.100.10', interfaceMask='255.255.255.0')
```
If we print the variable, we get our actual interface configuration
```
>>> print(ge000)

interface ge-0/0/0
  ip address 192.168.100.10 255.255.255.0
```
And this is nothing but a string
```
>>> print(type(ge000))
<class 'str'>
```
so what we have done so far is
string -> template -> string
i.e. we converted a string to a template which is then converted 
to a different string

we could form multiple such strings, one for each interface, let's do 
for a different interface
```
>>> ge001=intConfigTemplate.render(interfaceName='ge-0/0/1', interfaceIP='192.168.100.11', interfaceMask='255.255.255.0')
>>> print(ge001)

interface ge-0/0/1
  ip address 192.168.100.11 255.255.255.0
```
The strip() method could be used to remove leading and trailing spaces from 
the string
```
>>> print(ge001.strip())
interface ge-0/0/1
  ip address 192.168.100.11 255.255.255.0
>>>
```
### Loop
So far we have been generating configurations for one interface at a time. We could also 
generate configurations for multiple interfaces at the same time by using 'for' in our template.

### Define a dictionary
We are going to define a dictionary, that has data for multiple interfaces, for the three template variables
```
>>> interfaces = [
...     {'interfaceName': 'ge-0/0/0', 'interfaceIP': '192.168.1.0', 'interfaceMask': '255.255.255.0'},
...     {'interfaceName': 'ge-0/0/1', 'interfaceIP': '192.168.1.1', 'interfaceMask': '255.255.255.0'},
...     {'interfaceName': 'ge-0/0/2', 'interfaceIP': '192.168.1.2', 'interfaceMask': '255.255.255.0'}
... ]
```
### Define string
Let's define our string, but this time we are also going to include a 
jinja2 for loop in the string, note that statements such as for would be enclosed within \{% %\} jinja2, where as 
variables would be enclosed with in \{\{ ..  \}\}
```
{% raw %}
>>> interfacesConfiguration = '''
... {% for i in interfaces %}
... interface {{i.interfaceName}}
...   ip address {{i.interfaceIP}} {{i.interfaceMask}}
... {% endfor %}
...'''
{% endraw %}
```
### Convert to template
So our template string is ready, we now need to convert this to a template object like before. Last time 
we have used the ```Template``` class, but this time we are going to use ```Environment```.
So we first have to import it from ```jinja2``` package as we have used statements such as ```for```.

#### Import Environment
```
>>> from jinja2 import Environment
```
#### Create Template
The template object can be created as follows
```
>>> Environment().from_string(interfacesConfiguration)
<Template memory:7fff337f2880>
```
Note that we can also use ```Template(interfacesConfiguration)``` to make a Template object.

Its better we assign this to a variable for reusing it when required
```
>>> intsConfigTemplate = Environment().from_string(interfacesConfiguration)
```
### Actual configuration
Since the template object is now ready, its time to ```render``` the actual configuration
```
>>> intsConfigTemplate.render(interfaces=interfaces)
'\n\t\ninterface ge-0/0/0\n  ip address 192.168.1.0 255.255.255.0\n\t\ninterface ge-0/0/1\n  ip address 192.168.1.1 255.255.255.0\n\t\ninterface ge-0/0/2\n  ip address 192.168.1.2 255.255.255.0\n'
```
We can use a variable to store this
```
>>> actualIntsConfig = intsConfigTemplate.render(interfaces=interfaces)
>>> print(actualIntsConfig)


interface ge-0/0/0
  ip address 192.168.1.0 255.255.255.0

interface ge-0/0/1
  ip address 192.168.1.1 255.255.255.0

interface ge-0/0/2
  ip address 192.168.1.2 255.255.255.0

>>>
```
We can remove the leading and trailing spaces with ```strip()```
```
>>> print(actualIntsConfig.strip())
interface ge-0/0/0
  ip address 192.168.1.0 255.255.255.0

interface ge-0/0/1
  ip address 192.168.1.1 255.255.255.0

interface ge-0/0/2
  ip address 192.168.1.2 255.255.255.0
```
--end-of-post--
