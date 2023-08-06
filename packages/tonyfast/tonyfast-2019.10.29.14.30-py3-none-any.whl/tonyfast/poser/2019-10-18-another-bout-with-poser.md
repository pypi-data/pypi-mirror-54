`λ` is an `object` for fluent function composition in `"python"` based on the `toolz` library.

1.  [__Motivation__](#Motivation)
2. [__Source__](#Source)
3. [__Tests__](#Tests)

#### Motivation

[Function composition](https://en.wikipedia.org/wiki/Function_composition) is a common task in mathematics and modern programming.
Object oriented function composition often breaks with conventional representations.
The `toolz` library provides a set of functional programming objects to `compose` and `pipe` functions together.
`compose` and `pipe` are top level composition functions that how two different typographic conventions.

In the `toolz` example, both `f and g` are the same

1. `compose` mimics a symbollic function composition.

        f = compose(type, len, range)
    
1. `pipe` allows a fluent composition.

        g = lambda x: pipe(x, range, len, type)
        def h(x: int) -> type: return pipe(x, range, len, type)
        
The typology of the `compose` composition is destructive to the flow of literature because it must be read `reversed`. 
`pipe` on the other hand supplements the narrative providing literate compositions aligned with the direction of the literature.

From a learning perspective, my experience with `poser` & its predecessors have taught me a lot about the pythonic data model.
`Compose` expresses a near complete symbollic API for function composition.


```python
    import toolz, abc, inspect, functools, typing, importlib, urllib, builtins, json, pathlib, operator, itertools, fnmatch
    from toolz.curried import *
```

#### Source

`Compose` augments `toolz.Compose` to provide a fluent & symbollic object for function composition in python.


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
            if isinstance(object, typing.Hashable):
                if object in {True, 1}: return this.on()
                if object in {False, 0}: return this.off()
            if not object: return this
            object = juxt(forward(object))
            if args or kwargs: object = toolz.partial(object, *args, **kwargs)
            if this.first == I: this.first = object
            else: this.funcs += object,
            return this
        __add__ = __radd__ = __iadd__ = __getitem__ = pipe
        
        def extend(this, *object):
            for object in object: this = this[object]
            else: return this
                
        def skip(this, *args, **kwargs): 
            """Don't append an object, for modifying compositions interactively."""
            return this[:]
        __sub__ = __rsub__ = __isub__ = skip
        
        """Feature flags"""
        def on(this): return this
        def off(this):
            if this.funcs: this.funcs = this.funcs[:-1]
            else: this.first = I
            return this
        
        """Mapping, Filtering, Groupby, and Reduction."""
        def map(this, callable, key=None): return this[toolz.partial(map, juxt(callable), key=juxt(key))]
        __mul__ = __rmul__ = __imul__ = map
        
        def filter(this, callable, key=None): return this[toolz.partial(filter, juxt(callable), key=juxt(key))]
        __truediv__ = __rtruediv__ = __itruediv__ = filter
        
        def groupby(this, callable): return this[toolz.curried.groupby(juxt(callable))]
        __matmul__ = __rmatmul__ = __imatmul__ = groupby
        
        def reduce(this, callable): return this[toolz.curried.reduce(juxt(callable))]
        __mod__ = __rmod__ = __imod__ = reduce
        
        """Conditionals."""
        def excepts(this, *Exceptions): return λ(excepts=Exceptions)[this]
        __xor__ = excepts
        
        def ifthen(this, callable): return IfThen(this[callable])
        __and__ = ifthen
        
        def ifnot(this, callable): return IfNot(this[callable])
        __or__ = ifnot
        
        """Helpers"""
        def isinstance(this, type): return IfThen(this[toolz.partial(toolz.flip(isinstance), type)])
        __pow__ = __ipow__ = isinstance
        
        def do(this, callable): return this[toolz.curried.do(juxt(callable))]
        __lshift__ = do
                
        def complement(this, object=None): return λ[toolz.complement(this)] if object == None else self[toolz.complement(object)]
        __invert__ = complement
        
        """Object tools"""
        def attrgetter(this, *args, **kwargs): return this[operator.attrgetter(*args, **kwargs)]
        def itemgetter(this, *args, **kwargs): return this[operator.itemgetter(*args, **kwargs)]
        def methodcaller(this, *args, **kwargs): return this[operator.methodcaller(*args, **kwargs)]
        
        """File tools"""
        def read(this, *args, **kwargs): return this.pipe(read, *args, **kwargs)
        __pos__ = read
        
        def write(this, file): return this.do(toolz.curried.flip(write)(file))
        __rshift__ = write
    
        def dumps(this, **kwargs): return this[json.dumps]
        __neg__ = dumps        
        
        def read_text(this): return this[pathlib.Path][pathlib.Path.read_text]
        def read_bytes(this): return this[pathlib.Path][pathlib.Path.read_bytes]
        
        """Directory tools"""
        def glob(this, pattern): return this[pathlib.Path][toolz.curried.flip(pathlib.Path.glob)(pattern)]
        def rglob(this, pattern): return this[pathlib.Path][toolz.curried.flip(pathlib.Path.rglob)(pattern)]
        
        def get(this, *args, **kwargs): return this.pipe(__import__('requests').get, *args, **kwargs)
        def json(this, *args, **kwargs): return this[__import__('requests').Response.json]
        def text(this, *args, **kwargs): return this.attrgetter('text')
        
        def frame(this, *args, **kwargs): return this[__import__('pandas').DataFrame]
        def series(this, *args, **kwargs): return this[__import__('pandas').Series]
        
        def git(this, *args, **kwargs): return this[__import__('git').Repo]
        def fnmatch(this, pattern): return this[toolz.curried.flip(fnmatch.fnmatch)(pattern)]
        
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
    except: IPython = None
    else: 
        for key, value in toolz.merge(
            toolz.pipe(toolz, vars, toolz.curried.valfilter(callable), toolz.curried.keyfilter(toolz.compose(str.islower, toolz.first))),
            toolz.pipe(builtins, vars, toolz.curried.valfilter(callable), toolz.curried.keyfilter(toolz.compose(str.islower, toolz.first))),
            {} if IPython is None else toolz.pipe(IPython.display, vars, toolz.curried.valfilter(callable), toolz.curried.keyfilter(toolz.compose(str.isalpha, toolz.first)))).items(): 
            if not hasattr(Compose, key): 
                setattr(Compose, key, getattr(Compose, key, functools.partialmethod(Compose.pipe, value)))
                getattr(Compose, key).__doc__ = inspect.getdoc(value)
    
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

    @functools.wraps(toolz.map)
    def map(callable, object, key=None):
        """A general `map` function for sequences and containers."""
        if isinstance(object, typing.Mapping):
            if key is not None: object = toolz.keymap(key, object)
            return toolz.valmap(forward(callable), object)
        return toolz.map(callable, object)
            
    @functools.wraps(toolz.filter)
    def filter(callable, object, key=None):
        """A general `filter` function for sequences and containers."""
        if isinstance(object, typing.Mapping):
            if key is not None: object = toolz.keyfilter(key, object)
            return toolz.valfilter(forward(callable), object)
        return toolz.filter(callable, object)

    def read(object, *args, **kwargs):
        """Read files, urls, or yaml.  Always try to parse json."""
        try: 
            object = pathlib.Path(object).read_text()
            try: return json.loads(object)
            except: return objects
        except: ...
        if urllib.parse.urlparse(object).scheme:
            response = __import__('requests').get(object, *args, **kwargs)
            try: return response.json()
            except: return response.text
        return yaml(object)

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

    def write(object, filename): return getattr(pathlib.Path(filename), F"write_{'bytes' if isinstance(object, bytes) else 'text'}")(object)

    def yaml(object, *, loads=json.loads):
        try: from ruamel.yaml import safe_load as loads
        except ModuleNotFoundError: 
            try: from yaml import safe_load as loads
            except: ...
        return loads(object)
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

        >>> assert λ[:] == λ() == λ[::] == λ[0] == λ[1] 
        >>> λ[:]
        λ(<function I at ...>,)

    Composing compositions.

        >>> λ[callable]
        λ(<built-in function callable>,)
        >>> assert λ[callable] == λ+callable == callable+λ == λ.pipe(callable)
        >>> assert λ[callable] != λ[callable][range]
        >>> assert λ.skip() == λ-callable == callable-λ

    Juxtapositions.

        >>> λ[type, str]
        λ(<__main__.juxt object at ...>,)
        >>> λ[type, str](10)
        (<class 'int'>, '10')
        >>> λ[{type, str}][type, len](10)
        (<class 'set'>, 2)
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
        
    Filtering Mappings
    
        >>> λ('abc').enumerate().dict().filter('ab'.__contains__)()
        {0: 'a', 1: 'b'}
        >>> λ('abc').enumerate().dict().filter(λ().pipe(operator.__contains__, 'bc') , (1).__lt__)()
        {2: 'c'}
        >>> λ('abc').enumerate().dict().keyfilter((1).__lt__)()
        {2: 'c'}
        
    Groupby
        
        >>> assert λ[range] @ (2).__rmod__ == λ[range].groupby((2).__rmod__)
        >>> (λ[range] @ (2).__rmod__)(10)
        {0: [0, 2, 4, 6, 8], 1: [1, 3, 5, 7, 9]}
        
    Reduce
        
        >>> assert λ[range]%int.__add__ == λ[range].reduce(int.__add__)
        >>> (λ[range] % int.__add__)(10)
        45
        
    Conditionals
    
        >>> λ[λ**int+bool, λ**str](10)
        (True, False)
    
    Forward references.

        >>> λ['random.random']()
        0...
        
    Loading files.
    
        >>> (λ('2019-10-18-another-bout-with-poser.ipynb').read()[
        ... type, λ.itemgetter('cells')[toolz.first].itemgetter('cell_type')
        ... ])()
        (<class 'dict'>, 'markdown')

    Syntactic sugar causes cancer of the semicolon.  

    Feature flags: `λ` has `"on" "off"` features flags.

        >>> λ[range].do(λ+list+print).on()(10)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        range(0, 10)
        >>> λ[range].do(λ+list+print).off()(10)
        range(0, 10)
        >>> λ[range].do(λ+list+print)[False](10), λ[range].do(λ+list+print)[0](10)
        (range(0, 10), range(0, 10))
        
        
    Starred functions allows arguments and dictionaries to be defined in iterables.
    
        >>> stars(range)([0,10])
        range(0, 10)
        >>> stars(λ[dict])(λ[range][reversed][enumerate][[list]](3))
        {0: 2, 1: 1, 2: 0}
         
    Some recipes.
    
    Load a bunch of notebooks as objects.
    
        >>> λ[λ.glob('*.ipynb').take(2)[list] * [I, λ.read()] + dict + 'pandas.Series'][type, len]()
        (<class 'pandas.core.series.Series'>, ...)
    """


    import doctest; __name__ == '__main__' and display(doctest.testmod(optionflags=doctest.ELLIPSIS), IPython.display.Markdown(__test__[__name__]))
```


    TestResults(failed=0, attempted=32)




#### Tests

Initializing a composition.

    >>> assert λ[:] == λ() == λ[::] == λ[0] == λ[1] 
    >>> λ[:]
    λ(<function I at ...>,)

Composing compositions.

    >>> λ[callable]
    λ(<built-in function callable>,)
    >>> assert λ[callable] == λ+callable == callable+λ == λ.pipe(callable)
    >>> assert λ[callable] != λ[callable][range]
    >>> assert λ.skip() == λ-callable == callable-λ

Juxtapositions.

    >>> λ[type, str]
    λ(<__main__.juxt object at ...>,)
    >>> λ[type, str](10)
    (<class 'int'>, '10')
    >>> λ[{type, str}][type, len](10)
    (<class 'set'>, 2)
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
    
Filtering Mappings

    >>> λ('abc').enumerate().dict().filter('ab'.__contains__)()
    {0: 'a', 1: 'b'}
    >>> λ('abc').enumerate().dict().filter(λ().pipe(operator.__contains__, 'bc') , (1).__lt__)()
    {2: 'c'}
    >>> λ('abc').enumerate().dict().keyfilter((1).__lt__)()
    {2: 'c'}
    
Groupby
    
    >>> assert λ[range] @ (2).__rmod__ == λ[range].groupby((2).__rmod__)
    >>> (λ[range] @ (2).__rmod__)(10)
    {0: [0, 2, 4, 6, 8], 1: [1, 3, 5, 7, 9]}
    
Reduce
    
    >>> assert λ[range]%int.__add__ == λ[range].reduce(int.__add__)
    >>> (λ[range] % int.__add__)(10)
    45
    
Conditionals

    >>> λ[λ**int+bool, λ**str](10)
    (True, False)

Forward references.

    >>> λ['random.random']()
    0...
    
Loading files.

    >>> (λ('2019-10-18-another-bout-with-poser.ipynb').read()[
    ... type, λ.itemgetter('cells')[toolz.first].itemgetter('cell_type')
    ... ])()
    (<class 'dict'>, 'markdown')

Syntactic sugar causes cancer of the semicolon.  

Feature flags: `λ` has `"on" "off"` features flags.

    >>> λ[range].do(λ+list+print).on()(10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    range(0, 10)
    >>> λ[range].do(λ+list+print).off()(10)
    range(0, 10)
    >>> λ[range].do(λ+list+print)[False](10), λ[range].do(λ+list+print)[0](10)
    (range(0, 10), range(0, 10))
    
    
Starred functions allows arguments and dictionaries to be defined in iterables.

    >>> stars(range)([0,10])
    range(0, 10)
    >>> stars(λ[dict])(λ[range][reversed][enumerate][[list]](3))
    {0: 2, 1: 1, 2: 0}
     
Some recipes.

Load a bunch of notebooks as objects.

    >>> λ[λ.glob('*.ipynb').take(2)[list] * [I, λ.read()] + dict + 'pandas.Series'][type, len]()
    (<class 'pandas.core.series.Series'>, ...)


