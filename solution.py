import numpy as np

# Assumptions
# - GCD not divisible by 2 or 5
# - GCD should be divisible by 9 -> row should sum to div 9 (elim 9)

row_min = 12345678	# Smallest possible row: 012_345_678
row_max = 876543210 # Largest possible row: 876_543_210
initial_gcd = 4005 # Initial GCD 
progress = 1 # Progress check

def check_rows_valid(current_board):
	row_count = len(current_board)
	if row_count == 0:
		return True
	
	for col in zip(*current_board):  	# Transpose using zip
		if len(set(col)) != row_count:  # Use set for uniqueness
			return False
	return True

def build_boards_rec(rows, current_board=[], row_index=0):
	# print(f'Rows: {rows}')
	# print(f'Board: {current_board}')
	# With current board, filter out remaining rows 
	# Check each column have 9 unique elements
	# Pick one row and recurse	
	
	if len(current_board) == 9:
		# print(f'We are done: {current_board}')
		return [current_board]
	
	valid_boards = []
	for n in range(row_index, len(rows)):
		# print(f'Rows: {rows}')
		row = rows[n]
		potential_board = current_board + [row]
		# print(f'Potential: {potential_board}')
		if not check_rows_valid(potential_board):
			# print(f'Potential does not work')
			continue
		
		# print('Recursing')
		found_boards = build_boards_rec(rows, potential_board, n+1)
		valid_boards.extend(found_boards)
		# print(f'Valid boards: {valid_boards}')
	
	# print(f'Level of recursion ending {valid_boards}')
	return valid_boards

def build_boards(rows):
	return build_boards_rec(rows, [], 0)

# Start with GCD -- high -> low
for gcd in np.arange(initial_gcd, 27, -18): 
	if gcd % 5 == 0: 	# GCD cannot have 5 as factor
		continue
	if gcd / initial_gcd < progress:
		print(f'{initial_gcd - gcd}/{initial_gcd}')
		progress -= 0.1
	
	# Range of possible 9-digit numbers (including leading 0) with the divisor
	start = np.int32(np.ceil(row_min / gcd))
	finish = np.int32(np.floor(row_max / gcd))
	rows = gcd * np.arange(start, finish + 1, gcd)
	
	# Initial sudoku rules ceave
	first_ceave = []
	for row in rows:
		rep_row = str(row) # Easier row representation
		if "9" in rep_row: # Grid does not include '9'
			continue
		if len(set(rep_row)) != len(rep_row): # Breaks sudoku unique row solutions 
			continue
	
		first_ceave.append(rep_row.rjust(9, "0")) # Row is valid
	
	if (len(first_ceave) < 9):
		continue
	# Split into matrix
	second_ceave = np.array(list(map(lambda x: np.array(list(x), dtype=int), first_ceave)))

	fail = False # Python has no labels :(
	for col in range(9):
		if len(set(second_ceave[:, col])) < 9: # Check if each matrix column at least Sudokus
			fail = True
			break
	if fail:
		continue
	valid_rows = first_ceave
	
	if (len(valid_rows) < 9):
		continue
	
	third_ceave = build_boards(valid_rows)
	if not third_ceave:
		continue
	
	print(f'GCD: {gcd}') # We found the answer
	print(f'Boards: {third_ceave}')
	# break