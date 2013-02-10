from collections import defaultdict

from versus_game_state import VersusGameState, AveragingVersusGameState
from versus_simulator import VersusSimulator
from unit_factory import UnitFactory
from strategy import MeleeRangedStrategy, InvalidVariant

import rules
import utils

def determine_optimum_strategies(unit1, unit2):
    outcomes = defaultdict(dict)

    for v1 in MeleeRangedStrategy.VARIANTS:
        try:
            strategy = MeleeRangedStrategy(unit1, v1)
        except InvalidVariant:
            continue
        unit1.strategy = strategy
        for v2 in MeleeRangedStrategy.VARIANTS:
            try:
                strategy = MeleeRangedStrategy(unit2, v2)
            except InvalidVariant:
                continue
            unit2.strategy = strategy

            turn_order = (unit1, unit2)
            game_state = AveragingVersusGameState(turn_order, verbosity=0)
            game_state.run_combat()

            outcomes[v1][v2] = game_state.hp_delta

    # What's your best strategy?
    unit_1_strategies = { v1: min(outcomes[v1].values()) for v1 in outcomes }
    unit1_strategy = utils.argmax(unit_1_strategies)
    unit2_strategy = utils.argmin(outcomes[unit1_strategy])

    for v1 in outcomes:
        for v2, hp_delta in sorted(outcomes[v1].items()):
            print '(%d, %d) => %+.2f' % (v1, v2, hp_delta)

    print '%s\'s strategy: %s' % (unit1, unit1_strategy)
    print '%s\'s strategy: %s' % (unit2, unit2_strategy)

def main():
    unit1 = UnitFactory.create_warrior()
    unit2 = UnitFactory.create_mage()

    simulator = VersusSimulator(unit1, unit2)
    a1w1, a1w2 = simulator.determine_win_percentage(first_to_act=1)
    a2w1, a2w2 = simulator.determine_win_percentage(first_to_act=2)
    simulations_count = a1w1 + a1w2 + a2w1 + a2w2

    results = [
        (unit1, a1w1, a1w2),
        (unit2, a2w1, a2w2)
    ]

    # Print simulation report
    print '=====Simulation report====='
    print '%r\n\tvs\n%r' % (unit1, unit2)
    print 'Results after running %d simulations:\n' % simulations_count

    for unit, wins1, wins2 in results:
        print 'When %s starts, winner is:' % unit

        total = wins1 + wins2
        if wins1 > wins2:
            winner = unit1
            wins_count = wins1
        else:
            winner = unit2
            wins_count = wins2
        win_percentage = 100.0 * wins_count / total
        print '%15s with %.0f%%' % (winner, win_percentage)

    # print 'We have a winner: %s' % simulator.simulate(debug=True)
    game_state = simulator.simulate_averaging(first_to_act=1)



if __name__ == '__main__':
    determine_optimum_strategies(UnitFactory.create_hybrid(), UnitFactory.create_hybrid())
    # main()