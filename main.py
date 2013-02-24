from versus_simulator import VersusSimulator
from unit_factory import UnitFactory

def main():
    unit1 = UnitFactory.create_warrior()
    unit2 = UnitFactory.create_warrior()

    simulator = VersusSimulator(unit1, unit2)
    a1w1, a1w2 = simulator.determine_win_percentage(first_to_act=1)
    a2w1, a2w2 = simulator.determine_win_percentage(first_to_act=2)
    simulations_count = a1w1 + a1w2 + a2w1 + a2w2

    a1 = a1w1 + a1w2
    a2 = a2w1 + a2w2
    results = [
        (unit1, 100.0 * a1w1 / a1, 100.0 * a1w2 / a1),
        (unit2, 100.0 * a2w1 / a2, 100.0 * a2w2 / a2)
    ]

    # Print simulation report
    print '\n=====Simulation report=====\n'
    print '%r\n\tvs\n%r' % (unit1, unit2)
    print 'Results after running %d simulations:\n' % simulations_count

    for unit, wins1, wins2 in results:
        print 'When %s starts, winner is:' % unit

        if wins1 > wins2:
            winner = unit1
            win_percentage = wins1
        else:
            winner = unit2
            win_percentage = wins2
        print '%15s with %.0f%%' % (winner, win_percentage)

    wins_unit1 = a1w1 + a2w1
    wins_unit2 = a1w2 + a2w2
    if wins_unit1 > wins_unit2:
        winner = unit1
        wins_count = wins_unit1
    else:
        winner = unit2
        wins_count = wins_unit2

    win_percentage = 100.0 * wins_count / simulations_count
    print 'Overall winner: %s (%.0f%%)' % (winner, win_percentage)

    win_percentage_first = results[0][1] - results[1][1]
    print 'First unit to act has %+.0f%% chance to win' % win_percentage_first

    # print '\n=====Showing a single simulation=====\n'
    # simulator.simulate(verbosity=3)

if __name__ == '__main__':
    main()