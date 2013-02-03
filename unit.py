class Unit(object):
    """A GM unit, capable of melee combat and/or simple damage-based spellcast.

    """

    # List mapping internal attributes names to their actual names.
    ATTRIBUTES = (
        ('hp', 'HP'),
        ('damage', 'Damage'),
        ('wc', 'WC'),
        ('ac', 'AC'),
        ('critical_strike', 'Critical strike'),
        ('spell_resistance', 'Spell resistance'),
        ('spell_damage', 'Spell damage'),
    )

    # All units have a base speed of 5 for now.
    speed = 5

    def __init__(self, name, **kwargs):
        # Validate kwargs
        if not kwargs.get('hp'):
            raise ValueError('Units must have positive HP.')

        self.name = name

        for attribute, name in self.ATTRIBUTES:
            setattr(self, attribute, kwargs.get(attribute, 0))

    def __repr__(self):
        pieces = []
        for attribute, name in self.ATTRIBUTES:
            value = getattr(self, attribute)
            if value:
                pieces.append('%s %s' % (value, name))
        return '%s: %s' % (self.name, ' '.join(pieces))

    def __str__(self):
        return self.name

    @property
    def move_distance(self):
        return self.speed

    @property
    def run_distance(self):
        return 2 * self.speed