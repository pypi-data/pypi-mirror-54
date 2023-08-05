`λ` is an `object` for fluent function composition in `"python"` based on the `toolz` library.


```python
    import toolz, abc, inspect, functools, typing, importlib, builtins, json, pathlib, operator, itertools
    from toolz.curried import *
```


```python
    def identity(*args, **kwargs): return args[0] if args else None
```


```python
    def forward(module, *, property='', period='.'):
        if not isinstance(module, str): return module
        while period:
            try:
                if not property: raise ModuleNotFoundError
                return operator.attrgetter(property)(importlib.import_module(module))
            except ModuleNotFoundError as BaseException:
                module, period, rest = module.rpartition('.')
                property = '.'.join((rest, property)).rstrip('.')
                if not module: raise BaseException
```


```python
    class juxt(toolz.functoolz.juxt):
        def __new__(self, funcs):
            if isinstance(funcs, str): return forward(funcs)
            if callable(funcs): return funcs
            if not toolz.isiterable(funcs): return funcs
            self = super().__new__(self)
            return self.__init__(funcs) or self
        def __init__(self, object): self.funcs = object
        def __call__(self, *args, **kwargs):
            if isinstance(self.funcs, typing.Mapping):
                object = type(self.funcs)()
                for key, value in self.funcs.items():
                    if callable(key): key = key(*args, **kwargs)
                    if callable(value): value = value(*args, **kwargs)
                    object[key] = value
                else: return object
            if toolz.isiterable(self.funcs):return type(self.funcs)(x(*args, **kwargs) if callable(x) else x for x in self.funcs)                    
            if callable(self.funcs): return self.funcs(*args, **kwargs)
            return self.funcs

    class Ø(BaseException):
        def __bool__(self): return False

    def write(object, filename): return getattr(pathlib.Path(filename), F"write_{'bytes' if isinstance(object, bytes) else 'text'}")(object)
```


```python
    class Compose(toolz.functoolz.Compose):
        """
        
    >>> Compose(funcs=[range, len])(1, 10)
    9
    >>> Compose(2)[range][len](9)
    7
    >>> (λ[range] * λ[{toolz.identity: range}] + list)(3)
    [{0: range(0, 0)}, {1: range(0, 1)}, {2: range(0, 2)}]
    
    >>> (λ[range]*λ[type, str]+list+λ().isinstance(list))(10)
    True
        """
        def __init__(self, *args, **kwargs):
            super().__init__(list(reversed(kwargs.pop('funcs', [identity]))))
            self.args, self.excepts, self.kwargs = args, kwargs.pop('excepts', tuple()), kwargs
            
        def __call__(self, *args, **kwargs):
            args, kwargs = self.args + args, {**self.kwargs, **kwargs}
            for callable in (self.first,) + self.funcs: 
                try: args, kwargs = (callable(*args, **kwargs),), {}; object = args[0]
                except self.excepts as Exception: return Ø(Exception)
            return object
        compute = __call__
        
        def off(this):
            if this.funcs: this.funcs = this.funcs[:-1]
            else: this.first = identity
            return this
        def on(this): return this
        
        def pipe(this, object, *args, **kwargs):
            """`append` an `object` to `this` composition."""
            if isinstance(this, type): this = this()
            if object == slice(None): return this
            if isinstance(object, typing.Hashable):
                if object in {True, 1}: return this.on()
                if object in {False, 0}: return this.off()
            if not object: return this
            object = juxt(forward(object))
            if args or kwargs: object = toolz.partial(object, *args, **kwargs)
            if this.first == identity: this.first = object
            else: this.funcs += object,
            return this
        __add__ = __radd__ = __iadd__ = __getitem__ = pipe
        __sub__ = __rsub__ = __isub__ = pipe
        
        def map(self, callable): return self[toolz.curried.map(juxt(callable))]
        __mul__ = __rmul__ = __imul__ = map
        
        def filter(self, callable): return self[toolz.curried.filter(juxt(callable))]
        __truediv__ = __rtruediv__ = __itruediv__ = filter
        
        def groupby(self, callable): return self[toolz.curried.groupby(juxt(callable))]
        __matmul__ = __rmatmul__ = __imatmul__ = groupby
        
        def reduce(self, callable): return self[toolz.curried.reduce(juxt(callable))]
        __mod__ = __rmod__ = __imod__ = reduce
        
        def isinstance(self, type): return self[toolz.partial(toolz.flip(isinstance), type)]
        __pow__ = __ipow__ = isinstance
        
        def excepts(self, *Exceptions): return λ(excepts=Exceptions)[self]
        __xor__ = excepts
        
        def ifthen(self, callable): return IfThen(self[callable])
        __and__ = ifthen
        
        def ifnot(self, callable): return IfNot(self[callable])
        __or__ = ifnot
        
        def do(self, callable): return self[toolz.curried.do(juxt(callable))]
        __lshift__ = do
        
        def write(self, file): return self.do(toolz.curried.flip(write)(file))
        __rshift__ = write
    
        def loads(self, json=False): return self[json and __import__('json').loads or yaml]
        __pos__ = loads
        
        def dumps(self, **kwargs): return self[json.dumps]
        __neg__ = dumps
        
        def complement(self, object=None): return λ[toolz.complement(self)] if object == None else self[toolz.complement(object)]
        __invert__ = complement
        
        def attrgetter(self, *args, **kwargs): return self[operator.attrgetter(*args, **kwargs)]
        def itemgetter(self, *args, **kwargs): return self[operator.itemgetter(*args, **kwargs)]
        def methodcaller(self, *args, **kwargs): return self[operator.methodcaller(*args, **kwargs)]
        
        
        def read_bytes(self): return self[pathlib.Path][pathlib.Path.read_bytes]
        
        def parse(self): return self.pipe(yaml)
        
        def get(self, *args, **kwargs): return self.pipe(__import__('requests').get, *args, **kwargs)
        def json(self, *args, **kwargs): return self[__import__('requests').Response.json]
        def text(self, *args, **kwargs): return self.attrgetter('text')
        
        def frame(self, *args, **kwargs): return self[__import__('pandas').DataFrame]
        def series(self, *args, **kwargs): return self[__import__('pandas').Series]
        
        def git(self, *args, **kwargs): return self[__import__('git').Repo]
        
    class Conditional(Compose):
        def __init__(self, predicate, *args, **kwargs):
            self.predicate = super().__init__(*args, **kwargs) or predicate
            
    class IfThen(Conditional):
        def __call__(self, *args, **kwargs):
            object = self.predicate(*args, **kwargs)
            return super().__call__(*args, **kwargs) if object else object
        
    class IfNot(Conditional):
        def __call__(self, *args, **kwargs):
            object = self.predicate(*args, **kwargs)
            return object if object else super().__call__(*args, **kwargs)

    try: import IPython
    except: ...
    else: 
        for key, value in toolz.merge(
            toolz.pipe(IPython.display, vars, toolz.curried.valfilter(callable), toolz.curried.keyfilter(toolz.compose(str.isupper, toolz.first))),
            toolz.pipe(toolz, vars, toolz.curried.valfilter(callable), toolz.curried.keyfilter(toolz.compose(str.islower, toolz.first))),
        ).items(): 
            if not hasattr(Compose, key): setattr(Compose, key, getattr(Compose, key, functools.partialmethod(Compose.pipe, value)))

    class Type(abc.ABCMeta): ...
    for attr in set(dir(Compose))-(set(dir(toolz.functoolz.Compose)))-set("__weakref__ __dict__".split()): setattr(Type, attr, getattr(Type, attr, getattr(Compose, attr)))
        
    class λ(Compose, metaclass=Type): ...
```


```python
    def read(object, *args, **kwargs):
        try: return pathlib.Path(object).read_text()
        except: ...
        response = __import__('requests').get(object, *args, **kwargs)
        try: return response.json()
        except: return response.text
```


```python
    def yaml(object, *, loads=json.loads):
        try: from ruamel.yaml import safe_load as loads
        except ModuleNotFoundError: 
            try: from yaml import safe_load as loads
            except: ...
        return loads(object)
```


```python
    __test__ = {__name__: """
    Initializing a composition.

        >>> assert λ[:] == λ() == λ[::] == λ[0] == λ[1] 
        >>> λ[:]
        λ(<function identity at ...>,)

    Composing compositions.

        >>> λ[callable]
        λ(<built-in function callable>,)
        >>> assert λ[callable] == λ+callable == callable+λ == λ-callable == callable-λ

    Juxtapositions.

        >>> λ[type, str]
        λ(<__main__.juxt object at ...>,)
        >>> λ[type, str](10)
        (<class 'int'>, '10')
        >>> λ[{type, str}](10)
        {<class 'int'>, '10'}
        >>> λ[{'a': type, type: str}](10)
        {'a': <class 'int'>, <class 'int'>: '10'}
        
    Mapping.
    
        >>> (λ[range] * type + list)(3)
        [<class 'int'>, <class 'int'>, <class 'int'>]
        >>> λ[range].map((type, str))[list](3)
        [(<class 'int'>, '0'), (<class 'int'>, '1'), (<class 'int'>, '2')]
        
        
    Filtering
    
        >>> (λ[range] / λ[(3).__lt__, (2).__rfloordiv__][all] + list)(10)
        [4, 5, 6, 7, 8, 9]
        >>> (λ[range] / (λ[(3).__lt__, (2).__rmod__][all]) + list)(10)
        [5, 7, 9]


    Forward references.

        >>> λ['random.random']()
        0...

    Syntactic sugar causes cancer of the semicolon.  

    Feature flags: `λ` has `"on" "off"` features flags.

        >>> λ[range].do(λ+list+print).on()(10)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        range(0, 10)
        >>> λ[range].do(λ+list+print).off()(10)
        range(0, 10)
        >>> λ[range].do(λ+list+print)[False](10), λ[range].do(λ+list+print)[0](10)
        (range(0, 10), range(0, 10))



    """
    }

    import doctest; __name__ == '__main__' and display(doctest.testmod(optionflags=doctest.ELLIPSIS), IPython.display.Markdown(__test__[__name__]))
```


    TestResults(failed=0, attempted=20)




Initializing a composition.

    >>> assert λ[:] == λ() == λ[::] == λ[0] == λ[1] 
    >>> λ[:]
    λ(<function identity at ...>,)

Composing compositions.

    >>> λ[callable]
    λ(<built-in function callable>,)
    >>> assert λ[callable] == λ+callable == callable+λ == λ-callable == callable-λ

Juxtapositions.

    >>> λ[type, str]
    λ(<__main__.juxt object at ...>,)
    >>> λ[type, str](10)
    (<class 'int'>, '10')
    >>> λ[{type, str}](10)
    {<class 'int'>, '10'}
    >>> λ[{'a': type, type: str}](10)
    {'a': <class 'int'>, <class 'int'>: '10'}
    
Mapping.

    >>> (λ[range] * type + list)(3)
    [<class 'int'>, <class 'int'>, <class 'int'>]
    >>> λ[range].map((type, str))[list](3)
    [(<class 'int'>, '0'), (<class 'int'>, '1'), (<class 'int'>, '2')]
    
    
Filtering

    >>> (λ[range] / λ[(3).__lt__, (2).__rfloordiv__][all] + list)(10)
    [4, 5, 6, 7, 8, 9]
    >>> (λ[range] / (λ[(3).__lt__, (2).__rmod__][all]) + list)(10)
    [5, 7, 9]


Forward references.

    >>> λ['random.random']()
    0...

Syntactic sugar causes cancer of the semicolon.  

Feature flags: `λ` has `"on" "off"` features flags.

    >>> λ[range].do(λ+list+print).on()(10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    range(0, 10)
    >>> λ[range].do(λ+list+print).off()(10)
    range(0, 10)
    >>> λ[range].do(λ+list+print)[False](10), λ[range].do(λ+list+print)[0](10)
    (range(0, 10), range(0, 10))







```python

```
