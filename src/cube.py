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

cube = Cube()
print(f"CUBE CONFIGURATION: \n{cube}")

for row in range(cube.n):
    for direction in ['left', 'right']:
        cube.horizontal_rotate(row, direction)
        print(f"===========================")
        print(f"{direction.upper()} ROTATION ON ROW {row}: \n{cube}")

        cube.reset()
