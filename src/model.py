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

        self.curr_threshold = 0
        self.next_threshold = float('inf')

        self.heuristic = heuristic

        self.moves = []

    def search(self, state, g_score):
        """
        Recursively searches for a solution within the current threshold.

        Args:
            state (tuple): The current state of the cube.
            g_score (int): The cost to reach the current state.

        Returns:
            bool: True if the solution is found, False otherwise.
        """

        cube = Cube(state=state)

        h_score = self.heuristic_(cube)
        f_score = g_score + h_score

        if f_score > self.curr_threshold:
            self.next_threshold = min(self.next_threshold, f_score)
            return False
        
        if cube.complete():
            return True
        
        next_moves = []
        for action in cube.actions:
            for i in range(cube.n):
                new_cube = Cube(state=cube.state)

                twist = action[0]
                move = action[1]

                # apply the move
                if twist == "horizontal":
                    inverse_move = "right" if move == "left" else "left"
                    if self.moves and self.moves[-1][0] == (twist, i, inverse_move):
                        continue
                    new_cube.horizontal_rotate(i, move)
                elif twist == "vertical":
                    inverse_move = "down" if move == "up" else "up"
                    if self.moves and self.moves[-1][0] == (twist, i, inverse_move):
                        continue
                    new_cube.vertical_rotate(i, move)
                elif twist == "side":
                    inverse_move = "negative" if move == "positive" else "positive"
                    if self.moves and self.moves[-1][0] == (twist, i, inverse_move):
                        continue
                    new_cube.side_rotate(i, move)

                # calculate the heuristic cost
                h_score = self.heuristic_(new_cube)
                f_score = (g_score + 1) + h_score
                next_moves.append((f_score, (twist, i, move), new_cube.state))

        sorted_moves = sorted(next_moves, key=lambda x: x[0], reverse=False)
        
        for f_score_, (twist, i, move), new_state in sorted_moves:
            self.moves.append(((twist, i, move), new_state))

            isSolved = self.search(new_state, g_score+1)
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

        def simpler_heuristic_(cube):
            """
            Calculates the number of misplaced pieces on the Rubik's Cube for a simple heuristic.

            Args:
                cube (Cube): An instance of the Cube class representing the current state of the Rubik's Cube.
                            The Cube class should have the attributes `config` (the current configuration of the cube)

            Returns:
                int: The number of misplaced pieces across all faces of the cube.
            """

            misplaced_pieces = 0
            for k in range(6):
                face_color = cube.config[k][cube.n // 2][cube.n // 2]
                for i in range(cube.n):
                    for j in range(cube.n):
                        if cube.config[k][i][j] != face_color:
                            misplaced_pieces += 1
            
            return misplaced_pieces
        
        return self.heuristic.get(cube.state, simpler_heuristic_(cube)) if self.heuristic else simpler_heuristic_(cube)
    
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
                self.next_threshold = float('inf')
