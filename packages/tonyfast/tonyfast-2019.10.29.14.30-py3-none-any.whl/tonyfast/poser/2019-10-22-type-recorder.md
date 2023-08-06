```python
    import dataclasses, typing, collections, functools

    class Record(collections.defaultdict):
        """Record types called."""
        __init__ = functools.partialmethod(collections.defaultdict.__init__, functools.partial(collections.defaultdict, lambda: 0))
        def __call__(self, callable):
            @functools.wraps(callable)
            def call(*args, **kwargs):
                nonlocal self, callable
                try:
                    object = callable(*args, **kwargs)
                    self[callable][typing.Callable[list(map(type, args)), type(object)]] += 1
                    return object
                except BaseException as e:
                    self[callable][typing.Callable[list(map(type, args)), type(e)]] += 1
                    raise e
            return call
```
