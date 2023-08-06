import math
import numpy as np
import matplotlib.pyplot as plt

class ParameterException(Exception):
    def __init__(self, issue=""):
        print(issue)

def avrg(iterable):
    return sum(iterable) / len(iterable)

def median(iterable):
    if len(iterable) % 2 == 0:
        mid_val_1 = len(iterable) / 2
        mid_val_2 = mid_val_1 + 1
        median_tuple = mid_val_1, mid_val_2
        return avrg(median_tuple)
    else:
        return iterable[len(iterable)/2]

def prob(iterable, name, round_cyphers=None):
    elems = 0
    for i in iterable:
        if i == name:
            elems += 1
    raw_prob = elems / len(iterable) * 100
    return raw_prob

def stringize(elem):
    if type(elem) == int:
        return str(elem) + "%"
    else:
        raise ParameterException("'Stringize' function does not accept non-integer parameters")

def numerize(elem):
    if type(elem) == str:
        if "%" in elem:
            elem = elem.replace("%", "")
            return int(elem)
        elif "/" in elem:
            bar_pos = elem.index("/")
            numerator = elem[:bar_pos]
            denom = elem[bar_pos + 1 ::]
            return int(numerator) / int(denom)
        else:
            raise ParameterException("Parameter needs to be either a prob (%) or a fraction (1/4)")
    else:
        raise ParameterException("'Stringize' function does not accept non-integer parameters")

def frac_prob(iterable, name, round_cyphers=None):
    elems = 0
    for i in iterable:
        if i == name:
            elems += 1
    return str(elems) + "/" + str(len(iterable))