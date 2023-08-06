 > I want improve the criteria for identifying workers of a hotel vs guests. I was thinking about identifying devices that were seen in the hotel for 3 consecutive days, more than 3 times a month. Is it possible to do that efficiently and stay inside of pandas? I was thinking resample/groupby ‘1D’ and ‘device_id’, but I need an efficient way to calculate consecutive days

https://stackoverflow.com/questions/52901387/find-group-of-consecutive-dates-in-pandas-dataframe

* hours instead of days
* days instead of weeks


```python
    import pandas
```


```python
df = pandas.util.testing.makeTimeDataFrame(100, freq='3600s')
df.index = df.index.rename('independent')
df.columns = df.columns.rename('dependent')
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>dependent</th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
    <tr>
      <th>independent</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2000-01-01 00:00:00</td>
      <td>-1.864051</td>
      <td>0.194508</td>
      <td>-0.158947</td>
      <td>0.025978</td>
    </tr>
    <tr>
      <td>2000-01-01 01:00:00</td>
      <td>-0.924803</td>
      <td>-0.663514</td>
      <td>0.434736</td>
      <td>0.697357</td>
    </tr>
    <tr>
      <td>2000-01-01 02:00:00</td>
      <td>-0.270664</td>
      <td>-1.604472</td>
      <td>-0.249273</td>
      <td>0.812611</td>
    </tr>
    <tr>
      <td>2000-01-01 03:00:00</td>
      <td>-0.549321</td>
      <td>-0.701722</td>
      <td>-0.958898</td>
      <td>-0.730263</td>
    </tr>
    <tr>
      <td>2000-01-01 04:00:00</td>
      <td>0.251478</td>
      <td>-0.073544</td>
      <td>-0.615413</td>
      <td>0.167477</td>
    </tr>
    <tr>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>2000-01-04 23:00:00</td>
      <td>-0.329630</td>
      <td>-1.098350</td>
      <td>-2.224822</td>
      <td>-0.371213</td>
    </tr>
    <tr>
      <td>2000-01-05 00:00:00</td>
      <td>0.002818</td>
      <td>0.526695</td>
      <td>0.434844</td>
      <td>-0.449561</td>
    </tr>
    <tr>
      <td>2000-01-05 01:00:00</td>
      <td>-0.250249</td>
      <td>0.609006</td>
      <td>0.321713</td>
      <td>-0.161337</td>
    </tr>
    <tr>
      <td>2000-01-05 02:00:00</td>
      <td>-0.745092</td>
      <td>-1.161005</td>
      <td>-0.601730</td>
      <td>-1.112144</td>
    </tr>
    <tr>
      <td>2000-01-05 03:00:00</td>
      <td>-0.482342</td>
      <td>1.703145</td>
      <td>-0.876495</td>
      <td>0.132908</td>
    </tr>
  </tbody>
</table>
<p>100 rows × 4 columns</p>
</div>




```python
df = pandas.util.testing.makeTimeDataFrame(100, freq='3600s').stack()
df.index.names = 'time device'.split()
threshold = .6
guests = (df > threshold).astype(int)
__import__('IPython').display.Markdown(F"* One hotel with 4 guest {df.index.get_level_values('device').unique()}")
```




* One hotel with 4 guest Index(['A', 'B', 'C', 'D'], dtype='object', name='device')




```python
df = pandas.util.testing.makeTimeDataFrame(100, freq='3600s')
df.columns = df.columns.map(str.lower)
df = df.stack()
df.index.names = 'time device'.split()
threshold = -.1
employees = (df > threshold).astype(int)
__import__('IPython').display.Markdown(F"* One hotel with 4 employees {df.index.get_level_values('device').unique()}")
```




* One hotel with 4 employees Index(['a', 'b', 'c', 'd'], dtype='object', name='device')



Combine the guests and employees into a wide dataframe with hours on the the columns.  Values of 1 indicate a measurement.


```python
s = pandas.concat([guests, employees])
df = s[s.astype(bool)]
df = df.groupby([pandas.Grouper(level='time', freq='1H'), pandas.Grouper(level='device')]).sum().unstack('time', 0)
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>time</th>
      <th>2000-01-01 00:00:00</th>
      <th>2000-01-01 01:00:00</th>
      <th>2000-01-01 02:00:00</th>
      <th>2000-01-01 03:00:00</th>
      <th>2000-01-01 04:00:00</th>
      <th>2000-01-01 05:00:00</th>
      <th>2000-01-01 06:00:00</th>
      <th>2000-01-01 07:00:00</th>
      <th>2000-01-01 08:00:00</th>
      <th>2000-01-01 09:00:00</th>
      <th>...</th>
      <th>2000-01-04 18:00:00</th>
      <th>2000-01-04 19:00:00</th>
      <th>2000-01-04 20:00:00</th>
      <th>2000-01-04 21:00:00</th>
      <th>2000-01-04 22:00:00</th>
      <th>2000-01-04 23:00:00</th>
      <th>2000-01-05 00:00:00</th>
      <th>2000-01-05 01:00:00</th>
      <th>2000-01-05 02:00:00</th>
      <th>2000-01-05 03:00:00</th>
    </tr>
    <tr>
      <th>device</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>...</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <td>B</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>C</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <td>D</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <td>a</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <td>b</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <td>c</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <td>d</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>8 rows × 100 columns</p>
</div>



Hand roll our own pair correlation function using the [Wiener–Khinchin_theorem](https://en.wikipedia.org/wiki/Wiener–Khinchin_theorem).


```python
f = lambda df: pandas.DataFrame(abs(pandas.np.fft.ifftn(abs(pandas.np.fft.fftn(pandas.concat([df, df*0], axis=1), axes=(1,))**2), axes=(1,))), index=df.index)
```

Apply the pair correlation function to a day of data.


```python
g = lambda df: f(df.iloc[:, :24]).loc[:, 3].gt(3)
```


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>time</th>
      <th>2000-01-01 00:00:00</th>
      <th>2000-01-01 01:00:00</th>
      <th>2000-01-01 02:00:00</th>
      <th>2000-01-01 03:00:00</th>
      <th>2000-01-01 04:00:00</th>
      <th>2000-01-01 05:00:00</th>
      <th>2000-01-01 06:00:00</th>
      <th>2000-01-01 07:00:00</th>
      <th>2000-01-01 08:00:00</th>
      <th>2000-01-01 09:00:00</th>
      <th>...</th>
      <th>2000-01-04 18:00:00</th>
      <th>2000-01-04 19:00:00</th>
      <th>2000-01-04 20:00:00</th>
      <th>2000-01-04 21:00:00</th>
      <th>2000-01-04 22:00:00</th>
      <th>2000-01-04 23:00:00</th>
      <th>2000-01-05 00:00:00</th>
      <th>2000-01-05 01:00:00</th>
      <th>2000-01-05 02:00:00</th>
      <th>2000-01-05 03:00:00</th>
    </tr>
    <tr>
      <th>device</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>...</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <td>B</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>C</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <td>D</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <td>a</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <td>b</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <td>c</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>...</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <td>d</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>8 rows × 100 columns</p>
</div>




```python
g(df)
```




    device
    A    False
    B    False
    C    False
    D    False
    a     True
    b    False
    c     True
    d     True
    Name: 3, dtype: bool




```python
df.groupby(pandas.Grouper(level='time', freq='24H', axis=1)).agg(g)
```


```python
g(df)
```




    device
    A    False
    B    False
    C    False
    D    False
    a     True
    b     True
    c    False
    d     True
    Name: 3, dtype: bool




```python

```
