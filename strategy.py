class MeleeRangedStrategy(object):
    """Compute how fast each opponent can kill the other using ranged attacks,
    and decide if you should play ranged or melee.

    Use-cases (you vs opponent):
      WW - Warrior vs Warrior
      WH - Warrior vs Hybrid
      WM - Warrior vs Mage

      MW - Mage vs Warrior
      MH - Mage vs Hybrid
      MM - Mage vs Mage

      HW - Hybrid vs Warrior
      HM - Hybrid vs Mage
      HH - Hybrid vs Hybrid
    """

    def __init__(self):
        pass

    def act(self, unit, game_state):
        # If I don't have any ranged capabilities, just fallback to melee.
        # This solves W*.
        if unit.spell_damage == 0:
            self._act_melee(unit, game_state)
            return

        # If I don't have any melee capabilities, just fallback to ranged.
        # This solves M*.
        if unit.damage == 0:
            self._act_ranged(unit, game_state)
            return

        # We can assume at this point that we have both melee and ranged
        # capabilities. We're trying to solve H*.
        # TODO - if this code would cover all cornercases, then it would also
        # solve W* and H*.
        raise NotImplemented()

    def _act_melee(self, unit, game_state):
        if game_state.distance == 1:
            # Adjacent, perform Full melee attack.
            game_state.attack_melee_full(unit)

        elif game_state.distance <= unit.move_distance + 1:
            # Move + single attack.
            game_state.move_towards(unit, game_state.distance-1)
            game_state.attack_melee(unit)

        elif game_state.distance <= unit.run_distance + 1:
            # Charge!
            game_state.charge(unit)

        else:
            game_state.move_towards(unit, unit.run_distance)

    def _act_ranged(self, unit, game_state):
        game_state.spell_cast(unit)
