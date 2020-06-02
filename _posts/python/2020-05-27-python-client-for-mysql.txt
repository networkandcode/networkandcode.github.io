---
title: python > client for mysql
categories: python
---

In this post, we are going to use the 'pymysql' for interacting with a MySQL database. The prerequisites are to 
have MySQL, Python3 and PIP already in the system

Let's get the MySql database ready
Note that in a Ubuntu system, MySQL could be installed and setup using 
```
sudo apt update; sudo apt install mysql-server -y; sudo mysql_secure_installation
```

A user can be created and can be assigned privileges as required
```
$ sudo mysql
mysql> CREATE USER 'networkandcode'@'localhost' IDENTIFIED BY 'Welcome@123';
Query OK, 0 rows affected (2.67 sec)

mysql> GRANT ALL PRIVILEGES ON * . * TO 'networkandcode'@'localhost';
Query OK, 0 rows affected (3.73 sec)

mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (1.16 sec)
```

Create a database
```
mysql> CREATE DATABASE SampleDB;
Query OK, 1 row affected (1.06 sec)
```

Create a table in the database
```
mysql> USE SampleDB;
Database changed

mysql> CREATE TABLE Students (
    -> ID int,
    -> FirstName varchar(255),
    -> LastName varchar(255)
    -> );
Query OK, 0 rows affected (3.92 sec)
``` 

Exit MySQL
```
mysql> exit
Bye
```

Let's do the Python work, to access the MySQL Database we just setup

We may now install the pymysql package using pip
```
networkandcode $ python3 -m pip install pymysql
Collecting pymysql
  Downloading https://files.pythonhosted.org/packages/ed/39/15045ae46f2a123019aa968dfcba0396c161c20f855f11dea6796bcaae95/PyMySQL-0.9.3-py2.py3-none-any.whl (47kB)
    100% |████████████████████████████████| 51kB 206kB/s
Installing collected packages: pymysql
Successfully installed pymysql-0.9.3
```







