# SOLUTION.
#   Iterate through potential GCDs from high to low
#   For each GCD, generate all multiples from 012345678-987654320
#   Each multiple should not have any duplicate characters
#   If there are less than 9 valid multiples, continue the loop
#   For valid multiples, ensure that the columns have no duplicate characters either
#   For each valid multiple, try and generate a sudoku board

import numpy as np

gcd_0 = 87654321    # Initial GCD -- highest smallest row
row_max = 987654320 # Max row value
row_min = 12345678  # Min row value
df = [1, 3, 4, 6, 7, 8, 9]   # Degrees of freedom -- numbers which can be excluded
sudoku_dim = 9  # No magic numbers or something

def check_rows_valid(current_board):
    board_matrix = np.array(current_board)
    unique_columns = np.unique(board_matrix, axis=1)
    return unique_columns.shape[1] == board_matrix.shape[1]

def build_boards_rec(rows, current_board):
    # With current board, filter out remaining rows 
    # Check each column have 9 unique elements
    # Pick one row and recurse
    if not check_rows_valid(current_board):
        return []
    
    if len(current_board) == 9:
        print(current_board)
        return [current_board]
    
    valid_boards = []
    for rowi in range(len(rows)):
        potential_board = current_board + [rows[rowi]]
        if not check_rows_valid(potential_board):
            rows.remove(rowi)
            continue
        
        found_boards = build_boards_rec(rows, potential_board)
        valid_boards.extend(found_boards)
    
    return valid_boards


for gcd in range(gcd_0, 0, -1): # Iterate through all possible GCDs starting at initial
    mult_max = np.floor(row_max / gcd_0)
    mult_min = np.ceil(row_min / gcd_0)
    mult_range = gcd * np.arange(mult_min, mult_max + 1, 1)

    rows_first = np.array()     # Var for rows after initial ceave 
    for row in mult_range:      # Process potential rows
        row_chars = list(str(row).rjust(sudoku_dim, '0'))     # String format intermediary for digits; pad 0
        row_digits = np.array(row_chars, dtype=int)  # Row digits
        
        if len(np.unique(row_digits)) != len(row_digits):   # Filter out row by Sudoku rules
            continue

        rows_first.append(row_digits)   # Add output of initial ceave
    
    label = False # Python has no loop labels
    for elim in df: # Go through each possible eliminated digit (df)
        rows_filtered = []
        for row in rows_first: # Search for current 
            if elim in row:
                continue
            rows_filtered.append(rows_filtered)
        if len(rows_filtered) < sudoku_dim: # If there aren't enough rows to construct a sudoku board continue
            continue

        # Begin test sudoku board construction
        # boards_pot = build_sudoku_rec(np.array(rows_filtered), [])
        boards_pot = build_boards_rec(np.array(rows_filtered), [])
        if len(boards_pot) > 0:
            print(boards_pot)
            label = True
            break
    if label:
        break
