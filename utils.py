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