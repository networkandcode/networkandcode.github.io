---
title: python > ways to run code
categories
---

Let's see some ways of running Python. It's assumed you know some basics of Linux and its filesystem navigation.

## Interpreter

We can launch the python or python3 interpreter to issue certain commands.

Let's check where python3 is installed.
```
$ which python3
/usr/bin/python3
```

Run any python statement on the interpreter.
```
$ python3
Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print('Hello World!')
Hello World!
>>> 
```

This method is useful for testing, but what we type here is not saved, which means its not persistent.

## Script

This is the common way of running python code, we keep code in a file, and then run it as a script.
```
$ cat script.py 
print('Hello World!')

$ python3 script.py 
Hello World!
```

## Shebang
The shebang character sequence which is a combination of the number sign or hash (#) and an exclamation mark(!) could be used at the 
beginning of the file, to indicate the location of interpreter for the code.
```
$ cat script.py 
#!/usr/bin/python3

print('Hello World!')
```

This would help us running the code with out saying python3, while calling the file. But we are not ready yet, it would throw an error if we 
try now.
```
$ ./script.py
bash: ./script.py: Permission denied
```
Note that '.' refers to the current directory.

The error above indicates the file isn't executable yet.
```
$ ls -l script.py 
-rw-rw-r-- 1 networkandcode networkandcode 42 Oct 25 07:58 script.py
```

Let's make it executable.
```
$ chmod +x script.py 

$ ls -l script.py 
-rwxrwxr-x 1 networkandcode networkandcode 42 Oct 25 07:58 script.py
```

Well, it should work now !!!
```
$ ./script.py 
Hello World!
```

## Compile
We can also compile the complete code to see if there is any issues in any of the lines, with out running it.
```
$ python3 -m py_compile script.py 
$
```

An empty output means the code is syntactically good. The step above would create a __pycache__ directory with a pyc file inside.
```
$ ls __pycache__/
script.cpython-38.pyc
```

We could now run either the py file or the pyc file.
```
$ python3 script.py 
Hello World!

$ python3 __pycache__/script.cpython-38.pyc 
Hello World!
```

## Virtual Environment
We can virtual environments, which creates a complete copy of the python interpreter, any modules or packages installed inside the virtual 
environment, stays with in it and doesn't affect rest of the system. This is very useful when you have multiple projects and you don't want 
the dependecies of one project affecting another, which is otherwise possible without a virtual environment.

Although the venv package comes bundled with recent python3 installations, we may have to install it separately in debain/ubuntu systems.
```
$ sudo apt-get install python3-venv -y

```

Create a virtual environment.
```
$ python3 -m venv myenv
```

We should now have a directory by the name 'myenv', thats the name of virtual environment, and venv is the python3 package that helps 
creating virtual environments.
```
$ ls myenv
bin  include  lib  lib64  pyvenv.cfg  share
```

Start using the virtual environment using the source command below.
```
$ source myenv/bin/activate
(myenv) $ 
```

We are now in the virtual environment, what ever package we are going to install now in this virtual environment to going to stay here only.

Let's try installing flask.
```
myenv) $ pip install flask
Collecting flask
--TRUNCATED--
```

Let's start the python interpreter with in myenv, and import flask. Note its enough we give python here, even though we used python3 on the 
main bash terminal.
```
(myenv) $ python
Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import flask
>>> 
```

Flask was imported and no error was thrown, which means flask was installed successfully.

## IDEs
We could run code using IDEs such as pycharm, that gives lot of options in the GUI such as integrated terminal, file explorer, etc. We are 
not showing it here though.

## Conclusion
We have seen few ways of running python code, most of the times we would be running code as scripts i.e. files and virtual environments are 
used wherever applicable to isolate dependencies and to have an overall stable underlying system. The choice of CLI or GUI(IDE) is up to the 
developer, IDEs come with lots of options that can sometimes overwhelming during initial phases of learning. Thank you.

--end-of-post--
```






