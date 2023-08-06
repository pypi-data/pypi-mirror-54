```python
import tonyfast
```


```python
!pip install py-spy
```

    Collecting py-spy
    [?25l  Downloading https://files.pythonhosted.org/packages/49/5c/26626dcf4d8706a3015d9466fd3703b15de0d05b27bb4329aa344308ad91/py_spy-0.3.0-py2.py3-none-macosx_10_7_x86_64.whl (1.5MB)
    [K     |████████████████████████████████| 1.5MB 6.4MB/s eta 0:00:01
    [?25hInstalling collected packages: py-spy
    Successfully installed py-spy-0.3.0



```python
%%file myprogram.py
import tonyfast
```

    Overwriting myprogram.py



```python
    !py-spy record -o profile.svg -- python myprogram.py
```


```python
IPython.display.SVG('profile.svg')
```




![svg](output_4_0.svg)




```python
%load_ext snakeviz
%snakeviz import tonyfast.poser
```

     
    *** Profile stats marshalled to file '/var/folders/8x/l2g7g8cj1f79n71zvx84vlf00000gn/T/tmpw_chp0gh'. 
    Embedding SnakeViz in this document...




<iframe id='snakeviz-05af95de-f9d8-11e9-aa9a-80e65022f676' frameborder=0 seamless width='100%' height='1000'></iframe>
<script>document.getElementById("snakeviz-05af95de-f9d8-11e9-aa9a-80e65022f676").setAttribute("src", "http://" + document.location.hostname + ":8082/snakeviz/%2Fvar%2Ffolders%2F8x%2Fl2g7g8cj1f79n71zvx84vlf00000gn%2FT%2Ftmpw_chp0gh")</script>


