from cube import Cube

import random
class Model:
    def __init__(self):
        pass
class IDAStar(Model):
    """
    Implements the Iterative Deepening A* (IDA*) search algorithm to solve a Rubik's Cube.
    """

    def __init__(self, threshold=20, heuristic=None):
        """
        Initializes the IDA* solver.

        Args:
            threshold (int): Initial threshold for the f-cost (g + h) in the search.
            heuristic (dict): Heuristic function to estimate the cost to reach the goal. Default is None.
        """

        self.max_threshold = threshold

        self.curr_threshold = threshold
        self.next_threshold = float('inf')

        self.heuristic = heuristic

        self.moves = []
        self.visited = set()

    def search(self, state, g_score):
        """
        Recursively searches for a solution within the current threshold.

        Args:
            state (tuple): The current state of the cube.
            g_score (int): The cost to reach the current state.

        Returns:
            bool: True if the solution is found, False otherwise.
        """

        if state in self.visited:
            return False
        self.visited.add(state)

        cube = Cube(state=state)

        if cube.complete():
            return True
        else:
            h_score = self.heuristic_(cube)
            f_score = g_score + h_score
            if f_score >= self.curr_threshold:
                self.next_threshold = min(self.next_threshold, f_score)
                return False
            else:
                random.shuffle(cube.actions)
                for action in cube.actions:
                    for i in range(cube.n):
                        twist = action[0]
                        move = action[1]

                        new_cube = Cube(state=cube.state)
                        if twist == "horizontal":
                            new_cube.horizontal_rotate(i, move)
                        if twist == "vertical":
                            new_cube.vertical_rotate(i, move)
                        if twist == "side":
                            new_cube.side_rotate(i, move)
                        self.moves.append(((twist, i, move), new_cube.state))
                        isSolved = self.search(new_cube.state, g_score+1)
                        if isSolved:
                            return True
                        self.moves.pop()
                        
                return False

    def heuristic_(self, cube):
        """
        Estimates the cost to reach the goal state.

        Args:
            cube (Cube): A Cube object representing the current configuration.

        Returns:
            int: Heuristic cost estimate based on the heuristic database.
        """
        
        return self.heuristic.get(cube.state, 0) if self.heuristic else 0
    
    def solve(self, state):
        """
        Initiates the IDA* search process to find a solution from the given state.

        Args:
            state (tuple): The starting state of the cube.

        Returns:
            list: A list of moves representing the solution path.
        """

        while True:
            isSolved = self.search(state, 0)
            if isSolved:
                return self.moves
            else:
                self.curr_threshold = self.next_threshold

                self.moves = []
                self.visited.clear()
                self.next_threshold = float('inf')
