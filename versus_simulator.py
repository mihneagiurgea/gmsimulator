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
        self.game_state = VersusGameState(self.unit1, self.unit2, self.distance)

        strategy1 = self.unit1.get_strategy(self.game_state)
        strategy2 = self.unit2.get_strategy(self.game_state)

        # Randomize turn order.
        if first_to_act is None:
            first_to_act = random.randint(1, 2)
        turn_order = [strategy1, strategy2]
        if first_to_act == 2:
            turn_order.reverse()

        if debug:
            print('\tTurn order:\n1. %s\n2. %s' % (turn_order[0], turn_order[1]))

        # Fight!
        while self.game_state.alive:
            # New round.
            self.game_state.round += 1

            for strategy in turn_order:
                strategy.act()
                if not self.game_state.alive:
                    break

            if debug:
                print self.game_state

        # Combat has ended, we have a winner.
        if self.game_state.current_hp[self.unit1] > 0:
            winner = self.unit1
        else:
            winner = self.unit2

        return winner
