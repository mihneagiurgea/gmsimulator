from base_unit import BaseUnit

class Unit(BaseUnit):
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

    # Will inherit speed from BaseUnit.speed

    def __init__(self, name, **kwargs):
        BaseUnit.__init__(self, name, **kwargs)

        # Validate HPs.
        if not self.hp:
            raise ValueError('Units must have positive HP.')

