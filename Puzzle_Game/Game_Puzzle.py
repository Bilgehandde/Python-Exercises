# -*- coding: utf-8 -*-
"""
My Python Learning Journey - First Semester University Project - 3

Attention: This project is a homemade word puzzle game created without using any fancy libraries.
Expect to find the most absurd coding practices here :)

The code is part of my learning process, 
and I may have comments or explanations throughout to document my understanding and progress. 
Feel free to explore and provide feedback.

Therefor if you are triyng to optimize this routine and it fails (most surely),
please increase this counter as a warning for the next person.
total hours wasted here = 88 
"""
def read_file(filename="test_puzzle.txt"): 
    words = [] 
    board = []
    with open(filename, "r") as file:
        
        lines = file.readlines()
        
        for line in lines:
            letters = []
            numbers = []
            for char in line:
                if char.isalpha():
                    letters.append(char)
                    
                elif char.isdigit():
                    numbers.append(char)
                    
            words.append(''.join(letters))
            board.append(''.join(numbers))
            
    words = [item for item in words if item != '']
    board = [item for item in board if item != '']
           
    return words,board
# Checks the suitability of the board for the game.
def check_consistency(board):
    
    row_length = len(board[0]) 
    for row in board[1:]:
        if len(row) != row_length:
            return False 
    
    for i in range(len(board)):
        if len(board[i]) != len(board[0]):
            return False
    return True

# Converts each row into a list of characters.
def create_board(board):
    mutate_board = [list(row) for row in board]
    board[:]= mutate_board
# Words Usage Statistics Reset
def identifier(words):
   
    identifier_list = [False] * len(words)
    return identifier_list

def print_board(board):
    
    for row in board:
        for number in row:
            if number == '0':
                print('+', end=' ')  
            else:
                print(" ", end=' ')        
        print("\n")
# Board Printing with Row and Column Numbers        
def print_board_w_c(board):
    row_header = ["R" + str(i) + f"{'' :<2}" for i in range(1, 10)]
    row_header += ["R" + str(i) + f"{'' :<1}" for i in range(10, len(board) +1)]
    col_header = ["C" + str(i)  for i in range(1, len(board[0]) + 1)]

    print("    " + " ".join(col_header))
    for i, row in enumerate(board):
        row_str = row_header[i] + " " + "  ".join("+" if str(cell) == '0' else " " if str(cell) == "1" else str(cell) for cell in row)
        print(row_str)        

# Prints words and their usage statuses.
def print_wordlist(words, wstatus):
    print("Word List              Status")
    for i in range(len(words)):
        if i + 1 < 10 :
            if wstatus[i] : 
                status = "USED" 
            else :
                status = "NOT USED"
            print(f"W{i + 1} {words[i]:<19} {status}")
        else :
            print(f"W{i + 1} {words[i]:<18} {status}")
            
        
def check_entries(coordinates, wordno, board, words):
        rowno, colno = coordinates
        
        # Check the boundaries of the coordinates.
        coordinates_check = 0 < int(rowno) and int(rowno) <= len(board) and 0 < int(colno) and int(colno) <= len(board[0])
        
        # Check the boundaries of the word number.
        words_check = 0 < int(wordno) and int(wordno) <= len(words)

        return coordinates_check, words_check

                
def check_location(board, words, coordinates, wordno, direction='H'):
    rowno, colno = coordinates
    direction = direction.upper()
    
    # Check if the starting cell is restricted or not.
    if board[rowno -1 ][colno -1 ] == '0':
        return False, 1
    
    # Check if the cell above is 0 when the direction is vertical.
    if direction == 'V' and rowno > 1 and board[rowno - 2][colno - 1] != '0' and board[rowno - 2][colno - 1] != 0:
        return False, 2
    
    # Check if the cell left is 0 when the direction is horizontal.
    if direction == 'H' and colno > 1 and board[rowno - 1][colno - 2] != '0' and board[rowno - 1][colno - 2] != 0:
        return False, 3
    
    # If the direction is horizontal, check for the word overflowing the board.
    if direction == 'H' and (colno - 1 + len(words[wordno - 1])) > (len(board[0])):
        return False, 4
    
    # If the direction is vertical, check for the word overflowing the board.
    if direction == 'V' and (rowno - 1 + (len(words[wordno - 1]))) > (len(board)):
        return False, 7
    
    # If the direction is horizontal, check if the word fits into the empty space.
    if direction == 'H' and (colno - 1 + len(words[wordno - 1])) <= len(board[0]):
        
        for i in range(colno,colno + len(words[wordno - 1])):
           if board[rowno - 1][i-1] == "0" or board[rowno - 1][i-1] == 0 : 
               return False, 5
           if board[rowno - 1][i-1] != "1" and board[rowno - 1][i-1] != 1 :
                 
                 if board[rowno - 1][i-1] != f'{words[wordno - 1][i-colno]}' :
                      return False, 5   
    # If the direction is vertical, check if the word fits into the empty space.
    if direction == 'V' and (rowno - 1 + len(words[wordno - 1])) <= len(board):
        
        for i in range(rowno,rowno + len(words[wordno - 1])):
          if board[i-1][colno - 1] == "0" or board[i-1][colno - 1] == 0:
              return False, 8
          if board[i-1][colno - 1] != "1" and board[i-1][colno - 1] != 1:
                  if  board[i-1][colno - 1] != f'{words[wordno - 1][i-rowno]}' :
                      return False, 8
    
    # If the direction is horizontal, check if the cell at the end of the word
    if direction == 'H' and (colno - 1 + len(words[wordno - 1])) < len(board[0]):
        
        if board[rowno - 1][colno - 1 + len(words[wordno - 1])] != "0" and board[rowno - 1][colno - 1 + len(words[wordno - 1])] != 0:
            return False, 6
    
    # If the direction is vertical, check if the cell at the end of the word
    if direction == 'V' and (rowno - 1 + len(words[wordno - 1])) < len(board):
        
        if board[rowno - 1 + len(words[wordno - 1])][colno - 1] != "0" and board[rowno - 1 + len(words[wordno - 1])][colno - 1] != 0 :
            return False, 9
    
    return True, 0   
# Check if the word fits into the empty space.    
def check_word_fits(board, words, coordinates, wordno, direction='H'):
    rowno, colno = coordinates
    direction = direction.upper()
    word = words[wordno - 1]

    if direction == 'H':
        for i in range(len(word)):
            if colno - 1 + len(word) > len(board[0]):
                return False, 1
            if colno + i >= len(board[0]):
                if board[rowno - 1][colno - 1 + i] != '1':
                    if board[rowno - 1][colno - 1 + i] != word[i]:
                        return False, 1
        
    elif direction == 'V':
        for i in range(len(word)):
            if rowno - 1 + len(word) > len(board):
                return False, 2
            if rowno + i >= len(board):
                if board[rowno - 1 + i][colno - 1] != '1':
                    if board[rowno - 1 + i][colno - 1] != word[i]:
                        return False, 2

    return True, 0    

def clear_board(board, wstatus):
    # Tahta üzerindeki değerleri sıfırlar 1 yapar 
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j].isalpha():
                board[i] = board[i][:j] + '1' + board[i][j + 1:]
    for i in range(len(wstatus)):
        wstatus[i] = False
# Separate the entered command into its relevant tasks. "W1R2DHC12" or "R1C5DVW5"    
def decompose_command(str1): 
    str1 = str1.upper()
    
    if 'W' not in str1 or 'R' not in str1 or 'C' not in str1 or 'D' not in str1:
        return -1, None, None, None
    
    if str1[0].isdigit():
        return -1, None, None, None
    
    direction = ""
    move_w = []
    move_r = []
    move_c = []
    
    for i in range(0, len(str1)):
        if str1[i] == 'D':
            if i + 1 < len(str1) and str1[i + 1] == 'V':
                direction += 'V'
            else:
                direction += 'H'
        
        if str1[i] == 'W':
            move_w_str = ''
            for char in str1[i + 1:]:
                if char.isdigit():
                    move_w_str += char
                else:
                    break
            move_w.append(int(move_w_str) if move_w_str.isdigit() else None)
        
        if str1[i] == 'R':
            move_r_str = ''
            for char in str1[i + 1:]:
                if char.isdigit():
                    move_r_str += char
                else:
                    break
            move_r.append(int(move_r_str) if move_r_str.isdigit() else None)
        
        if str1[i] == 'C':
            move_c_str = ''
            for char in str1[i + 1:]:
                if char.isdigit():
                    move_c_str += char
                else:
                    break
            move_c.append(int(move_c_str) if move_c_str.isdigit() else None)
    
    return 0, move_w[0], [move_r[0], move_c[0]], direction 
# Perform the necessary checks for the word to be placed and, if correct, put it in its place.                
def word_it(board, words, wstatus, coordinates, wordno, direction):
    
    direction = direction.upper()
    
    check_entries_bool, check_entries_code = check_entries(coordinates, wordno, board, words) 
    check_location_bool, check_location_code = check_location(board, words, coordinates, wordno, direction)
    check_word_fits_bool, check_word_fits_code = check_word_fits(board, words, coordinates, wordno, direction)
    if check_entries_bool and check_location_bool and  check_word_fits_bool :
       if wstatus[wordno - 1] == False:   
           rowno, colno = coordinates
           word = words[wordno - 1]
       
           if direction == 'H':
               board[rowno-1] = board[rowno-1][:colno-1]+f"{word}"+board[rowno-1][colno-1 + len(word):]
           if direction == 'V':
               for i in range(len(word)):
                   board[rowno-1 + i] = board[rowno-1 + i][:colno-1]+f"{word[i]}"+board[rowno-1 + i][colno-1 + 1:]
            
           wstatus[wordno - 1] = True
           return True 
    return False 
# Tracks the progress of the played steps.                    
def track_board(board):
    trackboard = []

    for row in board:
        new_row = []
        for char in row:
            if char.isalpha():
                new_row.append(f'{char}')
            else:
                new_row.append(str(char))
        trackboard.append(new_row)
    return trackboard      
# Adds the played steps to the tracking list and provides the step count.            
def track_move(mvn, trackmoves, coordinates, wordno, direction, board, wstatus):
    board = track_board(board)
    moves = (coordinates, wordno, direction, board, wstatus.copy())
    trackmoves.append(moves)
    mvn += 1
    return mvn            
# Checks if the board is solved.            
def check_solved(board):
    for row in board:
        if 1 in set(row):
            return False
        if "1" in row:
            return False
    return True
# Undoes the last move.
def undo_moves(trackmoves,word,wstatus, words,board):
    if  trackmoves:
        last_move = trackmoves.pop()
        if not last_move :
            last_move = trackmoves[-1]
        if isinstance(last_move, list):
            last_move = last_move[0]
        coordinates, wordno, direction, _, wstatus = last_move
        rowno, colno = coordinates
        word = words[wordno - 1]
        
        if direction.lower() == "v":
            for i in range(len(words[wordno - 1])):
                letter_left = []
                letter_right = []
                # Checks the left side.
                if colno > 1:
                    if board[rowno - 1 + i][colno - 2] not in ['0', '1',0,1]:
                        
                        letter_left.append([board[rowno - 1 + i][colno -1], rowno - 1 + i, colno - 1])
                        
                # Checks the right side.
                if colno < len(board[0]):
                        if board[rowno - 1 + i][colno] not in ['0', '1',0,1]:
                            
                            letter_right.append([board[rowno - 1 + i][colno-1],rowno - 1 + i,colno - 1])
                # Replace the letters with 1s.         
                board[rowno - 1 + i] = board[rowno - 1 + i][:colno - 1] + '1' +board[rowno - 1 + i][colno:]

                # Add the letter on the left.
                for letter_info in letter_left:
                    board[letter_info[1]] = board[letter_info[1]][:letter_info[2]]+f"{letter_info[0]}"+board[letter_info[1]][letter_info[2] + 1:]

               # Add the letter on the right.
                for letter_info in letter_right:
                    board[letter_info[1]] = board[letter_info[1]][:letter_info[2]]+f"{letter_info[0]}"+board[letter_info[1]][letter_info[2] + 1:]
        
        if direction.lower() == "h":
            letter_up = []
            letter_down = []
            if rowno > 1 :
                for i in range(colno,colno + len(words[wordno - 1])):
                    if board[rowno - 2][i - 1] not in ['0', '1',0,1]:
                        
                        letter_up.append([board[rowno - 1][i-1],rowno-1,i-1])
                        
            if rowno < len(board):            
                for i in range(colno,colno + len(words[wordno - 1])):
                    if  board[rowno][i - 1] not in ['0', '1',0,1]:
                        
                        letter_down.append([board[rowno -1][i-1],rowno-1,i-1])
            # Replace the letters with 1s.  
            board[rowno - 1] = board[rowno - 1][:colno - 1] + len(word) * '1' + board[rowno - 1][colno - 1 + len(word):]
            
             # Add the deleted letters from above.
            for letter_info in letter_up:
                     board[letter_info[1]] = board[letter_info[1]][:letter_info[2]]+f"{letter_info[0]}"+board[letter_info[1]][letter_info[2] + 1:]

            # Add the deleted letters from down.
            for letter_info in letter_down:
                    board[letter_info[1]] = board[letter_info[1]][:letter_info[2]]+f"{letter_info[0]}"+board[letter_info[1]][letter_info[2] + 1:]
        
        wstatus[wordno - 1] = False
        
        return board,wordno

# Written to separate empty cells on the board, used in find_horizontal_cells and find_vertical_cells.
def convert_board(board): 
    converted_board = []
    # Example:  ['1111100111'] --> [1, 1, 1, 1, 1 , 0, 0, 1, 1, 1]
    for row in board:
        converted_row = [ int(cell) for cell in row]
        converted_board.append(converted_row)
    
    return converted_board

def factory(number):
    if number == 0 or number == 1 :
        return 1
    else : 
        result = 1 
        for i in range(2,number+1):
            result *= i
        return result
    
# This is for finding horizontal gaps along with the starting coordinate!
def find_horizontal_cells(board): 
    board = convert_board(board)
    h_cells = []

    for i, row in enumerate(board):
        sequence_start = 0

        while sequence_start < len(row):
            # Count consecutive 1s to check their length.
            sequence_length = 0
            while sequence_start + sequence_length < len(row) and row[sequence_start + sequence_length] == 1:
                sequence_length += 1

            # Add to the list if there are two or more consecutive 1s.
            if sequence_length >= 2:
                h_cells.append([[i, sequence_start], row[sequence_start:sequence_start + sequence_length]])

            sequence_start += sequence_length + 1
    

    return h_cells
# This is for finding vertical gaps along with the starting coordinate!
def find_vertical_cells(board):
    board = convert_board(board)
    v_cells = []

    for i in range(len(board[0])):
        sequence_start = 0

        while sequence_start < len(board):
            # Count consecutive 1s to check their length.
            sequence_length = 0
            while sequence_start + sequence_length < len(board) and board[sequence_start + sequence_length][i] == 1:
                sequence_length += 1

            # Add to the list if there are two or more consecutive 1s.
            if sequence_length >= 2:
                v_cells.append([[sequence_start, i], [board[j][i] for j in range(sequence_start, sequence_start + sequence_length)]])

            sequence_start += sequence_length + 1

    return v_cells
# Attempt to place the incoming move sequentially in the vacant spaces that have been separated from the board, 
# both horizontally and vertically. Update the statuses and tracking accordingly.
def word_write(length_dict_h, length_dict_v, wordno, word, words, board):
    length_dict_v_keys = list(length_dict_v.keys())
    length_dict_h_keys = list(length_dict_h.keys())
    
    exit_loop = False
    wstatus = identifier(words)
    trackmoves = []
    mvn = 0
    directions = ['H', 'V']

    for direction in directions:
        if exit_loop or wstatus[wordno - 1]:
            break

        if direction == 'H':
            length_dict_keys = length_dict_h_keys
        else:
            length_dict_keys = length_dict_v_keys

        for keys in length_dict_keys[::-1]:
            if exit_loop:
                break
            cell_infos = length_dict_h[keys] if direction == 'H' else length_dict_v[keys]

            for h_cell_info in cell_infos:
                for i in range(len(h_cell_info)):
                    rowno, colno = h_cell_info[i][0]
                    coordinates = [rowno + 1, colno + 1]
                    if word_it(board, words, wstatus, coordinates, wordno, direction):
                        rowno, colno = coordinates

                        if direction == 'H':
                            board[rowno - 1] = board[rowno - 1][:colno - 1] + f"{word}" + board[rowno - 1][colno - 1 + len(word):]
                        else:
                            for j in range(len(word)):
                                board[rowno - 1 + j] = board[rowno - 1 + j][:colno - 1] + f"{word[j]}" + board[rowno - 1 + j][colno - 1 + 1:]

                        wstatus[wordno - 1] = True
                        moveno = track_move(mvn, trackmoves, coordinates, wordno, direction, board, wstatus)
                        exit_loop = True
                        break

                if exit_loop:
                    break
    return trackmoves

# Shuffle the list of words separated by spaces according to their lengths.
def shuffle(index):
    shuffle = index.pop(len(index)-len(index))
    index.insert(len(index)-2, shuffle)
    shuffle = index.pop(len(index)-1)
    index.insert(0,shuffle)

    
    return index
# Place the words starting from the longest, filling in the empty spaces. 
# If there are words that couldn't be placed, move back as much as the number of successfully placed words in that length group, 
# and shuffle the words of that length again.    
def try_word(words,categorized_words,length_dict_h, length_dict_v,board,wstatus):    
        wstatus = identifier(words)
        trackmoves = []
        index_count = 0
        a = 0
        for index in categorized_words[::-1]:
            index_count = a
           
            for i in index[::-1]:
                wordno, word = i
                if not wstatus[wordno - 1] : 
                    
                    trackmoves.append(word_write(length_dict_h, length_dict_v, wordno, word, words, board ))
                    index_count += 1
                    wstatus[wordno - 1] = True

                    if len(trackmoves[-1]) == 0 : 
                            index = shuffle(index)
                            for b in range (index_count):
                                board , _ = undo_moves(trackmoves,word,wstatus, words,board)
                            index_count = 0 
                            wstatus[wordno - 1] = False
                            
                            break
        return board,wstatus
        

# Attempts to solve the board using the necessary functions.                   
def solve_puzzle(board, words):
    wstatus = identifier(words)
    h_cells = find_horizontal_cells(board)
    v_cells = find_vertical_cells(board)
    clear_board(board, wstatus)
    word_lengths = [len(word) for word in words]
    longest_word = max(word_lengths)
    # Find the longest horizontal cell
    h_length = 0
    longest_h_cells = []

    for i in h_cells:
        length = len(i[1])
        
        if length > h_length:
            h_length = length
            longest_h_cells = [i]
        elif length == h_length:
            longest_h_cells.append(i)       
    # Find the longest vertical cell      
    v_length = 0
    longest_v_cells = []

    for j in v_cells:
        length = len(j[1])
        
        if length > v_length:
            v_length = length
            longest_v_cells = [j]
        elif length == v_length:
            longest_v_cells.append(j)
    
    # Split words with their numbers in a list based on word length
    categorized_words = [[] for _ in range(2, max(word_lengths) + 1)]

    for i, length in enumerate(word_lengths):
        categorized_words[length - 2].append((i + 1, words[i]))
    # Filter the word list    
    categorized_words = [item for item in categorized_words if item]
        
    # Separate horizontal gaps with their coordinates based on the number of empty cells
    global_h = [[] for _ in range(2, 21)]

    for coordinates, cells in h_cells:
        length_h = len(cells)
        global_h[length_h - 2].append((coordinates,cells)) 
                
    # Separate vertical gaps with their coordinates based on the number of empty cells
    global_v =  [[] for _ in range(2, 21)]
    
    for coordinates, cells in v_cells:
        length_v = len(cells)
        global_v[length_v - 2 ].append((coordinates,cells))  
    
    # If the largest word doesn't fit into the largest empty cell, the board is unsolvable
 
    longest_puzzle_cells = max(len(longest_v_cells[0][1]), len(longest_h_cells[0][1]))
    if longest_puzzle_cells != longest_word:
        return False, print("\nYour longest word does not fit any space...\n")
   
# Create a list named according to length
    length_dict_h = {}
    
    for i, full_list in enumerate(global_h):
   
        if full_list:
            length = len(full_list[0][1])
            length_list = f"{length}"
            # Add to existing list if it already exists, otherwise create a new list
            if length_list in  length_dict_h:
                length_dict_h[length_list].append(full_list)
            else:
                length_dict_h[length_list] = [full_list]
                
    length_dict_v = {}
    
    for i, full_list in enumerate(global_v):

        if full_list:
            length = len(full_list[0][1])   
            length_list = f"{length}"
            # Add to existing list if it already exists, otherwise create a new list
            if length_list in length_dict_v:
                length_dict_v[length_list].append(full_list)
            else:
                length_dict_v[length_list] = [full_list]
     
    again_count = 0
    total_attempts = 0
    cont = 0
# Solve the puzzle by trying all possible combinations until a solution is found
    while again_count < len(categorized_words):
        current_category = categorized_words[again_count]
        num_words_in_category = len(current_category)
        
        for i in range(factory(num_words_in_category-1)):
            board , wstatus = try_word(words,categorized_words,length_dict_h, length_dict_v,board,wstatus)
            # print_board_w_c(board)
            total_attempts += 1
            if check_solved(board) :
                return True 
            elif len(categorized_words) - again_count == 1: 
                if cont == 0 : 
                    for i in range(len(categorized_words)):
                        index = categorized_words[i]
                        index = shuffle(index)
                    clear_board(board, wstatus)
                    cont += 1
                    again_count -= 1
        
        again_count += 1
        
    return False

# Main Gameplay 
def word_puzzle():
    while True:
        filename = input("\nEnter the filename for the puzzle (or press Enter for the default 'test_puzzle.txt'): ")
        if not filename:
            filename = "test_puzzle.txt"

        words, board = read_file(filename)

        while not check_consistency(board):
            print(f"The puzzle board of {filename} is not consistent!")

            try_new_file = input("Do you want to try a new file? (y/n): ").lower()
            if try_new_file != 'y':
                print("Game over. Goodbye!")
                return

            filename = input("Enter the filename for the puzzle: ")
            words, board = read_file(filename)
        wstatus = identifier(words)
        print_wordlist(words, wstatus)
        print("\n")
        print_board_w_c(board)

        trackmoves = []
        mvn = 0

        while not check_solved(board):
            move = input("Enter your move (or press 'h' for help): ").lower()

            if move == 'h':
                print("Move format: (WXRYCZDT)")
                print("Options:")
                print("cb - clear board")
                print("q - quit game")
                print("s - solve puzzle")
                print("w - move back")
                continue

            if move == 'q':
                print("Game quit. Goodbye!")
                return

            if move == 's':
                clear_board(board, wstatus)
                if solve_puzzle(board, words):
                    print("\n")
                    print_board_w_c(board)
                    print("\n******** Here is the solved puzzle ********")
                    break
                else:
                    print("Puzzle could not be solved.")
                    continue

            if move == 'cb':
                print("\n******** Board is cleared ********")
                clear_board(board, wstatus)
                print("\n")
                print_wordlist(words, wstatus)
                print("\n")
                print_board_w_c(board)
                continue

            if move == 'w':
                if trackmoves:
                    board, wordno = undo_moves(trackmoves, words, wstatus, words, board)
                    mvn -= 1
                    print("\n******** Last move undone ********")
                    print("\n")
                    wstatus[wordno - 1] = False
                    print_wordlist(words, wstatus)
                    print("\n")
                    print_board_w_c(board)
                    print("\n")
                    continue
                else:
                    print("\n******** No moves to undo ********")
                    continue

            try:
                code, wordno, coordinates, direction = decompose_command(move)
                if code == -1:
                    print("Invalid move. Please check the format.")
                    continue

                if code == 0:
                    if wordno is not None and coordinates is not None and direction is not None:
                        coordinates_check , word_check = check_entries(coordinates, wordno, board, words)
                        if not coordinates_check :
                            print("Invalid move: Check your coordinates!")
                            continue
                        elif not word_check :
                            print("Invalid move: Check your word!")
                            continue
                        result = check_location(board, words, coordinates, wordno, direction)
                        if not result[0]:
                            print("Invalid move: Check your cell! ")
                            continue

                        result = check_word_fits(board, words, coordinates, wordno, direction)
                        if not result[0]:
                            print("Invalid move: Word does not fit the space!")
                            continue

                        result = word_it(board, words, wstatus, coordinates, wordno, direction)
                        if not result:
                            print("Word placement failed. Please try again.")
                            continue

                        print("\n******** Word placed successfully ******** ")
                        print("\n")
                        wstatus[wordno - 1] = True
                        mvn = track_move(mvn, trackmoves, coordinates, wordno, direction, board,wstatus)
                        print_wordlist(words, wstatus)
                        print("\n")
                        print_board_w_c(board)
                    else:
                        print("Invalid move. Please check the format.")
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
        if not move == 's':
            print("\nWell done you solve the puzzle successfully :)\n ")
        play_again = input("Would you like to play again? (y/n): ").lower()
        if play_again != 'y':
            print("Game over. Goodbye!")
            break

if __name__ == "__main__":
     word_puzzle()
