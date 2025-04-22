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
        self.config = [[[color for _ in range(n)] for _ in range(n)] for color in self.colors]

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

cube = Cube()
print(f"CUBE CONFIGURATION: \n{cube}")
