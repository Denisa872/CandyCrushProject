import random


# Inițializarea matricei de bomboane 11x11 cu valori aleatorii
def initialize_board(size=11):
    return [[random.randint(1, 4) for _ in range(size)] for _ in range(size)]


# Afișarea matricei
def print_board(board):
    for row in board:
        print(' '.join(map(str, row)))
    print()


# Detectare linie de 3 pe orizontală și verticală
def detect_matches(board):
    matches = []
    # Detectare orizontală
    for i in range(len(board)):
        for j in range(len(board[i]) - 2):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] != 0:
                matches.append((i, j, 'horiz'))  # h = orizontal
    # Detectare verticală
    for j in range(len(board[0])):
        for i in range(len(board) - 2):
            if board[i][j] == board[i + 1][j] == board[i + 2][j] != 0:
                matches.append((i, j, 'vert'))  # v = vertical
    return matches


# Eliminare bomboane și actualizare scor
def remove_matches(board, matches):
    score = 0
    for match in matches:
        i, j, direction = match
        if direction == 'horiz':
            for k in range(3):
                board[i][j + k] = 0  # eliminăm linia orizontală
            score += 5  # 5 puncte pentru fiecare linie de 3
        elif direction == 'vert':
            for k in range(3):
                board[i + k][j] = 0  # eliminăm linia verticală
            score += 5
    return score


# Bomboanele cad în jos pentru a umple spațiile goale
def drop_candies(board):
    size = len(board)
    for j in range(size):
        column = [board[i][j] for i in range(size) if board[i][j] != 0]
        column = [0] * (size - len(column)) + column  # Adăugăm zerouri la început (bomboanele cad)
        for i in range(size):
            board[i][j] = column[i]


# Generăm noi bomboane pentru a completa spațiile goale
def refill_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                board[i][j] = random.randint(1, 4)


# Încearcă să facă un swap între două bomboane pentru a crea o nouă formațiune
def try_swap(board):
    size = len(board)
    for i in range(size):
        for j in range(size - 1):
            # Interschimbare pe orizontală
            board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]
            if detect_matches(board):
                return True
            board[i][j], board[i][j + 1] = board[i][j + 1], board[i][j]  # Revenim la poziția inițială

            # Interschimbare pe verticală
            if i < size - 1:
                board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]
                if detect_matches(board):
                    return True
                board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]  # Revenim la poziția inițială
    return False


# Funcția principală a jocului
def play_game():
    board = initialize_board()
    total_score = 0

    while total_score < 10000:
        matches = detect_matches(board)
        if matches:
            score = remove_matches(board, matches)
            total_score += score
            drop_candies(board)
            refill_board(board)
        else:
            # Dacă nu mai sunt formațiuni, încercăm să facem un swap
            if not try_swap(board):
                break

    return total_score


# Jucăm jocul de 100 de ori și calculăm media scorului
def run_simulation(num_games=100):
    scores = []
    for _ in range(num_games):
        print(f"Jocul {_ + 1} din {num_games}")
        score = play_game()
        scores.append(score)
        print(f"Scorul obținut în jocul {_ + 1}: {score}")

    avg_score = sum(scores) / num_games
    print(f"Scorul mediu după {num_games} jocuri: {avg_score}")


# Rulează simularea cu 100 de jocuri diferite
run_simulation()


