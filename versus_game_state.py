import rules
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

    def __init__(self, units, distance=None, debug=False, verbosity=0):
        # Default distance value.
        if distance is None:
            distance = rules.MAP_WIDTH-1

        self.units = units
        self._current_hp = { unit: unit.hp for unit in self.units }
        self.distance = distance
        self.round = 1
        self._active_turn = 0
        if debug:
            verbosity = 99
        self.verbosity = verbosity

    def run_combat(self):
        """Resolve combat by fighting to the death!"""
        if self.verbosity >= 2:
            print('\tTurn order:\n1. %s\n2. %s' % (self.units[0], self.units[1]))
            print '===Fight to the death!==='
        while self.alive:
            self.active_unit.act(self)
            self.next_turn()
        if self.verbosity >= 2:
            print '===End of Round %d===\n' % self.round
        if self.verbosity >= 1:
            print 'Combat lasted %d rounds:' % self.round
            print 'Winner: %s (%.2f HP)' % (self.winner, self[self.winner])
            print 'Loser : %s (%.2f HP)' % (self.loser, self[self.loser])
            print 'HPDelta: %.2f' % self.hp_delta

    def next_turn(self):
        """Ends the current turn."""
        if self.verbosity >= 2:
            print 'End of %s\'s turn:\n\t%r' % (self.active_unit, self)
        self._active_turn += 1
        if self._active_turn == 2:
            # End of a round.
            if self.verbosity >= 2:
                print '===End of Round %d===\n' % self.round
            self._active_turn = 0
            self.round += 1

    def __repr__(self):
        return '<GameState Round %d: %s HP vs %s HP, distance: %d>' % \
            (self.round, self[self.units[0]], self[self.units[1]],
             self.distance)

    def __getitem__(self, unit):
        """Returns the current HP of a unit."""
        return self._current_hp[unit]

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
        min_hp = min(self._current_hp.itervalues())
        if min_hp > 0:
            return True
        else:
            return False

    @property
    def winner(self):
        max_hp = max(self._current_hp.itervalues())
        for unit, hp in self._current_hp.iteritems():
            if hp == max_hp:
                return unit

    @property
    def loser(self):
        return self.get_opponent(self.winner)

    @property
    def hp_delta(self):
        """unit1.HP - unit2.HP"""
        return self[self.units[0]] - self[self.units[1]]

    """Game actions - they might belong in a different class. """

    def _deal_damage(self, unit, value):
        self._current_hp[unit] -= value
        # print '%s was dealt %d damage' % (unit, value)

    def move_towards(self, unit, distance):
        """Move towards your opponent."""
        if distance >= self.distance:
            raise ValueError('Invalid distance: %d/%d' % (distance, self.distance))
        if distance > 2 * unit.speed or distance <= 0:
            raise ValueError('Invalid distance to move: %d' % distance)

        self.distance -= distance

    def attack_full_melee(self, attacker):
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
        dmg = self._get_dmg_single_melee_attack(attacker, defender, wc_modifier)
        if dmg is not None:
            self._deal_damage(defender, dmg)

    def spell_cast(self, attacker):
        """Offensive spell cast."""
        defender = self.get_opponent(attacker)
        dmg = self._get_dmg_spell_cast(attacker, defender)
        if dmg is not None:
            self._deal_damage(defender, dmg)

    def _get_dmg_single_melee_attack(self, attacker, defender, wc_modifier=0):
        """Computes the outcome of a single melee attack.

        Returns:
            The damage dealt, or None, if the attack was a miss.
        """
        if check_d20_roll(attacker.wc + wc_modifier, defender.ac):
            if check_d20_roll(attacker.critical_strike, 21):
                return attacker.damage * 2
            else:
                return attacker.damage
        else:
            return None

    def _get_dmg_spell_cast(self, attacker, defender):
        """Computes the outcome of a spell cast attack.

        Returns:
            The damage dealt, or None, if the attack was a miss.
        """
        if check_d20_roll(0, defender.spell_resistance):
            return attacker.spell_damage
        else:
            return None

    """ DPS - average Damage per Second (or Turn, in our case) """

    def get_dps_full_melee(self, attacker):
        """Compute the average DPS of a Full melee attack."""
        defender = self.get_opponent(attacker)
        return ( self._get_dps_single_melee_attack(attacker, defender) +
                 self._get_dps_single_melee_attack(attacker, defender, -5) )

    def get_dps_charge(self, attacker):
        defender = self.get_opponent(attacker)
        return self._get_dps_single_melee_attack(attacked, defender, -2)

    def get_dps_spell_cast(self, attacker, defender=None):
        """Compute the average DPS of a Spell cast attack."""
        if defender is None:
            defender = self.get_opponent(attacker)
        hit_chance = d20_roll_hit_chance(0, defender.spell_resistance)
        return attacker.spell_damage * hit_chance

    def _get_dps_single_melee_attack(self, attacker, defender, wc_modifier=0):
        """Computes the average damage of a single melee attack."""
        hit_chance = d20_roll_hit_chance(attacker.wc + wc_modifier, defender.ac)
        avg_dmg = attacker.damage * (1.0 + attacker.critical_strike / 20.0)
        return hit_chance * avg_dmg

class AveragingVersusGameState(VersusGameState):
    """Average all d20 rolls, and use average damage instead."""

    _get_dmg_single_melee_attack = VersusGameState._get_dps_single_melee_attack
    _get_dmg_spell_cast = VersusGameState.get_dps_spell_cast
