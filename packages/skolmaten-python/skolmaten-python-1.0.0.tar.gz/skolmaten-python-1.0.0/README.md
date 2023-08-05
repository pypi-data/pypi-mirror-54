# skolmaten-python

[![Build Status](https://jenkins.lovskog.net/buildStatus/icon?job=skolmaten-python%2Fmaster&style=flat-square)](https://jenkins.lovskog.net/job/skolmaten-python/job/master/)

This is a simple wrapper for the [skolmaten.se](https://skolmaten.se) service.

I wrote this becuase I needed a way to get the data for what I am going to eat in school for some stuff. So, why not publish it and help somebody else.

FOR NON-SWEDISH PEPOLE: [skolmaten.se](https://skolmaten.se) has data for what is going to be servered in schools all over Sweden.
  
## Usage

```python

from skolmaten import skolmaten

# You can find the id of your school by going to skolmaten.se, selecting your school, and looking in the address bar. 
# For example this is what I see for polhemsskolan => https://skolmaten.se/polhemsskolan2/
schoolFood = skolmaten("polhemsskolan2")

weekly = schoolFood.getData()
print(weekly)

[{'date': datetime.datetime(2019, 10, 14, 0, 0), 'food': [u'Falukorv med potatismos', u'Potatisfrestelse med salladsost', u'ängsbiffar']}, ... {'date': datetime.datetime(2019, 10, 21, 0, 0), 'food': [u'Pastasås Arrabiata med linser och soltorkade tomater', u'Grönsakspaj']}]

```

## Todo

- [x] Basic weekly data.
- [ ] 100% Test coverage.
- [ ] Full documation.