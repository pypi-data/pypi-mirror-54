# DateString

Creates a manipulable date string in the form of 'YYYYmmdd'.

## Usage

- creates date string from various inputs.
```python
>>> ds = DateString('20180624')
>>> ds
'20180624'

>>> ds = DateString('2018/06/24')
>>> ds
'20180624'

>>> ds = DateString('2018-06-24')
>>> ds
'20180624'

>>> ds = DateString('2018年6月24日')
>>> ds
'20180624'

>>> ds = DateString(datetime.datetime(2018, 6, 24))
>>> ds
'20180624'

>>> today = DateString.today()
>>> yesterday = DateString.today(-1)
>>> tomorrow = DateString.today(1)
```

- supports date calculation.
```python
>>> DateString('2018/6/24') + 90
'20180922'

>>> DateString('2018-09-22') - 90
'20180624'

>>> DateString('2018-09-22') - '2018/06/24'
90

>>> DateString('2018/9/22') - datetime.datetime(2018, 6, 24)
90

>>> DateString('20180922') - DateString('2018-6-24')
90

>>> DateString('2018年9月22日') - pd.Timestamp('2018-06-24')
90
```

- supports date comparison.
```python
>>> DateString('20180922') == '2018/9/22'
True

>>> DateString('20180922') == '2018/6/24'
False

>>> DateString('20180922') >= '2018/6/24'
True

>>> DateString('20180922') >= '2019/9/22'
False
```

- supports date-related properties.
```python
>>> ds = DateString('2018-06-24')
>>> ds.year
2018
>>> ds.month
6
>>> ds.day
24
>>> ds.dayofweek
6
>>> ds.dayofyear
175
>>> ds.is_leap_year
False
>>> ds.is_weekday
False
>>> ds.is_weekend
True
```

- compatible with `pandas.date_range()`.
```python
>>> begin_ds = DateString('2019-01-01')
>>> end_ds = DateString('2019/1/3')
>>> pd.date_range(begin_ds, end_ds)
DatetimeIndex(['2019-01-01', '2019-01-02', '2019-01-03'], dtype='datetime64[ns]', freq='D')
```

- supports date string reformatting.
```python
>>> ds = DateString('20180624')
>>> ds.reformat()
'2018-06-24'
>>> ds.reformat(delimiter='/')
'2016/06/24'
```