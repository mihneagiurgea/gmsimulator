class BaseVersusStrategy(object):
    """Base unit strategy for 1v1 combat."""

    def __init__(self, unit, game_state):
        self.unit = unit
        self.game_state = game_state
        self.opponent = game_state.get_opponent(unit)

    def act(self):
        raise NotImplemented()

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, self.unit)


class MeleeRangedStrategy(BaseVersusStrategy):
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

    def act(self):
        # If I don't have any ranged capabilities, just fallback to melee.
        # This solves W*.
        if self.unit.spell_damage == 0:
            self._act_melee()


        # If I don't have any melee capabilities, just fallback to ranged.
        # This solves M*.
        if self.unit.melee_damage == 0:
            self._act_ranged()

        # We can assume at this point that we have both melee and ranged
        # capabilities. We're trying to solve H*.
        # TODO - if this code would cover all cornercases, then it would also
        # solve W* and H*.


        # How fast can I kill you using spells?
        ttk_spell_cast_me = self.game_state.ttk_spell_cast(self.unit, self.opponent)
        # How fast can the opponent kill me using spells?
        ttk_spell_cast_opp = self.game_state.ttk_spell_cast(self.opponent, self.unit)

        if ttk_spell_cast_me > ttk_spell_cast_opp:
            # If I can kill you using spells faster than you can kill me,
            # then I'll just nuke you!
            # This solves cases 4, 5, 6
            self._act_ranged()


    def _act_melee(self):
        if self.game_state.distance == 1:
            # Adjacent, perform Full melee attack.
            self.game_state.attack_melee_full(self.unit, self.opponent)

        elif self.game_state.distance <= self.unit.move_distance + 1:
            # Move + single attack.
            self.game_state.move_towards(self.unit, self.game_state.distance-1)
            self.game_state.attack_melee(self.unit, self.opponent)

        elif self.game_state.distance <= self.unit.run_distance + 1:
            # Charge!
            self.game_state.charge(self.unit, self.opponent)

        else:
            self.game_state.move_towards(self.unit, self.unit.run_distance)

    def _act_ranged(self):
        self.game_state.spell_cast(self.unit, self.opponent)
