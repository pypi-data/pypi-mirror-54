## Installing

```
pip3 install throttle
```

## Usage

```python
import time
import random
import throttle

delay = 1
# remove values every 1 second

limit = 3
# hold up to 3 values

key = lambda value: value < 5
# only check values less than 5 against the limit

valve = throttle.create(delay, limit, key = key)

# make some quick calls
for index in range(10):

  item = random.randrange(0, 8)

  allow = valve(item)

  print(item, allow)

  time.sleep(0.25)
```
