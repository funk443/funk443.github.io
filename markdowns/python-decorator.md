Title: The clearest explaination to Python decorators I've ever seen

[TOC]

So I was writing my Discord bot last night, and I was confused by something.  After some research, I not only solved the problem, but also found the best explaination about Python decorator I've ever seen.

Here is it, let's say we have a decorator like this:

```python
def deco(func):
    def wrap():
        # Do things with func
        pass

    return wrap
```

And a form like this:

```python
@deco
def foo():
    # Do things
    pass
```

The above form is equivalant to this following form:

```python
def foo():
    # Do things
    pass

foo = deco(foo)
```

For decorators with arguments:

```python
def make_deco(x, y):
    def deco(func):
        # Do things with x and y.

        def wrap():
            # Do things with func.
            pass

        return wrap

    return deco
```

and we have this form:

```python
@make_deco(x, y)
def foo():
    # Do things.
    pass
```

The above one is equivalant to this one:

```python
def foo():
    # Do things
    pass

foo = make_deco(x, y)(foo)
```

So the `make_deco(x, y)` basically returns a function, `deco(func)`, then this just becomes using a decorator that does not take arguments.

For multiple decorator applied, it's like this:

```python
@deco2
@deco1
def foo():
    # Do things.
    pass
```

The above form is equivalant to this form:

```python
def foo():
    # Do things.
    pass

foo = deco2(deco1(foo))
```

[This explanation](https://peps.python.org/pep-0318/#current-syntax) is, in my opinion, the best one explaning how decorators work.  It just transforms the decorator syntax, which is not very intuitive, to very simple function calls.