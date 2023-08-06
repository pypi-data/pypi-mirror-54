```python
    import toolz, abc, inspect, functools, typing, importlib, urllib, builtins, json, pathlib, operator, itertools, fnmatch
    from toolz.curried import *
```

What is does a `toolz` bound version of poser look like?  That means _none of my nonsense_ __only critical logic__.


```python
    class Compose(toolz.functoolz.Compose):
        __slots__ = toolz.functoolz.Compose.__slots__ + tuple("args kwargs exceptions".split())
        def __init__(self, funcs=None, *args, **kwargs): 
            """`Compose` stores `args` and `kwargs` like a partial."""
            super().__init__(funcs or (I,)); self.args, self.exceptions, self.kwargs = args, kwargs.pop('exceptions', tuple()), kwargs
            
        def __call__(self, *args, **kwargs):
            args, kwargs = self.args + args, {**self.kwargs, **kwargs}
            for callable in (self.first,) + self.funcs: 
                try: args, kwargs = (callable(*args, **kwargs),), {}; object = args[0]
                except self.exceptions as Exception: return Ø(Exception)
            return object
        compute = __call__        
        
        """`__add__ or pipe` a function into the composition."""  
        def pipe(this, object=None, *args, **kwargs):
            """`append` an `object` to `this` composition."""
            if isinstance(this, type) and issubclass(this, Compose): this = this()
            if object == slice(None): return this
            if not object: return this
            object = forward(object)
            if args or kwargs: object = toolz.partial(object, *args, **kwargs)
            if this.first == I: this.first = object
            else: this.funcs += object,
            return this
        __add__ = __radd__ = __iadd__ = __getitem__ = pipe
        def skip(this, *args, **kwargs): return this
        __sub__ = __rsub__ = __isub__ = pipe        
        __pow__ = isinstance = functools.partialmethod(pipe, flip(isinstance))
        
    for key, value in toolz.merge(
        toolz.pipe(toolz, vars, toolz.curried.valfilter(callable), toolz.curried.keyfilter(toolz.compose(str.islower, toolz.first))),
        toolz.pipe(builtins, vars, toolz.curried.valfilter(callable), toolz.curried.keyfilter(toolz.compose(str.islower, toolz.first)))).items():
        if not hasattr(Compose, key): 
            setattr(Compose, key, getattr(Compose, key, functools.partialmethod(Compose.pipe, value)))
            getattr(Compose, key).__doc__ = inspect.getdoc(value)
            
    for attr, symbol in map(str.split, "map mul;filter truediv;groupby matmul;reduce mod".split(';')):
        if attr not in Compose.__slots__:
            [setattr(Compose, format.format(symbol), getattr(Compose, attr)) for format in "__{}__ __i{}__ __r{}__".split()]
    Compose.__mul__ = Compose.__imul__ = Compose.__rmul__ =Compose.map
    
    class Type(abc.ABCMeta): 
        def __getattribute__(cls, str):
            if str in _type_method_names: return object.__getattribute__(cls, str)
            return object.__getattribute__(cls(), str)
        
    _type_method_names = set(dir(Type))        
    for attr in set(dir(Compose))-(set(dir(toolz.functoolz.Compose)))-set("__weakref__ __dict__".split()): 
        setattr(Type, attr, getattr(Type, attr, getattr(Compose, attr)))
        
    class λ(Compose, metaclass=Type): 
        def __init__(self, *args, **kwargs): super().__init__(None, *args, **kwargs)
    
```

Sometimes we have to write our own utility functions.


```python
    def I(*args, **kwargs): "A nothing special identity function, does pep8 peph8 me?"; return args[0] if args else None
    def forward(module, *, property='', period='.'):
        """Load string forward references"""
        if not isinstance(module, str): return module
        while period:
            try:
                if not property: raise ModuleNotFoundError
                return operator.attrgetter(property)(importlib.import_module(module))
            except ModuleNotFoundError as BaseException:
                module, period, rest = module.rpartition('.')
                property = '.'.join((rest, property)).rstrip('.')
                if not module: raise BaseException
                    
    class juxt(toolz.functoolz.juxt):
        def __new__(self, funcs):
            if isinstance(funcs, str): funcs = forward(funcs)
            if callable(funcs) or not toolz.isiterable(funcs): return funcs
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
            if toolz.isiterable(self.funcs): return type(self.funcs)(x(*args, **kwargs) if callable(x) else x for x in self.funcs)                    
            if callable(self.funcs): return self.funcs(*args, **kwargs)
            return self.funcs
        
        

    class Ø(BaseException):
        def __bool__(self): return False
```


```python
    def stars(callable):
        @functools.wraps(callable)
        def call(*iter, **kwargs):
            args, iter = list(), list(iter)
            while iter:
                if isinstance(iter[-1], typing.Mapping): kwargs.update(iter.pop())
                else: args.extend(iter.pop()) 
            return callable(*args, **kwargs)        
        return call
```

`"__main__"` tests.


```python
    
    __test__ = globals().get('__test__', {}); __test__[__name__] = """
    #### Tests
    
    Initializing a composition.

        >>> assert λ[:] == λ() == λ[::] 
        >>> λ[:]
        λ(<function I at ...>,)

    Composing compositions.

        >>> λ[callable]
        λ(<built-in function callable>,)
        >>> assert λ[callable] == λ+callable == callable+λ == λ.pipe(callable)
        >>> assert λ[callable] != λ[callable][range]
        >>> assert λ-callable == callable-λ

    Juxtapositions.

        >>> λ[juxt((type, str))]
        λ(<__main__.juxt object at ...>,)
        >>> λ[juxt((type, str))](10)
        (<class 'int'>, '10')
        
    Mapping.
    
        >>> (λ[range] * type + list)(3)
        [<class 'int'>, <class 'int'>, <class 'int'>]
        >>> λ[range].map(juxt((type, str)))[list](3)
        [(<class 'int'>, '0'), (<class 'int'>, '1'), (<class 'int'>, '2')]
        
    Filtering
    
        >>> (λ[range] / λ[juxt(((3).__lt__, (2).__rfloordiv__))][all] + list)(10)
        [4, 5, 6, 7, 8, 9]
        >>> (λ[range] / (λ[juxt(((3).__lt__, (2).__rmod__))][all]) + list)(10)
        [5, 7, 9]
        
    Filtering Mappings
    
        >>> λ('abc').enumerate().dict().valfilter('ab'.__contains__)()
        {0: 'a', 1: 'b'}
        >>> λ('abc').enumerate().dict().keyfilter((1).__lt__).valfilter(λ().pipe(operator.__contains__, 'bc'))()
        {2: 'c'}
        >>> λ('abc').enumerate().dict().keyfilter((1).__lt__)()
        {2: 'c'}
        
    Groupby
        
        > assert λ[range] @ (2).__rmod__ == λ[range].groupby((2).__rmod__)
        >>> (λ[range] @ (2).__rmod__)(10)
        {0: [0, 2, 4, 6, 8], 1: [1, 3, 5, 7, 9]}
        
    Reduce
        
        > assert λ[range]%int.__add__ == λ[range].reduce(int.__add__)
        >>> (λ[range] % int.__add__)(10)
        45
        
    Conditionals
    
        >>> λ[juxt((λ**int+bool, λ**str))](10)
        (True, False)
    
    Forward references.

        >>> λ['random.random']()
        0...
        
    Loading files.
    
        >>> read = λ[pathlib.Path][pathlib.Path.read_text][json.loads]
        >>> (λ('2019-10-18-another-bout-with-poser.ipynb')[read][
        ...      juxt((type, λ.get('cells')[toolz.first].get('cell_type')))
        ... ])()
        (<class 'dict'>, 'markdown')

    Starred functions allows arguments and dictionaries to be defined in iterables.
    
        >>> stars(range)([0,10])
        range(0, 10)
        >>> stars(λ[dict])(λ[range][reversed][enumerate][juxt((list,))](3))
        {0: 2, 1: 1, 2: 0}
         
    Some recipes.
    
    Load a bunch of notebooks as objects.
    
        >>> λ[λ[pathlib.Path].pipe(toolz.flip(pathlib.Path.glob), '*.ipynb').take(2)[list] * juxt((I, read)) + dict + 'pandas.Series'][juxt((type, len))]('')
        (<class 'pandas.core.series.Series'>, ...)
    """


    import doctest, IPython; __name__ == '__main__' and display(doctest.testmod(optionflags=doctest.ELLIPSIS), IPython.display.Markdown(__test__[__name__]))
```


    TestResults(failed=0, attempted=24)




#### Tests

Initializing a composition.

    >>> assert λ[:] == λ() == λ[::] 
    >>> λ[:]
    λ(<function I at ...>,)

Composing compositions.

    >>> λ[callable]
    λ(<built-in function callable>,)
    >>> assert λ[callable] == λ+callable == callable+λ == λ.pipe(callable)
    >>> assert λ[callable] != λ[callable][range]
    >>> assert λ-callable == callable-λ

Juxtapositions.

    >>> λ[juxt((type, str))]
    λ(<__main__.juxt object at ...>,)
    >>> λ[juxt((type, str))](10)
    (<class 'int'>, '10')
    
Mapping.

    >>> (λ[range] * type + list)(3)
    [<class 'int'>, <class 'int'>, <class 'int'>]
    >>> λ[range].map(juxt((type, str)))[list](3)
    [(<class 'int'>, '0'), (<class 'int'>, '1'), (<class 'int'>, '2')]
    
Filtering

    >>> (λ[range] / λ[juxt(((3).__lt__, (2).__rfloordiv__))][all] + list)(10)
    [4, 5, 6, 7, 8, 9]
    >>> (λ[range] / (λ[juxt(((3).__lt__, (2).__rmod__))][all]) + list)(10)
    [5, 7, 9]
    
Filtering Mappings

    >>> λ('abc').enumerate().dict().valfilter('ab'.__contains__)()
    {0: 'a', 1: 'b'}
    >>> λ('abc').enumerate().dict().keyfilter((1).__lt__).valfilter(λ().pipe(operator.__contains__, 'bc'))()
    {2: 'c'}
    >>> λ('abc').enumerate().dict().keyfilter((1).__lt__)()
    {2: 'c'}
    
Groupby
    
    > assert λ[range] @ (2).__rmod__ == λ[range].groupby((2).__rmod__)
    >>> (λ[range] @ (2).__rmod__)(10)
    {0: [0, 2, 4, 6, 8], 1: [1, 3, 5, 7, 9]}
    
Reduce
    
    > assert λ[range]%int.__add__ == λ[range].reduce(int.__add__)
    >>> (λ[range] % int.__add__)(10)
    45
    
Conditionals

    >>> λ[juxt((λ**int+bool, λ**str))](10)
    (True, False)

Forward references.

    >>> λ['random.random']()
    0...
    
Loading files.

    >>> read = λ[pathlib.Path][pathlib.Path.read_text][json.loads]
    >>> (λ('2019-10-18-another-bout-with-poser.ipynb')[read][
    ...      juxt((type, λ.get('cells')[toolz.first].get('cell_type')))
    ... ])()
    (<class 'dict'>, 'markdown')

Starred functions allows arguments and dictionaries to be defined in iterables.

    >>> stars(range)([0,10])
    range(0, 10)
    >>> stars(λ[dict])(λ[range][reversed][enumerate][juxt((list,))](3))
    {0: 2, 1: 1, 2: 0}
     
Some recipes.

Load a bunch of notebooks as objects.

    >>> λ[λ[pathlib.Path].pipe(toolz.flip(pathlib.Path.glob), '*.ipynb').take(2)[list] * juxt((I, read)) + dict + 'pandas.Series'][juxt((type, len))]('')
    (<class 'pandas.core.series.Series'>, ...)


