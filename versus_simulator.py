import random

from versus_game_state import VersusGameState, AveragingVersusGameState

class VersusSimulator(object):
    """Versus (1v1) simulator"""

    def __init__(self, unit1, unit2, distance=None):
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

        game_state = VersusGameState(turn_order, self.distance, debug=debug)
        game_state.run_combat()

        # Combat has ended, we have a winner.
        return game_state.winner
