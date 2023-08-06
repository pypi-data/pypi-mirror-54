# dateparse
[![Build Status](https://travis-ci.org/tobiasli/dateparse.svg?branch=master)](https://travis-ci.org/tobiasli/dateparse)<br/>
[![Coverage Status](https://coveralls.io/repos/tobiasli/dateparse/badge.svg?branch=master&service=github)](https://coveralls.io/github/tobiasli/dateparse?branch=master)<br/>
[![PyPI version](https://badge.fury.io/py/dateparse-tobiasli.svg)](https://badge.fury.io/py/dateparse-tobiasli)<br/>

Dateparser for creating datetime objects from arbitrarily formated date strings. Primary support for Norwegian date formats.

New version is a complete refactor:
* Much faster parsing. 
* Reduced pattern complexity. 
* Improved matching rutine. 
* Some reduced functionality with less used time formats (centuries, relative dates, text based). 

## Install

```
pip install dateparse-tobiasli
```
## Usage
```python
import datetime
from dateparse import DateParser
parser = DateParser()

# Dates with alpha components:
dt = parser.parse('5. januar 2015')
print(dt == [datetime.datetime(2015, 1, 5, 0, 0)])

# Multiple dates from same string:
dt = parser.parse('1/12/2014 kl 12, 11.12.2015 kl 14')
print(dt == [datetime.datetime(2014, 12, 1, 12, 00), datetime.datetime(2015, 12, 11, 14, 00)])
```
