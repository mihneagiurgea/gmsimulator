from utils import check_d20_roll, d20_roll_hit_chance

class VersusGameState(object):
    """Represents the state of a single 1v1 game.

    This class is responsible for implementing and validating the following
    game actions:
      * move towards
      * (full) melee attack
      * charge
      * spell cast
    """

    def __init__(self, units, distance):
        self.units = units
        self.current_hp = { unit: unit.hp for unit in self.units }
        self.distance = distance
        self.round = 1
        self._active_turn = 0

    def next_turn(self):
        """Ends the current turn."""
        self._active_turn += 1
        if self._active_turn == 2:
            # End of a round.
            self._active_turn = 0
            self.round += 1

    def __repr__(self):
        return '<%s Round %d: %s HP vs %s HP, distance: %d>' % \
            (self.__class__.__name__, self.round,
             self.current_hp[self.units[0]],
             self.current_hp[self.units[1]],
             self.distance)

    def get_opponent(self, unit):
        if unit == self.units[0]:
            return self.units[1]
        else:
            return self.units[0]

    @property
    def active_unit(self):
        return self.units[self._active_turn]

    @property
    def alive(self):
        min_hp = min(self.current_hp.itervalues())
        if min_hp > 0:
            return True
        else:
            return False

    @property
    def winner(self):
        max_hp = max(self.current_hp.itervalues())
        for unit, hp in self.current_hp.iteritems():
            if hp == max_hp:
                return unit

    """Game actions - they might belong in a different class. """

    def _deal_damage(self, unit, value):
        self.current_hp[unit] -= value
        # print '%s was dealt %d damage' % (unit, value)

    def move_towards(self, unit, distance):
        """Move towards your opponent."""
        if distance >= self.distance:
            raise ValueError('Invalid distance: %d/%d' % (distance, self.distance))
        if distance > 2 * unit.speed or distance <= 0:
            raise ValueError('Invalid distance to move: %d' % distance)

        self.distance -= distance

    def attack_melee_full(self, attacker):
        """Full melee attack (2 attacks, 2nd with -5 WC)."""
        if self.distance != 1:
            raise ValueError('Can only attack adjacent units.')
        self._process_single_melee_attack(attacker)
        self._process_single_melee_attack(attacker, -5)

    def attack_melee(self, attacker):
        """Single melee attack."""
        if self.distance != 1:
            raise ValueError('Can only attack adjacent units.')
        self._process_single_melee_attack(attacker)

    def charge(self, attacker):
        """Attacker performs a charge (move > speed) against defender, or
        a move action followed by an attack."""
        if not (attacker.speed < self.distance <= 2 * attacker.speed):
            raise ValueError('Invalid charge distanct: %d' % self.distance)
        self.move_towards(attacker, self.distance-1)
        # Charge attacks have a -2 WC penalty.
        self._process_single_melee_attack(attacker, -2)

    def _process_single_melee_attack(self, attacker, wc_modifier=0):
        """Process a single melee attack."""
        defender = self.get_opponent(attacker)
        if check_d20_roll(attacker.wc + wc_modifier, defender.ac):
            attack_damage = attacker.damage
            if check_d20_roll(attacker.critical_strike, 21):
                attack_damage *= 2
            self._deal_damage(defender, attack_damage)

    def spell_cast(self, attacker):
        """Offensive spell cast."""
        defender = self.get_opponent(attacker)
        if check_d20_roll(0, defender.spell_resistance):
            self._deal_damage(defender, attacker.spell_damage)
