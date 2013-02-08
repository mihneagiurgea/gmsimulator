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
