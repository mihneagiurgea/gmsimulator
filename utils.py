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

if __name__ == '__main__':
    import doctest
    doctest.testmod()