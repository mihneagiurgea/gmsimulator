from versus_simulator import VersusSimulator
from unit_factory import UnitFactory

def main():
    unit1 = UnitFactory.create_hybrid()
    unit2 = UnitFactory.create_warrior()

    simulator = VersusSimulator(unit1, unit2)
    a1w1, a1w2 = simulator.determine_win_percentage(first_to_act=1)
    a2w1, a2w2 = simulator.determine_win_percentage(first_to_act=2)
    simulations_count = a1w1 + a1w2 + a2w1 + a2w2

    results = [
        (unit1, a1w1, a1w2),
        (unit2, a2w1, a2w2)
    ]

    # Print simulation report
    print '\n=====Simulation report=====\n'
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

    print '\n=====Showing a single simulation=====\n'
    simulator.simulate(verbosity=2)

if __name__ == '__main__':
    main()