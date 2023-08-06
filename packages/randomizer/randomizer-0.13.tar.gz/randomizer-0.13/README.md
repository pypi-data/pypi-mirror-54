## Randomize

Liberty for generate random data. 

### Docs 



#### Randomize
Class for create custom random list.

```python
r = Randomize(['try', 'this', 'class'])
r.element() # -> 'class'
r.elements(3) #  ['this', 'try', 'try']
r.group_elements(2)  # -> 'try class' 
# pop del rundom element and return him
r.pop() # -> 'this'
# if pass index number, pop will be used as list.pop () 
r.pop(0) # -> 'try'
```

#### random_text_unicode
Generates random strings with unicode symbol.

 *param size*: size of returned text
 
 *param random_size*: if True, return random size [0*size]
 
 *return*: unicode text

```python
random_text_unicode(10)  # -> 'aT݃пޑ0սYׅa
random_text_unicode(10, random_size=True)  # -> 'ɘ0ͯłƏ'

```
#### random_text

Generates random strings.

 *param size*: size of returned text
 
 *param random_size*: if True, return random size [0:size]
 
 *return*: text


```python
random_text(10)  # -> 'v 9е93кт1O'
random_text(10, random_size=True)  # -> 'RПkF'
```
  
 
#### random_float

 *param a*: start digit
 
 *param b*: end digit
 
 *return*: random float with 14 digit after coma

```python
random_float(1.1, 2.2) # -> 1.4524252884290065
```
#### random_datetime

 *param a*: start datetime
 
 *param b*: end datetime
 
 *return*: random datetime with timezone of 'a' parameter

```python
random_datetime(datetime(2007,1,2,3,4,5), datetime.now())
# -> datetime.datetime(2019, 10, 11, 23, 1, 11, 296813)
```
#### random_list_element

 *param array*: list of elements
 
 *return*: random element of array

```python
random_list_element([1,2,3,4,5]) # -> 4 
```
#### random_bool

 *return*: return random bool value

```python
random_bool() # -> True
```
#### random_unix_time

 *return*: a float value from 0 to the current time with 7 digit after coma

```python
random_unix_time() # -> 785009993.9438592
```
 
#### random_dt_now

 *return*: a datetime object from 1.1.1980 to the current datetime without timezone

```python
random_dt_now() # -> datetime.datetime(1986, 4, 23, 3, 46, 12, 133432)
```
#### random_positive_float

 *param max_value*: maximum value
 
 *return*: random positive float with 14 digit after come

```python
random_positive_float(1.123) # -> 0.6647791533497713
```

### INT

return random digit, from ↓ table

```text
Type          Bytes         Minimum               Maximum
__________________________________________________________
TINYINT	        1	    -128		   127
SMALLINT	2	    -32768		   32767
MEDIUMINT	3	    -8388608	           8388607
INT	        4	    -2147483648	           2147483647
BIGINT	        8	    -2*63		   (2*63)-1
```
  
#### random_tinyint
```python
random_tinyint() # -> 62
```
  
#### random_smallint
```python
random_smallint() # -> 17031
```
#### random_mediumint
```python
random_mediumint() # -> 5518123
```
#### random_int
```python
random_int() # -> -1572638799
```
#### random_bigint
```python
random_bigint() # -> -475732340272717339
```


