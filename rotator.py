#!/usr/bin/env python3
# Edward Parrish
# rotator.py

import sys


def main():
    # Commands
    PRINT = "print"
    GOAL = "goal"
    ACTIONS = "actions"
    WALK = "walk"
    WALK_LEN = len(WALK)

    COMMAND_LIST = [PRINT, GOAL, ACTIONS, WALK + "<i>"]

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
            print("given state \"" + tiles + "\" either does not meet the minimum row size requirement of " +
                  str(MIN_ROWS) + " or the minimum columns size requirment of " + str(MIN_COLS))
            exit("exiting")

    # Run actionable command line argument.
    if command == PRINT:
        s.print()

    elif command == GOAL:
        print(s.is_goal())

    elif command == ACTIONS:
        actionList = s.actions()
        for a in actionList:
            print(a)

    else:
        # Test walk command for valid integer.
        if len(command) >= WALK_LEN:
            walkStr = command[WALK_LEN:]

            # Test if no walk action number given.
            try:
                if len(walkStr) < 1:
                    raise ValueError()
            except:
                print("no walk action number given")
                exit("exiting")

            # Test if walk action is not positive integer.
            try:
                walkInt = int(walkStr)
                if walkInt < 0:
                    raise ValueError()
            except ValueError:
                print("walk action " + walkStr + " not a positive integer.")
                exit("exiting")

            s.walk(walkInt)

        else:
            print("command " + command +
                  " not recognized. available commands are: ")
            for c in COMMAND_LIST:
                print("  - " + c)
            exit("exiting")


class State:
    EMPTY_TILE = " "
    SEPARATOR = "|"
    DEFAULT_STATE = "12345|1234 |12354"
    ROTATE = "rotate"
    SLIDE = "slide"
    OPEN = "("
    CLOSE = ")"
    COMMA = ","
    LEFT = "-1"
    RIGHT = "1"

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
                    if self.tiles[j][i] != self.EMPTY_TILE and firstTile != self.EMPTY_TILE:
                        return False

        return True

    # Returns a sorted list of possible legal actions from current state.
    def actions(self):
        rotateActions = self.build_rotate_actions()
        slideActions = self.build_slide_actions()

        actions = rotateActions + slideActions
        actions.sort()

        return actions

    # Builds and returns a list of possible rotate actions for the current state.
    def build_rotate_actions(self):
        actions = []

        # Loop through rows.
        for i in range(len(self.tiles)):
            # Append rotate row left and right actions to action list.
            actions.append(self.get_rotate_str(str(i), self.LEFT))
            actions.append(self.get_rotate_str(str(i), self.RIGHT))

        return actions

    # Builds and returns a list of possible slide actions for the current state.
    def build_slide_actions(self):
        actions = []

        # Get the coordinates of the empty tile.
        emptyTileCoordinates = self.locate_empty_tile()

        # Test if coordinates of empty tile is not None.
        if emptyTileCoordinates is not None:
            x = str(emptyTileCoordinates[0])
            y2 = emptyTileCoordinates[1]
            numRows = len(self.tiles)

            # Test if empty tile is not in top row.
            if y2 > 0:
                # Calculate y index of tile to be slid into empty tile space.
                y = str(int(y2) - 1)
                # Append slide action.
                actions.append(self.get_slide_str(x, y, x, str(y2)))

            # Test if empty tile is not in bottom row.
            if y2 < numRows - 1:
                # Calculate y index of tile to be slid into empty tile space.
                y = str(int(y2) + 1)
                # Append slide action.
                actions.append(self.get_slide_str(x, y, x, str(y2)))

        return actions

    # Returns the string representation of a rotate action.
    def get_rotate_str(self, rowIndex, direction):
        return self.ROTATE + self.OPEN + rowIndex + self.COMMA + direction + self.CLOSE

    # Returns the string representation of a slide action.
    def get_slide_str(self, x, y, x2, y2):
        return self.SLIDE + self.OPEN + x + self.COMMA + y + self.COMMA + x2 + self.COMMA + y2 + self.CLOSE

    # Locates the empty tile in the rotator.
    # If the empty tile is found, then returns an array ([x, y]) of the x & y
    # coordinates of the empty tile, otherwise None.
    def locate_empty_tile(self):
        # Iterate through rows.
        for y in range(len(self.tiles)):
            row = self.tiles[y]
            # Iterate through tiles in row.
            for x in range(len(row)):
                if row[x] == self.EMPTY_TILE:
                    return [x, y]

        # If there is no empty tile, then return None.
        return None

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

            # If not last row, then append separator.
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
    def walk(self, actionNum):
        previousStates = []
        isNewState = True

        # Get possible actions given current state.
        actions = self.actions()

        # Test if action number argument in bounds.
        if self.actionNumIsInBounds(len(actions), actionNum):
            while isNewState:
                # Print the current state.
                self.print()

                # Clone the current state before executing action.
                clone = self.clone()

                # Append clone to previous state list.
                previousStates.append(clone)

                # Execute action on current state.
                self.execute(actionNum)

                for s in previousStates:
                    # Test if current state is equal to any previous state.
                    if self.__eq__(s):
                        isNewState = False
                        break

        else:
            # Report out of bounds action number.
            print("action number \"" + str(actionNum) +
                  "\" is invalid, enter action number as index (0 - " + str(len(actions) - 1) + ").")

    # Returns true if action number is in bounds, otherwise false.
    def actionNumIsInBounds(self, numPossibleActions, actionNum):
        # Test if action number argument in bounds.
        if actionNum >= 0 and actionNum < numPossibleActions:
            return True

        return False

    # Executes the action in the current state. This changes the current state
    # to a new state.
    def execute(self, actionNum):
        # Get possible actions given current state.
        actions = self.actions()

        # Test if action number argument in bounds.
        if self.actionNumIsInBounds(len(actions), actionNum):
            # Parse action name and arguments.
            actionArray = actions[actionNum].split(self.OPEN)
            actionName = actionArray[0]
            actionArgs = actionArray[1].rstrip(self.CLOSE).split(self.COMMA)

            # Cast action arguments to ints.
            for i in range(len(actionArgs)):
                actionArgs[i] = int(actionArgs[i])

            a = Actions(self)
            if actionName == self.ROTATE:
                a.rotate(actionArgs[0], actionArgs[1])

            elif actionName == self.SLIDE:
                a.slide(actionArgs[0], actionArgs[1], actionArgs[2], actionArgs[3])


class Actions:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        print("__str__()")

    def rotate(self, y, dx):
        row = self.state.tiles[y]
        numCols = len(row)
        newRow = [None] * numCols

        # Loop through tiles in row.
        for i in range(numCols):
            newIndex = i + dx
            # Test if new index is negative
            if newIndex < 0:
                newIndex = numCols - 1
            # Test if new index is greater than length
            elif newIndex >= numCols:
                newIndex = 0

            # Insert tile into the new index of the new row.
            newRow[newIndex] = row[i]

        # Overwrite old row with new.
        self.state.tiles[y] = newRow

    def slide(self, x, y, x2, y2):
        temp = self.state.tiles[y2][x2]
        self.state.tiles[y2][x2] = self.state.tiles[y][x]
        self.state.tiles[y][x] = temp


if __name__ == "__main__":
    main()
