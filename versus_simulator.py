import random

from versus_game_state import VersusGameState

MAP_WIDTH = 24

class VersusSimulator(object):
    """Versus (1v1) simulator"""

    def __init__(self, unit1, unit2, distance=MAP_WIDTH-1):
        """
        Args:
            distance: The distance between the 2 fighting units (equal to
                Euclidean distance between their positions, so adjacent units
                ar at distance 1, not 0).
        """
        self.unit1 = unit1
        self.unit2 = unit2
        self.distance = distance

    def determine_win_percentage(self, first_to_act=None, simulation_count=250):
        """Determines the win percentage of each unit/strategy pair.

        Args:
            first_to_act: what's the first unit to act (1 or 2), or None, for
                a random initiative order
        """
        wins1 = 0
        wins2 = 0
        for i in xrange(simulation_count):
            winner = self.simulate(first_to_act=first_to_act)
            if winner == self.unit1:
                wins1 += 1
            elif winner == self.unit2:
                wins2 += 1
            else:
                raise ValueError('Invalid winner: %s' % winner)

        # print 'Win ratio: %d vs %d' % (wins1, wins2)
        return wins1, wins2

    def simulate(self, first_to_act=None, debug=False):
        """Simulation a single combat.

        Returns:
            A dict containing the simulation result.
        """
        if first_to_act is None:
            first_to_act = random.randint(1, 2)
        turn_order = [self.unit1, self.unit2]
        # Randomize turn order, if needed.
        if first_to_act == 2:
            turn_order.reverse()

        self.game_state = VersusGameState(turn_order, self.distance)

        if debug:
            print('\tTurn order:\n1. %s\n2. %s' % (turn_order[0], turn_order[1]))

        # Fight!
        while self.game_state.alive:
            unit = self.game_state.active_unit
            unit.act(self.game_state)
            self.game_state.next_turn()

            if debug:
                print self.game_state

        # Combat has ended, we have a winner.
        return self.game_state.winner
