# rotator

Usage: python3 rotator.py [OPTION]... [STATE]...
Simulates a rotator puzzle.
Options are mandatory to run the program, however if a state is not given then
the default state of "12345|1234 |12354" will be used. States must have at least
two columns and two rows.

Available options
    print               displays the current state
    goal                displays "True" if the current state is a solution
                        state, otherwise false.
    actions             displays all possible actions from the current state.
                        available actions are: rotate and slide. 
    walk<i>             displays the current state, executes actions[i] (where
                        i=0 is the first action), and continues to iterate until
                        it arrives at a state that has already been seen.
