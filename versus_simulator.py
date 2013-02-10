import random

from versus_game_state import VersusGameState
import strategy

class VersusSimulator(object):
    """Versus (1v1) simulator"""

    def __init__(self, unit1, unit2):
        # Determine the optimum strategies that should be used between
        # these two units, taking the starting unit into account.
        variants1 = strategy.determine_optimum_variants(unit1, unit2)
        variants2 = strategy.determine_optimum_variants(unit2, unit1)
        # I think in theory variants might differ, depending on the starting
        # unit. Assume they don't differ, because it simplifies implementation.
        if variants1 != tuple(reversed(variants2)):
            raise Exception('Different variants %s != %s' % (variants1, variants2))
        unit1.strategy = strategy.MeleeRangedStrategy(unit1, variants1[0])
        unit2.strategy = strategy.MeleeRangedStrategy(unit2, variants1[1])

        print 'Determined optimum strategies:'
        print '\t%s - %s' % (unit1, unit1.strategy)
        print '\t%s - %s' % (unit2, unit2.strategy)

        self.unit1 = unit1
        self.unit2 = unit2

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

    def simulate(self, first_to_act=None, verbosity=0):
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

        game_state = VersusGameState(turn_order, verbosity=verbosity)
        game_state.run_combat()

        # Combat has ended, we have a winner.
        return game_state.winner
