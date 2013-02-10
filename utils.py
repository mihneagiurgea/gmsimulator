import random

def d20():
    return random.randint(1, 20)

def check_d20_roll(modifier, target):
    """Check d20 + modifier vs target:
      * a score greater than or equal represents a hit, otherwise a miss
      * d20=20 => automatic hit
      * d20=1 => automatic miss
    """
    roll = d20()
    if roll == 20:
        return True
    if roll == 1:
        return False
    return roll + modifier >= target

def d20_roll_hit_chance(modifier, target):
    """What are the changes of a d20_roll to hit?
    >>> d20_roll_hit_chance(12, 23)
    0.5
    >>> d20_roll_hit_chance(0, 23)
    0.05
    >>> d20_roll_hit_chance(13, 10)
    0.95
    """
    min_roll = target - modifier
    # A 20 is an automatic hit.
    min_roll = min(min_roll, 20)
    min_roll = max(min_roll, 2)
    return (20 - min_roll + 1) / 20.0

def argmax(d):
    """The maximum argument of a dictionary.
    >>> argmax({ 1: 17, 2: 93, 2: 52, })
    2
    """
    best = max(d.itervalues())
    for k in d:
        if d[k] == best:
            return k

def argmin(d):
    """The minimum argument of a dictionary.
    >>> argmin({ 1: 17, 2: 93, 2: 52, })
    1
    """
    best = min(d.itervalues())
    for k in d:
        if d[k] == best:
            return k

if __name__ == '__main__':
    import doctest
    doctest.testmod()