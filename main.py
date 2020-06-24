from Q_learning import QLearning
from World import World
from argparse import ArgumentParser
from time import time, sleep

if __name__ == "__main__":
    parser = ArgumentParser(description='Implementation of Q-learning algorithm'
                                                 'using GridWorld environment. Use -h for more informations.')
    parser.add_argument('world_filename', help="Chosen world filename. Eg. \"world1.txt\"")
    parser.add_argument('-q', '--qrun', action="store_true", help="Run Q-learning algorithm for 10000 iteration."
                                                                  "To change number of iteration use: -qi [num]")
    parser.add_argument('-qi', '--qiter', help="Change number of iteration for Q-learning algorithm. Use: -qi [num]",
                        type=int, default=10000, required=False)
    parser.add_argument('-sh', '--show', action="store_true", help="Show figures")
    parser.add_argument('-s', '--save', action="store_true", help="Save figures and data to tmp.*"
                                                                  " To change filename use: -sfn [filename]")
    parser.add_argument('-sfn', '--save_filename', help="Change saved figures file names. Use -sfn [filename]"
                                                        " (DO NOT USE FILE EXTENSION!)", default="tmp", required=False)
    args = parser.parse_args()

    print("*********** PARSER INFO **************")
    print("World filename: ", args.world_filename)
    print("Run Qlearing: ", args.qrun)
    print("Q-learing iterations: ", args.qiter)
    print("Show figures: ", args.show)
    print("Save figures: ", args.save)
    print("Figures filename: ", args.save_filename)
    print("***************************************")

    #######################################################################################################  EXECUTION

    if args.qrun is False:
        print("ERROR: At least [-q] option have to be use to execute this program!")
    else:
        world = World()
        world.readFile(str(args.world_filename))
        world.showWorldValues()

        if args.qrun:
            print("\n\n############## Q-Learning ###############")
            print("Number of iterations: ", args.qiter)
            qlearning = QLearning(world)
            start_time = time()
            qtable = qlearning.qLearning(args.qiter)
            elapsed_time = time() - start_time
            print("Q-learning time: ", elapsed_time)
            print("++ Q-table ++")
            qlearning.printQTableText(qtable)
            q_utilities, q_policy = qlearning.extractUtilitiesAndPolicy(qtable)
            print("\n ++ Utilities and Policy ++")
            world.plotUtilitiesActionText(q_utilities, q_policy)

            if args.show is True and args.save is False:
                util_plot = world.plotUtilities(q_utilities, "q")
                policy_plot = world.plotPolicy(q_policy, "q")
                policy_plot.show()
                sleep(1)

            if args.save is True:
                util_plot = world.plotUtilities(q_utilities, "q")
                world.saveUtilitiesPlot(util_plot, str(args.save_filename), "q")
                policy_plot = world.plotPolicy(q_policy, "q")
                world.savePolicyPlot(policy_plot, str(args.save_filename), "q")
                if args.show is True:
                    policy_plot.show()
