import pygame

pygame.init()
pygame.display.set_caption("T - Rex")

edge = 28
dis = 2
block = edge + dis
row = col = 20
# window_size = math.sqrt((edge + dis)**2 + row*col)
window_size = (600 + dis, 600 + dis)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
x_img = pygame.transform.smoothscale(pygame.image.load("icons8-x-40.png").convert(), (edge, edge))
o_img = pygame.transform.smoothscale(pygame.image.load("letter-o.png").convert(), (edge, edge))

grid = [[0 for i in range(col)] for j in range(row)]
curr_player = 'o'


def printResult(status):
    # Nothing to do
    if status == -1:
        return True
    # Print result
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    text = font.render('', True, "blue", "black")
    if status == 1:
        text = font.render('X is the winner!', True, "red", "white")
    elif status == 2:
        text = font.render('O is the winner!', True, "blue", "white")
    elif status == 0:
        text = font.render('Draw!', True, "blue", "white")
    textContainer = text.get_rect()
    textContainer.center = (window_size[0] // 2, window_size[1] // 2)
    screen.blit(text, textContainer)
    return False


def winner_check(board):
    for i in range(row):
        for j in range(col):
            # Row check
            if col - j >= 5:
                if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == board[i][j + 4] == 'x':
                    return 1
                elif board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == board[i][j + 4] == 'o':
                    return 2
            # Column check
            if row - i >= 5:
                if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == board[i + 4][j] == 'x':
                    return 1
                elif board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == board[i + 4][j] == 'o':
                    return 2
            # Main diagonal check
            if col - j >= 5 and row - i >= 5:
                if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] ==\
                        board[i + 4][j + 4] == 'x':
                    return 1
                elif board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] ==\
                        board[i + 4][j + 4] == 'o':
                    return 2
            # Counter-diagonal check
            if j > 3 and row - i >= 5:
                if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] ==\
                        board[i + 4][j - 4] == 'x':
                    return 1
                elif board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] ==\
                        board[i + 4][j - 4] == 'o':
                    return 2
    count = 0
    for i in range(row):
        count += board[i].count(0)
    if count == 0:
        return 0
    return -1


running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                pos = pygame.mouse.get_pos()
                x = pos[1] // block
                y = pos[0] // block
                if grid[x][y] == 0:
                    if curr_player == 'x':
                        grid[x][y] = 'x'
                        curr_player = 'o'
                    else:
                        grid[x][y] = 'o'
                        curr_player = 'x'
        check = winner_check(grid)
    screen.fill("black")
    for i in range(row):
        for j in range(col):
            pygame.draw.rect(screen, "white", (block * j + dis, block * i + dis, edge, edge))
            if grid[i][j] == 'x':
                screen.blit(x_img, (block * j + dis, block * i + dis))
            if grid[i][j] == 'o':
                screen.blit(o_img, (block * j + dis, block * i + dis))
    running = printResult(check)
    pygame.display.update()

pygame.time.delay(2000)
pygame.quit()
