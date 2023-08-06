> python-anyconfig is a MIT licensed python library provides common APIs to load and dump configuration files in various formats with some useful features such as contents merge, templates, query, schema validation and generation support.

[Github](https://github.com/ssato/python-anyconfig/)
[Documentation](https://python-anyconfig.readthedocs.io)


This notebook demonstrates some features of `anyconfig` for loading and dumping data.  We raise a comparsion to `traitlets.config` at the end where a backend for python config files is created.


```python
    import anyconfig, pydantic, munch, json, toolz
```

`anyconfig` can load to multiple formats.


```python
    config = anyconfig.loads("""a: 10""", ac_parser='yaml')
    config.update(anyconfig.loads("""{"b": 10}""", ac_parser='json'))
```


```python
    anyconfig.loads("""a.q=10""", ac_parser='toml')
```




    {'a': {'q': 10}}



`anyconfig` allows `jinja2` templates.


```python
    anyconfig.loads("a: {{ a|default('aaa') }}\n", ac_parser='yaml', ac_template=True)
```




    {'a': 'aaa'}




```python
    anyconfig.loads("a: {{ a|default('aaa') }}\n", ac_parser='yaml', ac_template=True, ac_context={'a': 3})
```




    {'a': 3}



`anyconfig` can dump to multiple formats.


```python
    print(anyconfig.dumps(config, 'json'))
```

    {"a": 10, "b": 10}



```python
    print(anyconfig.dumps(config, 'yaml'))
```

    a: 10
    b: 10
    


`anyconfig` provides `jsonschema` validation.  We'll use `pydantic` to generate schema.


```python
    class Schema(pydantic.BaseModel): a: int; b: int
```


```python
    valid, _ = anyconfig.validate(config, Schema.schema())
    assert Schema and valid
```


```python
    class BadSchema(pydantic.BaseModel): a: int; b: str
```


```python
    valid, errors = anyconfig.validate(config, BadSchema.schema())
    assert not valid
    print(errors)
```

    10 is not of type 'string'
    
    Failed validating 'type' in schema['properties']['b']:
        {'title': 'B', 'type': 'string'}
    
    On instance['b']:
        10


In `traitlets` we could load configurations from python files.  Below we add similar functionality to `anyconfig` for a python backend.


```python
    def load(object, **c):
        if hasattr(object, 'read'): object = object.read()
        c['c'] = c.get('c', munch.Munch())
        return exec(object, c, c) or c['c']
```


```python
    class Python(anyconfig.backend.base.StringStreamFnParser):
        _cid = "python"
        _type = "python"
        _extensions = ["python"]
        _ordered = True
        _load_opts = _dump_opts = _dict_opts = ["_dict"]

        _load_from_string_fn = anyconfig.backend.base.to_method(load)
        _load_from_stream_fn = anyconfig.backend.base.to_method(load)
        _dump_to_string_fn = anyconfig.backend.base.to_method(toolz.compose('c = '.__add__, json.dumps))
        _dump_to_stream_fn = anyconfig.backend.base.to_method(json.dump)
```

Loading a python config.


```python
    data = anyconfig.loads("""c.a = list(range(10))""", ac_parser=Python); data
```




    {'a': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}



Writing a python config.


```python
    anyconfig.dumps(data, ac_parser=Python)
```




    'c = {"a": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}'


