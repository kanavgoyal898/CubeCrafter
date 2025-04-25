from cube import Cube

class IterativeDeepeningAStar:
    """
    Implements the Iterative Deepening A* (IDA*) search algorithm to solve a Rubik's Cube.
    """

    def __init__(self, threshold=20):
        """
        Initializes the IDA* solver.

        Args:
            threshold (int): Initial threshold for the f-cost (g + h) in the search.
        """

        self.max_threshold = threshold

        self.curr_threshold = threshold
        self.next_threshold = float('inf')

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
            print(cube.state)
            return True
        else:
            h_score = self.heuristic(cube)
            f_score = g_score + h_score
            if f_score >= self.curr_threshold:
                self.next_threshold = min(self.next_threshold, f_score)
                return False
            else:
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
                        self.moves.append((twist, i, move))
                        isSolved = self.search(new_cube.state, g_score+1)
                        if isSolved:
                            return True
                        self.moves.pop()
                        
                return False

    def heuristic(self, cube):
        """
        Estimates the cost to reach the goal state.

        Args:
            cube (Cube): A Cube object representing the current configuration.

        Returns:
            int: Heuristic cost estimate (number of misplaced pieces).
        """
        
        config = cube.config
        return 0
    
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

cube = Cube()
moves = cube.shuffle(1, 1)
print("Shuffling...")
print(f"Shuffled in {len(moves)} moves: {moves}")
print("Solving...")
model = IterativeDeepeningAStar(threshold=20)
solution = model.solve(cube.state)
print(f"Solved in {len(solution)} moves: {solution}")
