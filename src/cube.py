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

    def horizontal_rotate(self, row, direction):
        """
        Performs a horizontal rotation of the specified row across the four lateral faces.
        If the row is the top or bottom, the Up or Down face is rotated accordingly.

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

cube = Cube()
print(f"CUBE CONFIGURATION: \n{cube}")

for col in range(cube.n):
    for direction in ['up', 'down']:
        cube.vertical_rotate(col, direction)
        print(f"===========================")
        print(f"{direction.upper()} ROTATION ON COLUMN {col}: \n{cube}")

        cube.reset()
