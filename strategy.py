from collections import defaultdict

from versus_game_state import AveragingVersusGameState
import utils

def determine_optimum_variants(unit1, unit2):
    """Determines the optimum variants between two units."""
    # TODO - improve performance by considering variants (1,1) (1, 2) and (2,1)
    # as equivalent.
    outcomes = defaultdict(dict)

    for v1 in MeleeRangedStrategy.VARIANTS:
        if not MeleeRangedStrategy.is_compatible(unit1, v1):
            continue
        unit1.strategy = MeleeRangedStrategy(unit1, v1)
        for v2 in MeleeRangedStrategy.VARIANTS:
            if not MeleeRangedStrategy.is_compatible(unit2, v2):
                continue
            unit2.strategy = MeleeRangedStrategy(unit2, v2)

            turn_order = (unit1, unit2)
            game_state = AveragingVersusGameState(turn_order, verbosity=0)
            game_state.run_combat()

            outcomes[v1][v2] = game_state.hp_delta

    # What's your best strategy?
    unit_1_strategies = { v1: min(outcomes[v1].values()) for v1 in outcomes }
    unit1_strategy = utils.argmax(unit_1_strategies)
    unit2_strategy = utils.argmin(outcomes[unit1_strategy])

    # for v1 in outcomes:
    #     for v2, hp_delta in sorted(outcomes[v1].items()):
    #         print '(%d, %d) => %+.2f' % (v1, v2, hp_delta)

    # print '%s\'s strategy: %s' % (unit1, unit1_strategy)
    # print '%s\'s strategy: %s' % (unit2, unit2_strategy)

    return (unit1_strategy, unit2_strategy)

class MeleeRangedStrategy(object):
    """Compute how fast each opponent can kill the other using ranged attacks,
    and decide if you should play ranged or melee.

    This strategy focuses on when to stay ranged, and when to switch to melee.
    Three distance zones can be distinguished, based on the distance to your
    opponent:
      * Adjacent: distance = 1
      * Mid-range: when you are within charge distance from your opponent
        (distance <= run_distance + 1)
      * Long-range: outside of charge distance, distance > run_distance + 1

    Here are the options you can take in each of the 3 distance zones:
      * Adjacent -> choose the maximum damage you can deal now (between Full
        melee attack and spell cast)
      * Mid-ranged: choose between Charge (melee) and spell cast (ranged)
      * Long-ranged: choose between moving towards your opponent (melee) and
        spell cast (ranged)

    So, there are 3 distinct possible variants, based on when to switch to
    Melee vs when to remain Ranged:

                | Adjacent | Mid-range | Long-range |
    -------------------------------------------------
    Pure Ranged | best(M/R)| Ranged    | Ranged     |
    Hybrid      | Melee    | Melee     | Ranged     |
    Pure Melee  | Melee    | Melee     | Melee      |

    (all other possible combinations are strictly inferior)
    """

    PURE_RANGED = 1
    HYBRID = PURE_RANGED + 1
    PURE_MELEE = HYBRID + 1
    VARIANTS = (PURE_RANGED, HYBRID, PURE_MELEE)

    @classmethod
    def is_compatible(cls, unit, variant):
        """Determines if a unit is compatible a strategy variant."""
        if variant not in MeleeRangedStrategy.VARIANTS:
            raise ValueError('Invalid variant: %r' % variant)
        # Validate that this is a correct variant value, with respect
        # to the current unit.
        if unit.damage == 0 and variant != MeleeRangedStrategy.PURE_RANGED:
            return False
        if unit.spell_damage == 0 and variant != MeleeRangedStrategy.PURE_MELEE:
            return False
        return True

    def __init__(self, unit, variant):
        # Validate that this is a correct variant value, with respect
        # to the current unit.
        if not self.is_compatible(unit, variant):
            raise ValueError('Invalid variant %d for %r' % (variant, unit))

        self.variant = variant

    def __str__(self):
        #HACK - this should be improved.
        if self.variant == self.PURE_RANGED:
            return 'Pure Ranged'
        elif self.variant == self.HYBRID:
            return 'Hybrid'
        elif self.variant == self.PURE_MELEE:
            return 'Pure Melee'
        else:
            return 'Unknown variant: %s' % self.variant

    def _variant(self, mid_range=False, long_range=False):
        """Should you switch to melee yet?"""
        if mid_range and not long_range:
            return self.variant >= MeleeRangedStrategy.HYBRID

        if long_range and not mid_range:
            return self.variant == MeleeRangedStrategy.PURE_MELEE

        raise ValueError('Choose mid_range XOR long_range')

    def _act_adjacent(self, unit, game_state):
        dmg_melee = game_state.get_dps_full_melee(unit)
        dmg_ranged = game_state.get_dps_spell_cast(unit)
        if dmg_melee >= dmg_ranged:
            game_state.attack_full_melee(unit)
        else:
            game_state.spell_cast(unit)

    def _act_mid_range(self, unit, game_state):
        use_melee = self._variant(mid_range=True)
        if use_melee:

            # Am I close enough to just move and make a single attack?
            if game_state.distance <= unit.move_distance + 1:
                game_state.move_towards(unit, game_state.distance-1)
                game_state.attack_melee(unit)

            else:
                game_state.charge(unit)

        else:
            game_state.spell_cast(unit)

    def _act_long_range(self, unit, game_state):
        use_melee = self._variant(long_range=True)
        if use_melee:
            game_state.move_towards(unit, unit.run_distance)
        else:
            game_state.spell_cast(unit)

    def act(self, unit, game_state):
        if game_state.distance == 1:
            self._act_adjacent(unit, game_state)

        elif game_state.distance <= unit.run_distance + 1:
            self._act_mid_range(unit, game_state)

        else:
            self._act_long_range(unit, game_state)
