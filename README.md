# CubeCrafter Cube Engine

CubeCrafter is a Python-based Rubik's Cube simulation and solving engine that implements advanced algorithms to efficiently solve Rubik's Cubes of different dimensions. This library provides a comprehensive solution for creating, manipulating, and solving Rubik's Cubes using state-of-the-art search algorithms and heuristics.

<div style="text-align: center;">
  <img src="./image.png" alt="CubeCrafter Cube Engine" style="width: 100%;">
</div>

## Features

- **Customizable Cube Size**: Create and manipulate Rubik's Cubes of any dimension (2×2, 3×3, etc.)
- **Full Rotation Support**: Perform horizontal, vertical, and side rotations with precise control
- **Advanced Solver**: Implements Iterative Deepening A* (IDA*) algorithm with pattern database heuristics
- **Visualization**: String representation of cube states for easy debugging and visualization
- **Pre-computed Heuristics**: Generate and save heuristic databases to dramatically improve solving speed

## The Theory Behind CubeCrafter

### God's Number: The Theoretical Limit

God's Number refers to the minimum number of moves needed to solve any valid configuration of a Rubik's Cube in the worst-case scenario. For the standard 3×3×3 Rubik's Cube, this number was proven in 2010 to be **20 moves** in the half-turn metric (where a 180° turn counts as one move).

This discovery resulted from a collaboration between mathematicians and computer scientists, including Morley Davidson, John Dethridge, Herbert Kociemba, and Tomas Rokicki, who used a combination of group theory, symmetry analysis, and massive computational resources provided by Google.

The implications of God's Number for cube-solving algorithms are profound:
- It establishes a theoretical upper bound for any optimal solving algorithm
- It confirms that no configuration requires more than 20 moves to solve
- It demonstrates that the search space, while enormous (with **43 quintillion possible configurations**), has a surprisingly constrained solution depth

CubeCrafter's solver is designed with this theoretical limit in mind, utilizing sophisticated search techniques to find solutions that approach optimal move counts.

### Iterative Deepening A* (IDA*): Optimal Search in Limited Memory

IDA* is an elegant search algorithm that combines the completeness and optimality guarantees of A* with the memory efficiency of depth-first search. Here's how it works in CubeCrafter:

1. **Iterative Threshold Approach**: IDA* starts with a low threshold and gradually increases it in successive iterations.
   - Each iteration performs a depth-first search but cuts off branches whose estimated total cost (g + h) exceeds the current threshold
   - If a solution isn't found, the threshold is increased to the minimum cost that exceeded the previous threshold

2. **Cost Function**: For each cube state, the cost consists of:
   - **g-score**: The number of moves made so far from the initial state
   - **h-score**: The estimated minimum number of moves needed to reach the solved state (provided by the heuristic database)

3. **Memory Efficiency**: Unlike traditional A* which maintains a priority queue of all frontier nodes, IDA* only keeps track of the current path, making it suitable for the massive search space of the Rubik's Cube.

4. **Optimality Guarantee**: When used with an admissible heuristic (one that never overestimates the cost to goal), IDA* guarantees finding an optimal solution.

### Heuristic Database: The Key to Efficiency

The efficiency of IDA* critically depends on the quality of its heuristic function. CubeCrafter uses a pre-computed pattern database approach to create powerful admissible heuristics:

1. **Breadth-First Search (BFS) Generation**: Starting from the solved state, we perform a BFS to discover the minimum number of moves required to reach any reachable state within a certain depth.

2. **State Representation**: Each cube state is mapped to a string representation, allowing for efficient storage and lookup.

3. **Admissibility**: Our heuristic never overestimates the distance to the goal, ensuring that IDA* produces optimal solutions.

4. **Compression Techniques**: To manage the enormous state space, we utilize:
   - Symmetry reduction to eliminate redundant states
   - Pattern databases that focus on subsets of cube pieces
   - Layered lookup tables for different phases of the solution

The heuristic database dramatically improves performance by pruning large portions of the search space, often reducing solution time from hours to seconds for moderately complex scrambles.

## Installation

```bash
# Clone the repository
git clone https://github.com/kanavgoyal898/CubeCrafter.git
cd CubeCrafter

# Install requirements
pip install -r requirements.txt
```

## Performance Analysis

The efficiency of CubeCrafter's solver depends on several factors:

1. **Heuristic Database Quality**: 
   - Larger max_depth values in the Cost class yield more accurate heuristics but require more computation time
   - For a standard 3×3 cube, a max_depth of 7-8 provides a good balance

2. **Threshold Selection**:
   - Lower thresholds limit the search depth but may fail to find solutions for complex scrambles
   - Higher thresholds allow for more thorough searches but increase computation time

3. **Scramble Complexity**:
   - Performance varies with the distance from the solved state
   - Solutions for scrambles of up to 7-8 moves are typically found in under a second
   - More complex scrambles may require several seconds to minutes

## Acknowledgments

CubeCrafter draws inspiration from decades of research on the Rubik's Cube and optimal solving algorithms, including the work of:

1. **Kociemba, H. (1995).** *The Two-Phase Algorithm for Solving the Rubik’s Cube.* [Link](https://kociemba.org/math/twophase.htm) <br>
In this paper, Kociemba introduces the Two-Phase Algorithm, a highly efficient method for solving the Rubik's Cube. The algorithm divides the solving process into two phases, which significantly reduces the search space, leading to solutions typically within 20 moves. The approach optimizes the search for the cube’s solution by leveraging group theory.

2. **Korf, R. E. (1985).** *Depth-First Iterative-Deepening: An Optimal Admissible Tree Search.* [Link](https://www.sciencedirect.com/science/article/abs/pii/0004370285900840) <br>
In this work, Korf proposes the Iterative Deepening A* (IDA*) algorithm, an optimal search strategy for solving problems like the Rubik's Cube. The algorithm efficiently finds the shortest solution by combining depth-first search with A* and uses pattern databases to speed up the search process.

3. **Rokicki, T., & Kociemba, H. (2010).** *God’s Number Is 20.* [Link](https://kociemba.org/moves20.htm) <br>
Rokicki and Kociemba, in collaboration with others, prove that any configuration of the Rubik’s Cube can be solved in 20 moves or fewer. This result, called “God's Number,” was a significant milestone in computational group theory and Rubik's Cube solving.
