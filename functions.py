def displayArt():
    import random
    import os

    fileDirectory = os.path.abspath('reversiNames')
    print(fileDirectory)
    s = 0
    for i in range(4):
        s += random.randint(1, 25)
    if s >= 85:
        childDirectory = os.path.join(fileDirectory, '10lo')
        for i in open(childDirectory).read():
            print(i, end='')
        open(childDirectory).close()

    else:
        logo = random.randint(1, 9)
        childDirectory = os.path.join(fileDirectory, f'{str(logo)}lo')
        for i in open(childDirectory).read():
            print(i, end='')
        open(childDirectory).close()
    print('\n')
    instructions = os.path.abspath('instructions')
    print("Have you played the game before? (y/n)")
    if input() in 'Nn':
        print('\n\n')
        for i in open(instructions).read():
            print(i, end='')
        open(instructions).close()
        print('\n\n\n')


def printInstructions():
    instructions = os.path.abspath('instructions')
    for i in open(instructions).read():
        print(i, end='')
    open(".\\instructions").close()
    print('\n\n\n')


def createBoard():
    board = [' ']*8
    for i in range(8):
        board[i] = [' ']*8
    initialize(board)
    return board


def showBoard(displayboard, value=False):
    if value:
        head1 = '01234567'
        head2 = '01234567'
    else:
        head1 = '12345678'
        head2 = 'abcdefgh'
    print('  ', end=' ')
    # prints an empty space for the numbers to line up with the board
    for i in head1:
        print(i, end='  ')
    # prints the indentifying numbers
    print()
    for i in range(len(displayboard)):
        # This prints the identifying number for the side
        print(head2[i], end='  ')
        for j in displayboard[i]:
            if j == ' ':
                # prints a '.' for empty spaces
                print('.', end='  ')
            else:
                # prints the character in the list
                print(j, end='  ')
        print()
    print()


def initialize(board):
    # 0 is a white piece, @ is a black piece
    board[3][3] = 'O'
    board[3][4] = '@'
    board[4][3] = '@'
    board[4][4] = 'O'


def getScore(board):
    whiteCount = blackCount = 0
    for i in board:
        for j in i:
            if j == 'O':
                whiteCount += 1
            # not used else because there can be empty spaces when the game finishes
            elif j == '@':
                blackCount += 1

    return whiteCount, blackCount


def getMovePlayed(board, key):
    dic = {'@': 'Black', 'O': 'White'}
    print(f"{dic[key]}, enter your move: ")
    move = input()
    if move.lower() == 'skip':
        return 0
    if move.lower() == "rules":
        printInstructions()
        return getMovePlayed(board, key)
    moveX = int(move[1]) - 1
    moveIndexY = {'a': 0, 'b': 1, "c": 2,
                  'd': 3, 'e': 4, 'f': 5, 'g': 6, "h": 7}
    if board[moveIndexY[move[0]]][moveX] == ' ':
        board[moveIndexY[move[0]]][moveX] = key
    else:
        print("Invalid move :/")
        return getMovePlayed(board, key)
    if not checkMove(board, [moveIndexY[move[0]], moveX], key) == [[[]], [[]], [[]]]:
        return [moveIndexY[move[0]], moveX]
    else:
        board[moveIndexY[move[0]]][moveX] = ' '
        print("Invalid Move :/")
        return getMovePlayed(board, key)


def flipPieces(board, base, positions, key):
    def flipVertical(board, start, end, key):
        if start[0] < end[0]:
            for i in range(start[0], end[0] + 1, 1):
                board[i][start[1]] = key
        else:
            for i in range(start[0], end[0] - 1, -1):
                board[i][start[1]] = key

    def flipHorizontal(board, start, end, key):
        if start[1] < end[1]:
            for i in range(start[1], end[1] + 1, 1):
                board[start[0]][i] = key
        else:
            for i in range(start[1], end[1] - 1, -1):
                board[start[0]][i] = key

    def flipDiagonal(board, start, end, key):
        i, j = start[0], start[1]
        if i < end[0]:
            if j < end[1]:
                while (-1 < i < end[0]) and (-1 < j < end[1]):
                    board[i][j] = key
                    i += 1
                    j += 1
            elif j > end[1]:
                while (-1 < i < end[0]) and (8 > j > end[1]):
                    board[i][j] = key
                    i += 1
                    j -= 1
        if i > end[0]:
            if j < end[1]:
                while (8 > i > end[0]) and (-1 < j < end[1]):
                    board[i][j] = key
                    i -= 1
                    j += 1
            elif j > end[1]:
                while (8 > i > end[0]) and (8 > j > end[1]):
                    board[i][j] = key
                    i -= 1
                    j -= 1

    if positions[0] != [[]]:
        for j in positions[0]:
            for i in j:
                flipVertical(board, base, i, key)
    if positions[1] != [[]]:
        for j in positions[1]:
            for i in j:
                flipHorizontal(board, base, i, key)
    if positions[2] != [[]]:
        for j in positions[2]:
            for i in j:
                flipDiagonal(board, base, i, key)


def checkMove(board, base, key):
    x, y = base[0], base[1]
    horizontalPos, verticalPos, diagonalPos = [], [], []

    def horizontal(board, x, y, key, sign=1):

        nonlocal horizontalPos
        if sign == 1:
            for i in range(y + 1, len(board)):
                if board[x][i] == ' ':
                    break
                elif board[x][i] != key:
                    continue
                elif (board[x][i] == key) and (i != y):
                    if i - 1 > y:
                        if (board[x][i-1] not in [key, ' ']):
                            horizontalPos.append([x, i])
                            break
                else:
                    continue
        else:
            for i in range(y-1, -1, -1):
                if board[x][i] == ' ':
                    break
                elif board[x][i] != key:
                    continue
                elif (board[x][i] == key) and (i != y):
                    if i + 1 < y:
                        if (board[x][i+1] not in [key, ' ']):
                            horizontalPos.append([x, i])
                            break
                else:
                    continue

        if sign == -1:
            return horizontalPos
        else:
            return horizontal(board, x, y, key, -1)

    def vertical(board, x, y, key, sign=1):

        nonlocal verticalPos
        if sign == 1:
            for i in range(x, len(board)):
                if board[i][y] == ' ':
                    break
                elif board[i][y] != key:
                    continue
                elif (board[i][y] == key) and (i != x):
                    if i - 1 > x:
                        if (board[i-1][y] not in [key, ' ']):
                            verticalPos.append([i, y])
                            break
                else:
                    continue
        else:
            for i in range(x, -1, -1):
                if board[i][y] == ' ':
                    break
                elif board[i][y] != key:
                    continue
                elif (board[i][y] == key) and (i != x):
                    if i + 1 < x:
                        if (board[i+1][y] not in [key, ' ']):
                            verticalPos.append([i, y])
                            break

                else:
                    continue

        if sign == -1:
            return verticalPos
        else:
            return vertical(board, x, y, key, -1)

    def diagonal(board,  x, y, key, signs):

        nonlocal diagonalPos
        sign1, sign2 = signs
        a, b = x, y
        while (0 <= a < len(board)) and (0 <= b < len(board)):
            if board[a][b] == ' ':
                break
            elif board[a][b] != key:
                a += sign1
                b += sign2
                continue
            elif (board[a][b] == key) and ([a, b] not in diagonalPos) and ([a, b] != [x, y]) and (board[a - (sign1)][b-(sign2)] not in [key, ' ']):
                diagonalPos.append([a, b])
                break

            a += sign1
            b += sign2

    values = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    for i in values:
        diagonal(board, x, y, key, i)

    horizontal(board, x, y, key)
    vertical(board, x, y, key)
    return [[verticalPos], [horizontalPos], [diagonalPos]]


def allMoves(board):

    moves = []

    def horizontal(board, key):
        nonlocal moves
        # left to right
        for i in range(len(board)):
            for j in range(len(board)-1):
                if board[i][j] == ' ' and board[i][j + 1] == key:
                    for a in range(j + 1, len(board)):
                        if board[i][a] == ' ':
                            break
                        elif board[i][a] == key:
                            continue
                        elif board[i][a] not in f"{key} ":
                            if (i, j) not in moves:
                                moves.append((i, j))
        # right to left
            for j in range(len(board)-1, 0, -1):
                if board[i][j] == ' ' and board[i][j - 1] == key:
                    for a in range(j-1, -1, -1):
                        if board[i][a] == ' ':
                            break
                        elif board[i][a] == key:
                            continue
                        elif board[i][a] not in f"{key} ":
                            if (i, j) not in moves:
                                moves.append((i, j))

    def vertical(board, key):
        nonlocal moves
        # up to down
        for i in range(len(board)-1):
            for j in range(len(board)):
                if board[i][j] == ' ' and board[i+1][j] == key:
                    for a in range(i + 1, len(board)):
                        if board[a][j] == key:
                            continue
                        elif board[a][j] == ' ':
                            break
                        elif board[a][j] not in f"{key} ":
                            if (i, j) not in moves:
                                moves.append((i, j))
        # down to up
        for i in range(len(board)-1, 0, -1):
            for j in range(len(board)):
                if board[i][j] == ' ' and board[i-1][j] == key:
                    for a in range(i-1, -1, -1):
                        if board[a][j] == ' ':
                            break
                        elif board[a][j] == key:
                            continue
                        elif board[a][j] not in f"{key} ":
                            if (i, j) not in moves:
                                moves.append((i, j))

    def diagonal(board, key):
        nonlocal moves
        i, j = 0, 0
        while (i < len(board) - 1) and (j < len(board)-1):
            if board[i][j] == ' ' and board[i+1][j+1] == key:
                a, b = i + 1, j + 1
                while a < len(board) and b < len(board):
                    if board[a][b] == ' ':
                        break
                    elif board[a][b] == key:
                        a += 1
                        b += 1
                        continue
                    elif board[a][b] not in f"{key} ":
                        if (i, j) not in moves:
                            moves.append((i, j))
                    a += 1
                    b += 1
            i += 1
            j += 1
        i, j = 0, len(board)-1
        while (i < len(board) - 1) and (j >= 0):
            if board[i][j] == ' ' and board[i+1][j-1] == key:
                a, b = i+1, j-1
                while a < len(board) and b >= 0:
                    if board[a][b] == ' ':
                        break
                    elif board[a][b] == key:
                        a += 1
                        b -= 1
                        continue
                    elif board[a][b] not in f"{key} ":
                        if (i, j) not in moves:
                            moves.append((i, j))
                    a += 1
                    b -= 1
            i += 1
            j -= 1
        j, i = 0, len(board)-1
        while (j < len(board) - 1) and (i >= 0):
            if board[i][j] == ' ' and board[i-1][j+1] == key:
                a, b = i-1, j+1
                while b < len(board) and a >= 0:
                    if board[a][b] == ' ':
                        break
                    elif board[a][b] == key:
                        b += 1
                        a -= 1
                        continue
                    elif board[a][b] not in f"{key} ":
                        if (i, j) not in moves:
                            moves.append((i, j))
                    b += 1
                    a -= 1
            j += 1
            i -= 1
        j, i = len(board)-1, len(board)-1
        while (j >= 0) and (i >= 0):
            if board[i][j] == ' ' and board[i-1][j-1] == key:
                a, b = i-1, j-1
                while b >= 0 and a >= 0:
                    if board[a][b] == ' ':
                        break
                    elif board[a][b] == key:
                        b -= 1
                        a -= 1
                        continue
                    elif board[a][b] not in f"{key} ":
                        if (i, j) not in moves:
                            moves.append((i, j))
                    b -= 1
                    a -= 1
            j -= 1
            i -= 1

    for i in 'O@':
        horizontal(board, i)
        vertical(board, i)
        diagonal(board, i)

    return moves
