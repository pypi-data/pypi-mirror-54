```python
    with __import__('importnb').Notebook():
        try: from .__init__ import load_ipython_extension
        except: from __init__ import load_ipython_extension
    load_ipython_extension(__import__('IPython').get_ipython())
```


    with __import__('importnb').Notebook():
        try: from .__init__ import load_ipython_extension
        except: from __init__ import load_ipython_extension
    load_ipython_extension(__import__('IPython').get_ipython())



```python
Testing

    print(11)
```

    11



Testing

    print(11)



```python
    def f():
# This is the docstring
        
        ...
    print(f.__doc__, '\n', __import__('inspect').getsource(f))
```

    # This is the docstring 
     def f():
        """# This is the docstring""";
    
        ...
    



    def f():
# This is the docstring
        
        ...
    print(f.__doc__, '\n', __import__('inspect').getsource(f))



```python
Bash in markdown
    
    echo hi
```

    hi





    




Bash in markdown
    
    echo hi

