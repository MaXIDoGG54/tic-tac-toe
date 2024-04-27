import pygame

VICTORIES = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(2, 0), (1, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
]

MAP = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def draw_cells(surface):
    for x in range(3):
        for y in range(3):
            pygame.draw.rect(
                surface=surface,
                color="white",
                rect=(
                    horizontal_cell_size * x,
                    vertical_cell_size * y,
                    horizontal_cell_size,
                    vertical_cell_size,
                ),
                width=3,
            )


def set_shape(x, y, player, surface, cell_size):
    width, height = cell_size
    for i in range(3):
        for j in range(3):
            if i * width < x < (i + 1) * width and j * height < y < (j + 1) * height:
                if MAP[j][i]:
                    return False
                if player == 1:
                    MAP[j][i] = "O"
                    cell_center = (i * width + width // 2, j * height + height // 2)
                    pygame.draw.circle(
                        surface, "red", cell_center, radius=width // 2, width=10
                    )
                else:
                    MAP[j][i] = "X"
                    pygame.draw.line(
                        surface,
                        "blue",
                        (i * width, j * height),
                        (i * width + width, j * height + height),
                        width=10,
                    )
                    pygame.draw.line(
                        surface,
                        "blue",
                        (i * width + width, j * height),
                        (i * width, j * height + height),
                        width=10,
                    )
    return True


def check_win():
    win = None

    number_of_empty_cells = 0
    for row in MAP:
        for cell in row:
            if cell == 0:
                number_of_empty_cells += 1
    if number_of_empty_cells == 0:
        win = "-"

    for combo in VICTORIES:
        x1, y1 = combo[0]
        x2, y2 = combo[1]
        x3, y3 = combo[2]

        if MAP[x1][y1] == "X" and MAP[x2][y2] == "X" and MAP[x3][y3] == "X":
            win = "X"
        elif MAP[x1][y1] == "O" and MAP[x2][y2] == "O" and MAP[x3][y3] == "O":
            win = "O"

    return win


def draw_win(win, surface):
    font = pygame.font.SysFont("Consolas", 36)
    text = font.render(f"Победитель: {win}", False, "green")
    surface.blit(text, (10, 10))


print(pygame.font.get_fonts())

pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 300, 300
screen = pygame.display.set_mode(SCREEN_SIZE)

horizontal_cell_size = SCREEN_WIDTH // 3
vertical_cell_size = SCREEN_HEIGHT // 3

clock = pygame.time.Clock()

current_player = 1

end_game = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not end_game:
                start_game = True
                mouse_pos = event.pos
                x, y = mouse_pos

                status = set_shape(
                    x,
                    y,
                    current_player,
                    screen,
                    (horizontal_cell_size, vertical_cell_size),
                )

                if status:
                    if current_player == 1:
                        current_player = 2
                    else:
                        current_player = 1

    draw_cells(screen)

    result = check_win()
    if result:
        end_game = True
        draw_win(result, screen)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
