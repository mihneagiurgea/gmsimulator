from unit import Unit

class UnitFactory(object):

    _unit_counter = 0

    @classmethod
    def generate_name(cls, label='MyUnit'):
        cls._unit_counter += 1
        return '%s#%d' % (label, cls._unit_counter)

    @classmethod
    def create_malak(cls):
        return Unit(name = cls.generate_name('Malak'),
            hp=105,
            damage=14,
            wc=13,
            ac=19,
            critical_strike=6
        )

    @classmethod
    def create_warrior(cls):
        return Unit(name = cls.generate_name('HighAC'),
            hp=105,
            damage=9,
            wc=13,
            ac=23,
        )

    @classmethod
    def create_mage(cls):
        return Unit(name = cls.generate_name('Mage'),
            hp=45,
            ac=13,
            spell_damage=21
        )

    @classmethod
    def create_hybrid(cls):
        return Unit(name = cls.generate_name('Hybrid'),
            hp=75,
            damage=13,
            wc=11,
            ac=18,
            critical_strike=2,
            spell_damage=8,
            spell_resistance=4
        )
