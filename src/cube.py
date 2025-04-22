import random

class Cube:
    """
    A class representing a Rubik's Cube with customizable size and initial face colors.

    Attributes:
        n (int): Dimension of the cube (e.g., 3 for 3x3).
        colors (list): List of color initials for each face.
        faces (list): List of face names in standard cube orientation.
        config (list): 3D list storing color configuration for each face.
    """

    def __init__(self, n=3):
        """
        Initializes the Cube with uniform color configuration for each face.

        Args:
            n (int): Size of each face (default is 3 for a standard 3x3 cube).
        """
        
        self.n = n
        self.colors = ['W', 'G', 'R', 'B', 'O', 'Y']
        self.faces = ['Up', 'Left', 'Front', 'Right', 'Back', 'Down']
        self.reset()

    def __str__(self):
        """
        Returns a formatted string representation of the cube's face configurations.

        Returns:
            str: Readable layout of all six cube faces with their respective color rows.
        """

        result = []
        for face_name, face_config in zip(self.faces, self.config):
            result.append(f'{face_name} Face:')
            result.extend([' '.join(row_config) for row_config in face_config])
            result.append('')
        return '\n' + '\n'.join(result)

    def reset(self):
        """
        Resets the cube to its initial state.
        The cube faces are initialized with uniform color (or digits for top and bottom).
        """

        self.config = [[[color for _ in range(self.n)] for _ in range(self.n)] for color in self.colors]

        # horizontal rotate testing
        # self.config[0] = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]  # Up
        # self.config[5] = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]  # Down

        # vertical rotate testing
        # self.config[1] = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]  # Left
        # self.config[3] = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]  # Right

        # side rotate testing
        # self.config[2] = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]  # Front
        # self.config[4] = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]  # Back

    def is_solved(self):
        """
        Determines if the Rubik's Cube is solved by checking if each face consists of a single color.
        
        Returns:
            bool: True if the Rubik's Cube is solved (all faces have a single color), 
                  False otherwise.
        """

        def flatten(lst):
            """
            Flattens a nested list structure into a set of unique elements.
            
            This helper function takes a list (which may contain nested lists) and flattens it
            into a set of unique elements. It is used to check if all elements on a face are the
            same color.
            
            Args:
                lst (list): A list which may contain nested lists.
                
            Returns:
                set: A set containing the unique elements found in the list.
            """

            result = set()

            for ls in lst:
                if isinstance(ls, list):
                    result.update(flatten(ls))
                else:
                    result.add(ls)

            return result
        
        isSolved = True

        for face in self.config:
            if len(flatten(face)) != 1:
                isSolved = False
                break

        return isSolved
    
    def shuffle(self, lower_limit, upper_limit):
        """
        Shuffles the Rubik's Cube by performing a random series of rotations.

        Args:
            lower_limit (int): The minimum number of moves to shuffle the cube.
            upper_limit (int): The maximum number of moves to shuffle the cube.

        Raises:
            ValueError: 
                - If `lower_limit` or `upper_limit` is negative.
                - If `lower_limit` is greater than `upper_limit`.
        """
        
        if lower_limit < 0 or upper_limit < 0:
            raise ValueError("Limits must be non-negative.")
        if lower_limit > upper_limit:
            raise ValueError("Lower limit must be less than or equal to upper limit.")
        

        moves_count = random.randint(lower_limit, upper_limit)

        actions = [
            ('horizontal', 'left'),
            ('horizontal', 'right'),
            ('vertical', 'up'),
            ('vertical', 'down'),
            ('side', 'positive'),
            ('side', 'negative')
        ]

        for _ in range(moves_count):
            action = random.choice(actions)

            i = random.randint(0, self.n - 1)

            twist = action[0]
            move = action[1]

            if twist == 'horizontal':
                self.horizontal_rotate(i, move)
            if twist == 'vertical':
                self.vertical_rotate(i, move)
            if twist == 'side':
                self.side_rotate(i, move)

    def horizontal_rotate(self, row, direction):
        """
        Performs a horizontal rotation of the specified row across the four lateral faces.
        If the row is the top or bottom, the Up or Down face is rotated accordingly.

        Time Complexity:
            O(1)
        Space Complexity:
            O(n*n)

        Args:
            row (int): The index of the row to rotate (0-based).
            direction (str): Direction of rotation, either 'left' or 'right'.

        Raises:
            ValueError: If row is out of bounds or direction is invalid.
        """

        if row < 0 or row >= self.n:
            raise ValueError("Row index out of bounds.")
        if direction not in ['left', 'right']:
            raise ValueError("Direction must be 'left' or 'right'.")

        face_1, face_2, face_3, face_4 = self.config[1], self.config[2], self.config[3], self.config[4]

        if direction == 'left':
            self.config[1][row], self.config[2][row], self.config[3][row], self.config[4][row] = face_2[row], face_3[row], face_4[row], face_1[row]
            if row == 0:
                # clockwise rotation for the top row
                self.config[0] = [list(row) for row in zip(*reversed(self.config[0]))]
            if row == self.n - 1:
                # counter-clockwise rotation for the bottom row
                self.config[5] = [list(row) for row in zip(*self.config[5])][::-1]

        if direction == 'right':
            self.config[1][row], self.config[2][row], self.config[3][row], self.config[4][row] = face_4[row], face_1[row], face_2[row], face_3[row]
            if row == 0:
                # counter-clockwise rotation for the top row
                self.config[0] = ([list(row) for row in zip(*self.config[0])])[::-1]
            if row == self.n - 1:
                # clockwise rotation for the bottom row
                self.config[5] = ([list(row) for row in zip(*reversed(self.config[5]))])

    def vertical_rotate(self, col, direction):
        """
        Performs a vertical rotation of the specified column across the four lateral faces.
        If the column is the left or right, the Left or Right face is rotated accordingly.

        Time Complexity:
            O(n)
        Space Complexity:
            O(n*n)

        Args:
            col (int): The index of the column to rotate (0-based).
            direction (str): Direction of rotation, either 'up' or 'down'.

        Raises:
            ValueError: If column is out of bounds or direction is invalid.
        """

        if col < 0 or col >= self.n:
            raise ValueError("Column index out of bounds.")
        if direction not in ['up', 'down']:
            raise ValueError("Direction must be 'up' or 'down'.")
        
        face_1, face_2, face_3, face_4 = self.config[0], self.config[2], self.config[5], self.config[4]

        if direction == 'up':
            for i in range(self.n):
                self.config[0][i][col], self.config[2][i][col], self.config[5][i][col], self.config[4][i][col] = face_2[i][col], face_3[i][col], face_4[i][col], face_1[i][col] 
            if col == 0:
                # counter-clockwise rotation for the left column
                self.config[1] = [list(row) for row in zip(*self.config[1])][::-1]
            if col == self.n - 1:
                # clockwise rotation for the right column
                self.config[3] = [list(row) for row in zip(*reversed(self.config[3]))]

        if direction == 'down':
            for i in range(self.n):
                self.config[0][i][col], self.config[2][i][col], self.config[5][i][col], self.config[4][i][col] = face_4[i][col], face_1[i][col], face_2[i][col], face_3[i][col]
            if col == 0:
                # clockwise rotation for the left column
                self.config[1] = [list(row) for row in zip(*reversed(self.config[1]))]
            if col == self.n - 1:
                # counter-clockwise rotation for the right column
                self.config[3] = [list(row) for row in zip(*self.config[3])][::-1]

    def side_rotate(self, dpt, direction):
        """
        Performs a side rotation of the specified depth across the four lateral faces.
        If the depth is the front or back, the Front or Back face is rotated accordingly.

        Time Complexity:
            O(n)
        Space Complexity:
            O(n*n)

        Args:
            dpt (int): The index of the depth to rotate (0-based).
            direction (str): Direction of rotation, either 'positive' or 'negative'.

        Raises:
            ValueError: If depth is out of bounds or direction is invalid.
        """

        if dpt < 0 or dpt >= self.n:
            raise ValueError("Depth index out of bounds.")
        if direction not in ['positive', 'negative']:
            raise ValueError("Direction must be 'positive' or 'negative'.")
        
        face_1, face_2, face_3, face_4 = self.config[0], self.config[3], self.config[5], self.config[1]

        if direction == 'positive':
            for i in range(self.n):
                self.config[0][-(dpt+1)][i], self.config[3][-(dpt+1)][i], self.config[5][-(dpt+1)][i], self.config[1][-(dpt+1)][i] = face_4[-(dpt+1)][i], face_1[-(dpt+1)][i], face_2[-(dpt+1)][i], face_3[-(dpt+1)][i]
            if dpt == 0:
                # clockwise rotation for the front face
                self.config[2] = [list(row) for row in zip(*reversed(self.config[2]))]
            if dpt == self.n - 1:
                # counter-clockwise rotation for the back face
                self.config[4] = [list(row) for row in zip(*self.config[4])][::-1]
    
        if direction == 'negative':
            for i in range(self.n):
                self.config[0][-(dpt+1)][i], self.config[3][-(dpt+1)][i], self.config[5][-(dpt+1)][i], self.config[1][-(dpt+1)][i] = face_2[-(dpt+1)][i], face_3[-(dpt+1)][i], face_4[-(dpt+1)][i], face_1[-(dpt+1)][i] 
            if dpt == 0:
                # counter-clockwise rotation for the front face
                self.config[2] = [list(row) for row in zip(*self.config[2])][::-1]
            if dpt == self.n - 1:
                # clockwise rotation for the back face
                self.config[4] = [list(row) for row in zip(*reversed(self.config[4]))]
