from versus_simulator import VersusSimulator
from unit_factory import UnitFactory
from strategy import WarriorStrategy

def main():
    unit1 = UnitFactory.create_warrior()
    unit2 = UnitFactory.create_malak()

    simulator = VersusSimulator(unit1, WarriorStrategy, unit2, WarriorStrategy)
    wins1, wins2 = simulator.determine_win_percentage()

    # Print simulation report
    print '=====Simulation report====='
    print '%r\n\tvs\n%r' % (unit1, unit2)

    if wins1 == wins2:
        print 'It was a tie: %d vs %d wins' % (wins1, wins2)
    else:
        total = wins1 + wins2
        if wins1 > wins2:
            winner = unit1
            wins_count = wins1
        else:
            winner = unit2
            wins_count = wins2
        win_percentage = 100.0 * wins_count / total
        print 'Overall winner: %s' % winner
        print 'Win percentage: %.2f%% (%d/%d)' % \
              (win_percentage, wins_count, total)
    # print 'We have a winner: %s' % simulator.simulate()

if __name__ == '__main__':
    main()