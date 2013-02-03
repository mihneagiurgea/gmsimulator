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

class WarriorStrategy(BaseVersusStrategy):

    def act(self):
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