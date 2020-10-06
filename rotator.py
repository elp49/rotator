#!/usr/bin/python

import sys


def main():
    # Commands
    PRINT = "print"
    GOAL = "goal"
    ACTIONS = "actions"
    WALK = "walk"
    WALK_LEN = len(WALK)

    MIN_ROWS = 2
    MIN_COLS = 2
    numArgs = len(sys.argv)

    # Test if no command given
    if numArgs < 2:
        print("no command given")
        exit("exiting")
    else:
        command = sys.argv[1]

    # Test if no state given
    if numArgs < 3:
        s = State()
    else:
        tiles = sys.argv[2]
        s = State(tiles)

        # Test if state meets minimum size requirement
        if len(s.tiles) < MIN_ROWS or len(s.tiles[0]) < MIN_COLS:
            print("given state \"" + tiles + "\" either does not meet the " +
                  "minimum row size requirement of " + str(MIN_ROWS) + " or the " +
                  "minimum columns size requirment of " + str(MIN_COLS))
            exit("exiting")

    # Run actionable command line argument.
    if command == PRINT:
        s.print()
    elif command == GOAL:
        print(s.is_goal())
    elif command == ACTIONS:
        s.actions()
    elif command[0:WALK_LEN] == WALK:
        s.walk(command[WALK_LEN:])


    # Test code
    """ print("command: " + command)
    print("tileStr: " + s.tileStr)

    print("tiles: ")
    for row in s.tiles:
        print(row)

    print("Test __str_() and print(): ")
    s.print()

    print("Test clone(): ")
    clone = s.clone()
    clone.print()

    print("Test __eq__(): ")
    print(s.__eq__(clone))

    print("Test is_goal():")
    print(s.is_goal()) """


class State:
    EMPTY_TILE = " "
    SEPARATOR = "|"
    DEFAULT_STATE = "12345|1234 |12354"

    def __init__(self, tileStr=DEFAULT_STATE):
        self.tileStr = tileStr
        self.tiles = []
        self.initialize()

    # Initializes the current state by parsing the state string and creating
    # an matrix representation of the tiles.
    def initialize(self):
        for row in self.tileStr.split(self.SEPARATOR):
            col = []

            for t in row:
                col.append(t)

            self.tiles.append(col)

    # Prints the current state to the console.
    def print(self):
        print(self.__str__())

    # Checks whether the current state is a solution state.
    # Returns true if it is a solution state, otherwise false.
    def is_goal(self):
        numRows = len(self.tiles)
        numCols = len(self.tiles[0])

        # Loop for each tile in a column.
        for i in range(numCols):
            firstTile = self.tiles[0][i]
            # Loop through each row.
            for j in range(1, numRows):
                # Test if tile in a column is not in solution state.
                if self.tiles[j][i] != firstTile:
                    # If the tiles are not equal, then test if it is not empty.
                    if self.tiles[j][i] != self.EMPTY_TILE \
                            and firstTile != self.EMPTY_TILE:
                        return False

        return True

    # Returns a sorted list of possible legal actions from current state.
    def actions(self):
        print("Returns a sorted list of possible legal actions from current" +
              "state.")

    # Executes the action in the current state. This changes the current state
    # to a new state.
    def execute(self, action):
        print("executing action.")

    # Returns a string representation of the current state.
    def __str__(self):
        stateStr = ""
        numRows = len(self.tiles)
        i = 0

        # Append the tiles in each row to state string.
        for row in self.tiles:
            i += 1
            for t in row:
                stateStr += t

            # If not last row, then separator.
            if i != numRows:
                stateStr += self.SEPARATOR

        return stateStr

    # Checks whether the current state is equal to another state.
    # Returns true if the two states are equal, otherwise false.
    def __eq__(self, state):
        numRows = len(self.tiles)
        numCols = len(self.tiles[0])

        # Test if the two states have different number of rows or columns.
        if numRows != len(state.tiles) or numCols != len(state.tiles[0]):
            return False

        i = 0
        # Loop through rows.
        for row in self.tiles:
            j = 0
            # Loop through tiles in row.
            for t in row:
                # Test if the two states are not equal.
                if t != state.tiles[i][j]:
                    return False

                j += 1

            i += 1

        return True

    # Returns a cloned instance of the current state.
    def clone(self):
        return State(self.__str__())

    # Starts with the current state, prints the state, gets its possible
    # actions, executes actions[i], and iterates. It continues to iterate until
    # it arrives at a state that has already been seen, and then stops.
    def walk(self, rowNum):
        # Test rowNum is not of type string.
        if type(rowNum) != str:
            raise TypeError("parameter 1 in walk(rowNum) is not of type string.")

        # Test rowNum has length less than 1.
        if len(rowNum) < 1:
            raise ValueError("parameter 1 in walk(rowNum) is empty.")

        print("walking " + rowNum)


class Actions:
    def __init__(self, tiles):
        print("creating actions for tiles: " + tiles)

    def __str__(self):
        print("__str__()")


if __name__ == "__main__":
    main()
