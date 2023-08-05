# parsewhen

Parse when is a library for extracting and parsing date / time from regular English text.


![pipeline status](https://gitlab.com/sj1k/parsewhen/badges/release/pipeline.svg)
![coverage](https://gitlab.com/sj1k/parsewhen/badges/release/coverage.svg)


## Usage


```python
import parsewhen


parsewhen.parse('10:30pm next Friday')

# 2019-11-01 22:30:00 
# 
# parse() takes text and converts it to either a datetime or timedelta.
# Whichever is found first.


list(parsewhen.generate('10:30pm next Friday, for 10 hours'))

# [datetime.datetime(2019, 11, 1, 22, 30), ', for ', datetime.timedelta(0, 36000)]
#
# generate() takes text and generates groups of either datetimes, timedeltas or text.


list(parsewhen.range('Next week'))

# [datetime.datetime(2019, 10, 22, 0, 0), datetime.datetime(2019, 10, 23, 0, 0), ...
#  ..., datetime.datetime(2019, 10, 29, 0, 0)]
#
# Generates a datetime for each 'step' in a range.
# Similar to the built in range() you can specify a start, stop and a step.
```


## Roadmap

This is a list of things it can currently parse and the ones I plan to support.


- [ ] Date / Time
   - [x] Time `10pm / 01:30`
   - [x] Date `1st / 2nd / ...`
   - [x] Day `Monday / Friday / Wed / ...` (no shortnames yet)             
   - [x] Month `January / October / Apr / ...` (no shortnames yet)
   - [x] Year `2019 / 2001 / ...`
   - [x] Prefixes `Next Tuesday / Last week / Next Month`
   - [x] Tomorrow `Tomorrow / Yesterday / ...`
   - [ ] Timezone `+11 / GMT+0`


Relative durations are like durations but they return a datetime, rather than timedelta.


- [x] Relative duration
   - [x] Ago `2 days ago / 5 hours ago`
   - [x] In `In 3 days / In 7 weeks`


- [x] Duration
   - [x] Years `1year / 7years`
   - [x] Hour `10hours / 1hour`
   - [x] Minutes `5minutes / 2min`
   - [x] Seconds `3seconds / 100sec`
   - [x] Days `3 days / 8 days / ...`

- [ ] Words for numbers `One / Two / Three / ...`
