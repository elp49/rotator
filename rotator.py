#!/usr/bin/python

import sys

def main():
    if len(sys.argv) < 2:
        print("no command given")
        exit()

    command = sys.argv[1]
    print("command: " + command)

    s = State(sys.argv[2])
    print("tiles: " + s.tiles)

    print("initialize: ")
    s.initialize()


class State:
    def __init__(self, tiles="12345|1234 |12354"):
        self.tiles = tiles
        self.initialize()

    def initialize(self):
        print(self.tiles)

if __name__ == "__main__":
    main()