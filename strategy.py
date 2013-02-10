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
        # Validate that this is a correct variant value, with respect
        # to the current unit.
        if unit.damage == 0 and variant != MeleeRangedStrategy.PURE_RANGED:
            return False
        if unit.spell_damage == 0 and variant != MeleeRangedStrategy.PURE_MELEE:
            return False
        return True

    def __init__(self, unit, variant=None):
        if variant is None:
            if unit.damage == 0:
                variant = MeleeRangedStrategy.PURE_RANGED
            elif unit.spell_damage == 0:
                variant = MeleeRangedStrategy.PURE_MELEE
            else:
                variant = MeleeRangedStrategy.HYBRID

        if variant not in MeleeRangedStrategy.VARIANTS:
            raise ValueError('Invalid variant: %r' % variant)

        # Validate that this is a correct variant value, with respect
        # to the current unit.
        if not self.is_compatible(unit, variant):
            raise ValueError('Invalid variant %d for %r' % (variant, unit))

        self.variant = variant

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
