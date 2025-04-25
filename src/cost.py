from cube import Cube

import tqdm

class Cost:
    """
    Pre-computes a heuristic database for a Rubik's Cube of size `n` using BFS traversal.
    
    Attributes:
        n (int): Dimension of the cube (default: 3).
        max_depth (int): Maximum search depth for heuristic generation.
        heuristic (dict): Mapping from cube state to minimal number of moves from solved state.
    """

    def __init__(self, n=3, max_depth=20):
        """
        Initializes the Cost object and pre-computes the heuristic table.

        Args:
            n (int, optional): Cube size. Defaults to 3.
            max_depth (int, optional): Depth limit for BFS. Defaults to 20.
        """

        self.n = n
        self.max_depth = max_depth

        self.heuristic = self.heuristic_()

    def heuristic_(self):
        """
        Generates a heuristic lookup table using BFS from the solved cube state.
        
        Returns:
            dict: A dictionary mapping cube states to minimal depth (number of moves).
        """
        
        cube = Cube(self.n)

        queue = [(cube.state, 0)]
        heuristic = {cube.state: 0}
        max_node_count = sum([(len(cube.actions) * cube.n) ** (i+1) for i in range(self.max_depth+1)])

        with tqdm.tqdm(total=max_node_count, desc="Heuristic Database") as progress_bar:
            while queue:
                state, depth = queue.pop()
                if depth > self.max_depth:
                    continue

                for action in cube.actions:
                    for i in range(cube.n):
                        twist = action[0]
                        move = action[1]

                        new_cube = Cube(state=state)
                        if twist == "horizontal":
                            new_cube.horizontal_rotate(i, move)
                        if twist == "vertical":
                            new_cube.vertical_rotate(i, move)
                        if twist == "side":
                            new_cube.side_rotate(i, move)

                        if new_cube.state not in heuristic:
                            heuristic[new_cube.state] = depth + 1

                        if heuristic[new_cube.state] > depth + 1:
                            heuristic[new_cube.state] = depth + 1

                        if new_cube.state not in queue:
                            queue.append((new_cube.state, depth + 1))
                        progress_bar.update(1)

        return heuristic
