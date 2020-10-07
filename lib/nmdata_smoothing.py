import json
import datetime
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def smoothForFields(list, field, consecutive=7):
    """
    Given an array of objects with numerical attributes, leave the first entries alone,
    and then average the consecutive entries from the number of consecutive entries requested. 
    """
    def averaged(array, idx):
        if (idx < consecutive):
            return array[idx]
        else:
            return sum(array[idx-consecutive:idx])/consecutive
        
    newArray = [l[field] for l in list]
    return [averaged(newArray, idx) for (idx, e) in enumerate(newArray)] 

def collected(jsonFile,starting = 0):
    """
    Average, collect, and sort the fields in the provided entry. In the result. 
    * data is the 
    """
    entries = json.load(open(jsonFile))["data"]
    r = [ {
        "dataDate": t['date'],
        "cases": t['cases'],
        "deaths": t['deaths'],
        "tests": t['tests']
        } for t in entries[starting:]]
    r.sort( key=lambda x:x['dataDate'])
    
    newCases = smoothForFields(entries, 'cases', 10) 
    newTests = smoothForFields(entries, 'tests', 10)
    windows = [
        {'date': r[i]['dataDate'],
         'cases': max(newCases[i]-newCases[i-7],0),
         'tests': max(newTests[i]-newTests[i-7],0),
         'deaths': r[i]['deaths']
         }
        for i in range(7,len(r))
        ]

    windows = [{
        'date' : w['date'],
        'cases' : w['cases'],
        'tests' : w['tests'],
        'deaths' : w['deaths'],
        'pos' : w['cases']/w['tests'] if (w['tests']) else 0
        }
        for w in windows
        ]
    windows = [
        {
            'date' : w['date'],
            'pos': w['pos'],
            'deaths' : w['deaths'],
            'estimate' : 28*w['cases']*math.sqrt(max(w['pos'],0.0))     
        }
        for w in windows
        ]
    windows = [
        {
        'date': w['date'],
        'pos': w['pos'],
            'deaths' : w['deaths'],
        'estimate': w['estimate']
        }
        for w in windows
        ]
    return windows
