def displayArt():
    import random

    s = 0
    for i in range(4):
        s += random.randint(1, 25)
    if s >= 85:
        for i in open(f"othello\\reversiNames\\10lo", "r").read():
            print(i, end='')
        open(f"othello\\reversiNames\\10lo", "r").close()

    else:
        logo = random.randint(1, 9)
        for i in open(f"othello\\reversiNames\\{str(logo)}lo", "r").read():
            print(i, end='')
        open(f"othello\\reversiNames\\{str(logo)}lo", "r").close()
    print('\n')
    print("If you haven't played the game before, press y for instructions. Press anything else if you have.")
    if input() in 'Yy':
        print('\n\n')
        for i in open("othello\\instructions").read():
            print(i, end='')
        open("othello\\instructions").close()
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
    xPosition, yPosition = base[0], base[1]
    horizontalPos, verticalPos, diagonalPos = [], [], []

    def horizontal(board, xPosition, yPosition, key, sign=1):

        nonlocal horizontalPos
        if sign == 1:
            for iterationY in range(yPosition + 1, len(board)):
                if board[xPosition][iterationY] == ' ':
                    break
                elif board[xPosition][iterationY] != key:
                    continue
                elif (board[xPosition][iterationY] == key) and (iterationY != yPosition):
                    if iterationY - 1 > yPosition:
                        if (board[xPosition][iterationY-1] not in [key, ' ']):
                            horizontalPos.append([xPosition, iterationY])
                            break
                else:
                    continue
        else:
            for iterationY in range(yPosition-1, -1, -1):
                if board[xPosition][iterationY] == ' ':
                    break
                elif board[xPosition][iterationY] != key:
                    continue
                elif (board[xPosition][iterationY] == key) and (iterationY != yPosition):
                    if iterationY + 1 < yPosition:
                        if (board[xPosition][iterationY+1] not in [key, ' ']):
                            horizontalPos.append([xPosition, iterationY])
                            break
                else:
                    continue

        if sign == -1:
            return horizontalPos
        else:
            return horizontal(board, xPosition, yPosition, key, -1)

    def vertical(board, xPosition, yPosition, key, sign=1):

        nonlocal verticalPos
        if sign == 1:
            for iterationX in range(xPosition, len(board)):
                if board[iterationX][yPosition] == ' ':
                    break
                elif board[iterationX][yPosition] != key:
                    continue
                elif (board[iterationX][yPosition] == key) and (iterationX != xPosition):
                    if iterationX - 1 > xPosition:
                        if (board[iterationX-1][yPosition] not in [key, ' ']):
                            verticalPos.append([iterationX, yPosition])
                            break
                else:
                    continue
        else:
            for iterationX in range(xPosition, -1, -1):
                if board[iterationX][yPosition] == ' ':
                    break
                elif board[iterationX][yPosition] != key:
                    continue
                elif (board[iterationX][yPosition] == key) and (iterationX != xPosition):
                    if iterationX + 1 < xPosition:
                        if (board[iterationX+1][yPosition] not in [key, ' ']):
                            verticalPos.append([iterationX, yPosition])
                            break

                else:
                    continue

        if sign == -1:
            return verticalPos
        else:
            return vertical(board, xPosition, yPosition, key, -1)

    def diagonal(board,  xPosition, yPosition, key, signs):

        nonlocal diagonalPos
        sign1, sign2 = signs
        continuityCheckerX, continuityCheckerY = xPosition, yPosition
        while (0 <= continuityCheckerX < len(board)) and (0 <= continuityCheckerY < len(board)):
            if board[continuityCheckerX][continuityCheckerY] == ' ':
                break
            elif board[continuityCheckerX][continuityCheckerY] != key:
                continuityCheckerX += sign1
                continuityCheckerY += sign2
                continue
            elif (board[continuityCheckerX][continuityCheckerY] == key) and ([continuityCheckerX, continuityCheckerY] not in diagonalPos) and ([continuityCheckerX, continuityCheckerY] != [xPosition, yPosition]) and (board[continuityCheckerX - (sign1)][continuityCheckerY-(sign2)] not in [key, ' ']):
                diagonalPos.append([continuityCheckerX, continuityCheckerY])
                break

            continuityCheckerX += sign1
            continuityCheckerY += sign2

    values = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    for i in values:
        diagonal(board, xPosition, yPosition, key, i)

    horizontal(board, xPosition, yPosition, key)
    vertical(board, xPosition, yPosition, key)
    return [[verticalPos], [horizontalPos], [diagonalPos]]


def allMoves(board):

    moves = []

    def horizontal(board, key):
        nonlocal moves
        # left to right
        for iterationX in range(len(board)):
            for iterationY in range(len(board)-1):
                if board[iterationX][iterationY] == ' ' and board[iterationX][iterationY + 1] == key:
                    for continuityCheckerX in range(iterationY + 1, len(board)):
                        if board[iterationX][continuityCheckerX] == ' ':
                            break
                        elif board[iterationX][continuityCheckerX] == key:
                            continue
                        elif board[iterationX][continuityCheckerX] not in f"{key} ":
                            if (iterationX, iterationY) not in moves:
                                moves.append((iterationX, iterationY))
        # right to left
            for iterationY in range(len(board)-1, 0, -1):
                if board[iterationX][iterationY] == ' ' and board[iterationX][iterationY - 1] == key:
                    for continuityCheckerX in range(iterationY-1, -1, -1):
                        if board[iterationX][continuityCheckerX] == ' ':
                            break
                        elif board[iterationX][continuityCheckerX] == key:
                            continue
                        elif board[iterationX][continuityCheckerX] not in f"{key} ":
                            if (iterationX, iterationY) not in moves:
                                moves.append((iterationX, iterationY))

    def vertical(board, key):
        nonlocal moves
        # up to down
        for iterationX in range(len(board)-1):
            for iterationY in range(len(board)):
                if board[iterationX][iterationY] == ' ' and board[iterationX+1][iterationY] == key:
                    for continuityCheckerX in range(iterationX + 1, len(board)):
                        if board[continuityCheckerX][iterationY] == key:
                            continue
                        elif board[continuityCheckerX][iterationY] == ' ':
                            break
                        elif board[continuityCheckerX][iterationY] not in f"{key} ":
                            if (iterationX, iterationY) not in moves:
                                moves.append((iterationX, iterationY))
        # down to up
        for iterationX in range(len(board)-1, 0, -1):
            for iterationY in range(len(board)):
                if board[iterationX][iterationY] == ' ' and board[iterationX-1][iterationY] == key:
                    for continuityCheckerX in range(iterationX-1, -1, -1):
                        if board[continuityCheckerX][iterationY] == ' ':
                            break
                        elif board[continuityCheckerX][iterationY] == key:
                            continue
                        elif board[continuityCheckerX][iterationY] not in f"{key} ":
                            if (iterationX, iterationY) not in moves:
                                moves.append((iterationX, iterationY))

    def diagonal(board, key):
        nonlocal moves
        iterationX, iterationY = 0, 0
        while (iterationX < len(board) - 1) and (iterationY < len(board)-1):
            if board[iterationX][iterationY] == ' ' and board[iterationX+1][iterationY+1] == key:
                continuityCheckerX, continuityCheckerY = iterationX + 1, iterationY + 1
                while continuityCheckerX < len(board) and continuityCheckerY < len(board):
                    if board[continuityCheckerX][continuityCheckerY] == ' ':
                        break
                    elif board[continuityCheckerX][continuityCheckerY] == key:
                        continuityCheckerX += 1
                        continuityCheckerY += 1
                        continue
                    elif board[continuityCheckerX][continuityCheckerY] not in f"{key} ":
                        if (iterationX, iterationY) not in moves:
                            moves.append((iterationX, iterationY))
                    continuityCheckerX += 1
                    continuityCheckerY += 1
            iterationX += 1
            iterationY += 1
        iterationX, iterationY = 0, len(board)-1
        while (iterationX < len(board) - 1) and (iterationY >= 0):
            if board[iterationX][iterationY] == ' ' and board[iterationX+1][iterationY-1] == key:
                continuityCheckerX, continuityCheckerY = iterationX+1, iterationY-1
                while continuityCheckerX < len(board) and continuityCheckerY >= 0:
                    if board[continuityCheckerX][continuityCheckerY] == ' ':
                        break
                    elif board[continuityCheckerX][continuityCheckerY] == key:
                        continuityCheckerX += 1
                        continuityCheckerY -= 1
                        continue
                    elif board[continuityCheckerX][continuityCheckerY] not in f"{key} ":
                        if (iterationX, iterationY) not in moves:
                            moves.append((iterationX, iterationY))
                    continuityCheckerX += 1
                    continuityCheckerY -= 1
            iterationX += 1
            iterationY -= 1
        iterationY, iterationX = 0, len(board)-1
        while (iterationY < len(board) - 1) and (iterationX >= 0):
            if board[iterationX][iterationY] == ' ' and board[iterationX-1][iterationY+1] == key:
                continuityCheckerX, continuityCheckerY = iterationX-1, iterationY+1
                while continuityCheckerY < len(board) and continuityCheckerX >= 0:
                    if board[continuityCheckerX][continuityCheckerY] == ' ':
                        break
                    elif board[continuityCheckerX][continuityCheckerY] == key:
                        continuityCheckerY += 1
                        continuityCheckerX -= 1
                        continue
                    elif board[continuityCheckerX][continuityCheckerY] not in f"{key} ":
                        if (iterationX, iterationY) not in moves:
                            moves.append((iterationX, iterationY))
                    continuityCheckerY += 1
                    continuityCheckerX -= 1
            iterationY += 1
            iterationX -= 1
        iterationY, iterationX = len(board)-1, len(board)-1
        while (iterationY >= 0) and (iterationX >= 0):
            if board[iterationX][iterationY] == ' ' and board[iterationX-1][iterationY-1] == key:
                continuityCheckerX, continuityCheckerY = iterationX-1, iterationY-1
                while continuityCheckerY >= 0 and continuityCheckerX >= 0:
                    if board[continuityCheckerX][continuityCheckerY] == ' ':
                        break
                    elif board[continuityCheckerX][continuityCheckerY] == key:
                        continuityCheckerY -= 1
                        continuityCheckerX -= 1
                        continue
                    elif board[continuityCheckerX][continuityCheckerY] not in f"{key} ":
                        if (iterationX, iterationY) not in moves:
                            moves.append((iterationX, iterationY))
                    continuityCheckerY -= 1
                    continuityCheckerX -= 1
            iterationY -= 1
            iterationX -= 1

    for iterator in 'O@':
        horizontal(board, iterator)
        vertical(board, iterator)
        diagonal(board, iterator)

    return moves


'''def dumbo(moves, board, key):
    import random
    choice = random.choice(moves)
    flipPieces(board, choice, checkMove(board, choice, key), key)
'''
