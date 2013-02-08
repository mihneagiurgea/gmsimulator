import copy

from base_unit import BaseUnit
from versus_game_state import VersusGameState

class SimplifiedUnit(BaseUnit):
    """A Simplified GM unit, capable of less.
    """

    # List mapping internal attributes names to their actual names.
    ATTRIBUTES = (
        ('damage_adjacent', 'Adjacent Damage'),
        ('damage_charge', 'Charge Damage'),
        ('damage_ranged', 'Ranged Damage'),
    )

    # Will inherit speed from BaseUnit.speed

class SimplifiedVersusGameState(VersusGameState):
    """Simplified - instead of rolling dice, just average damages dealt."""

    def _process_single_melee_attack(self, attacker, defender, wc_modifier=0):
        """Reimplemented to represent a simplified melee attack."""
        hit_chance = d20_roll_hit_chance(attacker.wc + wc_modifier, defender.ac)
        avg_dmg = attacker.damage * (1.0 + attacker.critical_strike / 20.0)
        attack_damage = hit_chance * avg_dmg
        self._deal_damage(defender, attack_damage)

    def spell_cast(self, attacker, defender):
        """Reimplemented to represent a simplified spell cast."""
        hit_chance = d20_roll_hit_chance(0, defender.spell_resistance)
        attack_damage = attacker.spell_damage * hit_chance
        self._deal_damage(defender, attack_damage)

class SimplifiedGM(object):
    """Determines the outcome of the Simplified GM version.

    A simplified unit is a 4-tuple that describes its damage patterns:
        (dmg_adjacent, dmg_medium_range, dmg_long_range, run_speed)
    """

    def __init__(self, versus_game_state):
        # Deepcopy to avoid side effects.
        self.game_state = SimplifiedVersusGameState(\
            versus_game_state.units[0], versus_game_state.units[1],
            versus_game_state.distance)
        self.game_state.current_hp = versus_game_state.current_hp

    def _simulate(self, first_to_act):
        """Simulates and determines the outcome

        Args:
            first_to_act: The SimplifiedUnit that is next to act.
        """
        # Validate damage.
        for unit in self.simplified_units.values():
            if unit.is_melee:
                if not unit.damage_adjacent or not unit.damage_charge:
                    raise ValueError('Cannot play melee with no melee damage')
            else:
                if not unit.damage_ranged:
                    raise ValueError('Cannot play ranged with no ranged damage')

        hps = [self.versus_game_state.1.0, 1.0]
        distance = self.distance
        active_unit_index = 0
        opponent_index = 1

        while hps[0] > 0 and hps[1] > 0:
            active_unit = self.units[active_unit]

            if is_melee[active_unit_index]:
                # Melee action!
                if distance > active_unit.run_distance + 1:
                    distance -= active_unit.run_distance
                elif distance > 1:
                    hps[opponent_index] -= active_unit.damage_charge
                else:
                    hps[opponent_index] -= active_unit.damage_adjacent
            else:
                hps[opponent_index] -= active_unit.damage_ranged

            # Switch to next unit.
            active_unit_index ^= 1
            opponent_index ^= 1

        return hps



