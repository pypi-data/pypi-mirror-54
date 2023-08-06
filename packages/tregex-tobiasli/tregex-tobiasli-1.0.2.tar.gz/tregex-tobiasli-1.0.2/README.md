# tregex
[![Build Status](https://travis-ci.org/tobiasli/tregex.svg?branch=master)](https://travis-ci.org/tobiasli/tregex)<br/>
[![Coverage Status](https://coveralls.io/repos/github/tobiasli/tregex/badge.svg?branch=master)](https://coveralls.io/github/tobiasli/tregex?branch=master)<br/>
[![PyPI version](https://badge.fury.io/py/tregex-tobiasli.svg)](https://badge.fury.io/py/tregex-tobiasli)<br/>

`tregex` is a wrapper around Python regular expressions that makes usage smoother and more user friendly.

## Install

```
pip install tregex-tobiasli
```

## Usage

```python
import tregex as tr

t = tr.to_tuple(pattern='([^;]+?)@(.+?)\.([^;]+)', string='john.smith@somewhere.co.uk; hackzor@coolface.com')
assert t[0][1] == 'somewhere'
assert t[1][2] == 'com'

pattern = '(?P<name>[^;]+?)@(?P<address>.+?)\.(?P<domain>[^;]+)'
t = tr.to_dict(pattern=pattern, string='john.smith@somewhere.co.uk; hackzor@coolface.com')
assert t[0]['name'] == 'john.smith'
assert t[1]['address'] == 'coolface'

t = tr.to_object(pattern=pattern, string='john.smith@somewhere.co.uk; hackzor@coolface.com')
assert t[0].name == 'john.smith'
assert t[1].address == 'coolface'
```

The above methods patterns can be either a string or a compiled regular expression. `TregexCompiled` is a class for simply
containing the compiled regex to be run on the above methods. If patterns are long, this usage will speed things up
considerably.

```python
from tregex import TregexCompiled

pattern = '(?P<name>[^;]+?)@(?P<address>.+?)\.(?P<domain>[^;]+)'
trc = TregexCompiled(pattern)

t = trc.to_object('john.smith@somewhere.co.uk; hackzor@coolface.com')

assert t[0].name == 'john.smith'
```

tregex also contains some methods for simply fuzzy text matching using `difflib.SequenceMatcher`:

```python
from tregex import find_best

places_in_wales = ['Llanaber', 'Llanaelhaearn', 'Llanbedr', 'Llandbedrgoch', 'Llanbedrog', 'Llanberis', 'Llandanwg', 'Llanegryn', 'Llandegwning', 'Llandeiniolen', 'Llandwrog']

best = find_best('Llanberris', places_in_wales)
assert best == 'Llanberis'
```

The other methods are `find`, `find_scores` (returns the matched scores along with the candidate) and `similarity` (which
returns the score between a single pair of strings).
