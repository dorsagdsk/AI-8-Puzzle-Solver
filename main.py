import tkinter as tk
from tkinter import messagebox
import time

elapsed_time = 0.0
solution = []

class Puzzle:
    """
    A class representing the 8 Puzzle problem.

    Attributes:
        state (list): Current state of the puzzle.
        goal_state (list): The goal state of the puzzle.
    """

    def __init__(self, state):
        """
        Initialize the Puzzle class with a given state.

        Args:
            state (list): Current state of the puzzle.
        """
        self.state = state
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # Goal state of the puzzle

    def is_goal_state(self):
        """
        Check if the current state is the goal state.

        Returns:
            bool: True if the current state is the goal state, False otherwise.
        """
        return self.state == self.goal_state

    def get_successors(self):
        """
        Generate successor states of the current state by moving the empty tile.

        Returns:
            list: A list of successor states.
        """
        successors = []
        # Finding the index of the empty tile (0)
        empty_tile_index = self.state.index(0)

        # Possible moves: Up, Down, Left, Right
        possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for move in possible_moves:
            new_state = self.state[:]
            row, col = empty_tile_index // 3 + move[0], empty_tile_index % 3 + move[1]
            if 0 <= row < 3 and 0 <= col < 3:
                new_index = row * 3 + col
                new_state[empty_tile_index], new_state[new_index] = new_state[new_index], new_state[empty_tile_index]
                successors.append(new_state)

        return successors

def hamming_distance(state, goal_state):
    """
    Calculate the Hamming distance heuristic.

    Args:
        state (list): Current state of the puzzle.
        goal_state (list): The goal state of the puzzle.

    Returns:
        int: The Hamming distance heuristic value.
    """
    return sum(1 for i, j in zip(state, goal_state) if i != j and i != 0)

def manhattan_distance(state, goal_state):
    """
    Calculate the Manhattan distance heuristic.

    Args:
        state (list): Current state of the puzzle.
        goal_state (list): The goal state of the puzzle.

    Returns:
        int: The Manhattan distance heuristic value.
    """
    total_distance = 0
    for i in range(3):
        for j in range(3):
            if state[i * 3 + j] != 0:
                current_row, current_col = divmod(state[i * 3 + j] - 1, 3)
                goal_row, goal_col = divmod(goal_state[i * 3 + j] - 1, 3)
                total_distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return total_distance

def depth_limited_search_heuristic(state, goal_state, depth_limit, visited, heuristic):
    if state == goal_state:
        return [state]

    if depth_limit == 0:
        return None

    visited.add(tuple(state))

    successors = Puzzle(state).get_successors()
    successors.sort(key=lambda s: heuristic(s, goal_state))

    for successor in successors:
        if tuple(successor) not in visited:
            result = depth_limited_search_heuristic(successor, goal_state, depth_limit - 1, visited, heuristic)
            if result is not None:
                return [state] + result

    return None

def iterative_deepening_search_heuristic(initial_state, goal_state, heuristic):
    max_depth = 50
    start_time = time.time()
    global elapsed_time
    for depth_limit in range(max_depth):
        visited = set()
        result = depth_limited_search_heuristic(initial_state, goal_state, depth_limit, visited, heuristic)
        if result is not None:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Solution found in {elapsed_time} seconds.")
            return result
    print("No solution found within the depth limit.")
    return None

def initial_state():
    initial_state = [2, 3, 1, 8, 0, 4, 7, 6, 5]
    return initial_state

def solve_puzzle_gui():
    global solution

    if not solution:
        messagebox.showinfo("No Solution")
        return

    root = tk.Tk()
    root.title("8 Puzzle")

    for index, state in enumerate(solution):
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                if state[index] == 0:
                    label = tk.Label(root, text=" ", width=10, height=5, borderwidth=1, relief="solid")
                else:
                    label = tk.Label(root, text=state[index], width=10, height=5, borderwidth=1, relief="solid")
                label.grid(row=i, column=j)

        end_time_label = tk.Label(root, text=f"Elapsed Time: {elapsed_time:.2f} seconds")
        end_time_label.grid(row=4, column=0, columnspan=3)

        root.update()
        time.sleep(1)

    root.mainloop()

def solve_puzzle_ids():
    global solution
    initial_state_value = initial_state()
    goal_state = [1, 2, 3, 8,0, 4, 7, 6, 5]
    print("Random Initial State:", initial_state_value)
    solution = iterative_deepening_search_heuristic(initial_state_value, goal_state, hamming_distance)
    if solution is not None:
        print("Solution found:")
        print_solution_steps(solution)
        solve_puzzle_gui()
    else:
        print("No solution found within the depth limit.")
        root = tk.Tk()
        root.title("8 Puzzle")
        end_time_label = tk.Label(root, text=f"no solution")
        end_time_label.grid(row=4, column=0, columnspan=3)

        def misplaced_tiles(state, goal_state):
            """
            Calculate the number of misplaced tiles heuristic.

            Args:
                state (list): Current state of the puzzle.
                goal_state (list): The goal state of the puzzle.

            Returns:
                int: The number of misplaced tiles heuristic value.
            """
            return sum(1 for i, j in zip(state, goal_state) if i != j)


def misplaced_tiles(state, goal_state):
    """
    Calculate the number of misplaced tiles heuristic.

    Args:
        state (list): Current state of the puzzle.
        goal_state (list): The goal state of the puzzle.

    Returns:
        int: The number of misplaced tiles heuristic value.
    """
    return sum(1 for i, j in zip(state, goal_state) if i != j)



def iterative_deepening_search_heuristic(initial_state, goal_state, heuristic):
    max_depth = 50
    start_time = time.time()
    global elapsed_time
    for depth_limit in range(max_depth):
        visited = set()
        result = depth_limited_search_heuristic(initial_state, goal_state, depth_limit, visited, heuristic)
        if result is not None:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Solution found in {elapsed_time} seconds.")
            return result
    print("No solution found within the depth limit.")
    return None

def solve_puzzle_heuristic_type3():
    global solution
    initial_state_value = initial_state()
    goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    print("Random Initial State:", initial_state_value)
    solution = iterative_deepening_search_heuristic(initial_state_value, goal_state, misplaced_tiles)
    if solution is not None:
        print("Solution found:")
        print_solution_steps(solution)
        solve_puzzle_gui()
    else:
        print("No solution found within the depth limit.")
        root = tk.Tk()
        root.title("8 Puzzle")
        end_time_label = tk.Label(root, text=f"no solution")
        end_time_label.grid(row=4, column=0, columnspan=3)



def solve_puzzle_heuristic_type1():
    global solution
    initial_state_value = initial_state()
    goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    print("Random Initial State:", initial_state_value)
    solution = iterative_deepening_search_heuristic(initial_state_value, goal_state, hamming_distance)
    if solution is not None:
        print("Solution found:")
        print_solution_steps(solution)
        solve_puzzle_gui()
    else:
        print("No solution found within the depth limit.")
        root = tk.Tk()
        root.title("8 Puzzle")
        end_time_label = tk.Label(root, text=f"no solution")
        end_time_label.grid(row=4, column=0, columnspan=3)

def solve_puzzle_heuristic_type2():
    global solution
    initial_state_value = initial_state()
    goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    print("Random Initial State:", initial_state_value)
    solution = iterative_deepening_search_heuristic(initial_state_value, goal_state, manhattan_distance)
    if solution is not None:
        print("Solution found:")
        print_solution_steps(solution)
        solve_puzzle_gui()
    else:
        print("No solution found within the depth limit.")
        root = tk.Tk()
        root.title("8 Puzzle")
        end_time_label = tk.Label(root, text=f"no solution")
        end_time_label.grid(row=4, column=0, columnspan=3)




def print_solution_steps(solution):
    for index, state in enumerate(solution):
        print(f"Step {index + 1}: {state}")

def main():
    root = tk.Tk()
    root.title("8 Puzzle")

    def display_initial_state():
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                if initial_state_value[index] == 0:
                    label = tk.Label(root, text=" ", width=10, height=5, borderwidth=1, relief="solid")
                else:
                    label = tk.Label(root, text=initial_state_value[index], width=10, height=5, borderwidth=1,
                                     relief="solid")
                label.grid(row=i, column=j)

    initial_state_value = initial_state()
    display_initial_state()

    solve_button = tk.Button(root, text="Solve with ids", command=solve_puzzle_ids)
    solve_button.grid(row=3, column=0, columnspan=3)

    solve_button = tk.Button(root, text="Solve with heuristic type 1", command=solve_puzzle_heuristic_type1)
    solve_button.grid(row=4, column=0, columnspan=3)

    solve_button = tk.Button(root, text="Solve with heuristic type 2", command=solve_puzzle_heuristic_type2)
    solve_button.grid(row=5, column=0, columnspan=3)

    solve_button = tk.Button(root, text="Solve with heuristic type 3", command=solve_puzzle_heuristic_type3)
    solve_button.grid(row=6, column=0, columnspan=3)

    root.mainloop()

if __name__ == "__main__":
    main()
