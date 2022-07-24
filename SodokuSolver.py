def board_import(board_name):
    #create empty board for a 9 x 9 sodoku game
    board = [[],[],[],[],[],[],[],[],[]]
    #open the file could do an input to choose here
    file = open(board_name, 'r')
    #make an index to append each number into a different nested list or column
    bindex = 0
    #strip the newline out of the end of each line
    for line in file:
        newline = line.rstrip()
        #convert each charcter to an int and put it in the corresponding nested list
        for char in newline:
            better_char = int(char)
            board[bindex].append(better_char)
        bindex += 1
    #close the file
    file.close()
    return board

def row_scan(row):
    #use an empty list to see all the values in the row and compare
    row_vals = []
    for value in board[row]:
        row_vals.append(value)
    return row_vals

def column_scan(column):
    #use an empty list to see all the values in the column and compare
    col_vals = []
    for num in range(9):
        col_vals.append(board[num][column])
    return col_vals

def square_scan(row, column):
    square = None
    square_list = []
    #square 1
    if row <= 2:
        if column <= 2:
            square = 0
        elif column <= 5:
            square = 1
        elif column <= 8:
            square = 2
    if row >= 3 and row <= 5:
        if column <= 2:
            square = 3
        elif column <= 5:
            square = 4
        elif column <= 8:
            square = 5
    if row >= 6 and row <= 8:
        if column <= 2:
            square = 6
        elif column <= 5:
            square = 7
        elif column <= 8:
            square = 8
    if square <= 2:
        #row = 0-2 every time
        for row in range(3):
            for column in range(3*square, 3*square + 3):
                square_list.append(board[row][column])
    if square >= 3 and square <= 5:
        #row = 3-5 every time
        for row in range(3, 6):
            for column in range(3*(square%3), 3*(square%3) + 3):
                square_list.append(board[row][column])
    if square >= 6 and square <= 8:
        #row = 6-8 every time
        for row in range(6, 9):
            for column in range(3*(square%3), 3*(square%3) + 3):
                square_list.append(board[row][column])
    return square_list    
        


def symmetric_difference(list1, list2):
    difference = []
    for value in list1:
        if value not in list2:
            difference.append(value)
    for value in list2:
        if value not in list1:
            difference.append(value)
    return difference

#FIXME check for squares too XOXO
def possible_values():
    PVL = [
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[]]
    ]
    #filling PVL with known numbers
    for row in range(9):
        for column in range(9):
            if board[row][column] != 0:
                PVL[row][column].append(board[row][column])

    #iterating through the board and finding all numbers that fit with each space
    #make a list of the row
    for row in range(9):
        row_list = row_scan(row)
        #make a list of the column
        for column in range(9):
            col_list = column_scan(column)
            square_list = square_scan(row, column)
            #fill the space if it is empty and not an immutable number
            if PVL[row][column] == []:
                #if a number between 1 - 9 is not in either list add it to PVL in correct space
                for num in range(10):
                    if num not in row_list and num not in col_list and num not in square_list:
                        PVL[row][column].append(num)
    return PVL

def board_solved():
    for num in range(9):
        row = sum(row_scan(num))
        column = sum(column_scan(num))
        if row != 45 or column != 45:
            return True
    return False
        


def solve_backtrack():
    PVL = possible_values()

    row = 0
    column = 0
    row_list = row_scan(row)
    column_list = column_scan(column)
    square_list = square_scan(row, column)
    index = 0
    
    #FIXME completely forgot that 9x9 square also has to be 1 - 9 and add to 45 this should make algorithm more efficient and solve block by block instead
    #FUCKME have to rewrite a ton of code
    #FIXME cannot backtrack to row 0 column 0 without error (unsure if this is still an error)
    while board_solved():
        row_list = row_scan(row)
        column_list = column_scan(column)
        square_list = square_scan(row, column)
        value = PVL[row][column][index]
        #if the value is unique and greater than the current value in the board or it is unmutable add it to the board
        if value not in row_list and value not in column_list and value not in square_list and value > board[row][column] or len(PVL[row][column]) == 1:
            board[row][column] = value
            index = 0
            #if reached the end of the columns go on to the next row else go to next column
            if column == 8:
                column = 0
                row += 1
            else:
                column += 1
        else:
            index += 1

        #print(row)
        #print(column)
        #print(board, '\n\n')

#check to see if it is time to end program since row will be set to 9
        if row == 9:
            pass
        else:
            #backtracking part
            if index == len(PVL[row][column]):
                #reset that space to 0
                board[row][column] = 0
                #go up to the previous row if column equals 0
                if column == 0:
                    row -= 1
                    column = 8
                    #check to see if I need to skip over a non mutable value
                    while len(PVL[row][column]) == 1:
                        if column == 0:
                            row -= 1
                            column = 8
                        else:
                            column -= 1

                else:
                    column -= 1
                    #check to see if I need to skip over a non mutable value
                    while len(PVL[row][column]) == 1:
                        if column == 0:
                            row -= 1
                            column = 8
                        else:
                            column -= 1
                index = 0

if __name__ == "__main__":
    board = board_import('Sodoku1.txt')
    solve_backtrack()
    print(board)