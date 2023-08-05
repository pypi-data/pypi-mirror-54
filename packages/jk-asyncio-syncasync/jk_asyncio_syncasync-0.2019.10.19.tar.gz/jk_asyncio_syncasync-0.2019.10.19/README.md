jk_asyncio_syncasync
==========

Introduction
------------

This python module enables asyncio based functions/methods to invoke classic synchroneous functions/methods. This is implemented by delegating execution of to a thread pool.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/....)
* [pypi.python.org](https://pypi.python.org/pypi/jk_asyncio_syncasync)

Why this module?
----------------

Mixing synchroneous and asynchroneous code is not so easy and generally not recommended. Unfortunately sometimes you run into a situation where you can't avoid mixing both. For example this is the case if you need to invoke a synchroneous method implemented in a third party module where there is no asynchroneous counterpart implementation to the synchroneous one so that you can't avoid invoking the synchroneous code. In such a situation your call to a synchroneous function/method would block the asynchroneous task loop.

This module solves this problem by running the synchroneous method in a background thread without block the asynchroneous task loop. It therefore provides a safe way to invoke synchroneous code from within asynchroneous code.

Limitations of this module
--------------------------

This module focuses on `asyncio` (and `asyncio`) only. For `trio` this module is not required as `trio` already contains this functionality.

How to install module
----------------------

This module can be installed easily using `pip`.

Use this command for a system wide installation of this module:

```bash
$ sudo pip install jk-asyncio-syncasync
```

Use this command for user specific installation of this module:

```bash
$ pip install --user jk-asyncio-syncasync
```

The PiPy module is always kept in sync with the Github repository so using PyPi is equivalent to a manual installation using the code provided on Github.

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
from jk_asyncio_syncasync import *
```

### Invoke a synchroneous function directly

Let's asume we have implemented a synchroneous function, for example this one:

```python
def synchroneousFunction():
	print("Beginning synchroneous task ...")
	time.sleep(2)
	print("Synchroneous task completed.")
```

Let's now asume we want to invoke this function. This can be done with the following code using the function `call_sync()` provided by this module:

```python
await call_sync(synchroneousFunction)
```

### Invoke a synchroneous function using a decorator

Let's asume we have implemented a synchroneous function, for example this one:

```python
def synchroneousFunction():
	print("Beginning synchroneous task ...")
	time.sleep(2)
	print("Synchroneous task completed.")
```

You can make use of a decorator in order to make this function asynchroneous:

```python
@make_async
def synchroneousFunction():
	print("Beginning synchroneous task ...")
	time.sleep(2)
	print("Synchroneous task completed.")
```

Now invoking this function is easy:

```python
await synchroneousFunction()
```

### Invoking methods

It's perfectly safe to use `call_sync()` and the decorator `@make_async` with methods. Example:

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



