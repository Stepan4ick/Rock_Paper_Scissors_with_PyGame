import pygame, sys
from random import randint, choice

WIDTH, HEIGHT = 1200, 750
GAME_TITLE = "Камень, ножницы, бумага!"
WINDOW_ICON = "images\\window_icon.png"
FZ_CHOICE = int(HEIGHT//18)
FZ_MAIN = int(HEIGHT // 35 * 2.5)
FZ_MID = int(HEIGHT // 22)
FZ_GAME = int(HEIGHT // 14)
TAB_X = (WIDTH - 270) // 4   # 270px - это сумма всех ширин картинок для выбора
TAB_Y = int(HEIGHT // 20)
ASSORTIMENT = ["камень", "ножницы", "бумага"]
MAX_SCORE = 5

# Colors
BACKGROUND_COLOR = (161,104,213)   #  #A168D5
TEXT_COLOR = (255,248,114)         #  #FFF872
TEXT_COLOR_EASY = (156,239,107)    #  #9CEF6B
TEXT_COLOR_MEDIUM = (255,217,114)  #  #FFD972
TEXT_COLOR_HARD = (162,36,51)      #  #A22433

def main():
    screen, clock = init_pygame()
    game_state = init_game_state()
    all_icons = list(load_images())
    while game_state["program_running"]:
        clock.tick(30)
        events = get_events()
        update_game_state(game_state, events)
        update_screen(screen, game_state, all_icons)
    close_game()

def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    icon = pygame.image.load(WINDOW_ICON)
    pygame.display.set_icon(icon)
    return screen, clock

def load_images():
    main_icon = pygame.image.load("images\\icon.png")
    rock = pygame.image.load("images\\КАМЕНЬ.png")
    paper = pygame.image.load("images\\БУМАГА.png")
    scissors = pygame.image.load("images\\НОЖНИЦЫ.png")
    big_rock = pygame.image.load("images\\КАМЕНЬ БОЛЬШОЙ.png")
    big_paper = pygame.image.load("images\\БУМАГА БОЛЬШАЯ.png")
    big_scissors = pygame.image.load("images\\НОЖНИЦЫ БОЛЬШИЕ.png")
    evil_rock = pygame.image.load("images\\КАМЕНЬ КОМПА.png")
    evil_paper = pygame.image.load("images\\БУМАГА КОМПА.png")
    evil_scissors = pygame.image.load("images\\НОЖНИЦЫ КОМПА.png")
    human_icon = pygame.image.load("images\\Человечек 128.png")
    computer_lose = pygame.image.load("images\\computer lose 256.png")
    human_lose = pygame.image.load("images\\human lose 256.png")
    return main_icon, rock, paper, scissors, big_rock, big_paper, big_scissors, evil_rock, evil_paper, evil_scissors, human_icon, computer_lose, human_lose

def init_game_state():
    game_state = {
        "program_running": True, 
        "game_running": False,
        "choice_dificulty": False,
        "game_paused": False,
        "human_score": 0,
        "computer_score": 0,
        "human_choice": "undefind",
        "computer_choice": "undefind",
        "last_human_choice": "камень",
        "last_computer_choice": "камень",
        "computer_icon": "",
        "round_winner": "undefind",
        "winner": "undefind",
        "dificulty": "undefind",
        "mouse_pos": 0,
        "rounds": 1,
        "coord_x": [WIDTH//2-int(FZ_CHOICE*9.5), WIDTH//2-int(FZ_CHOICE*5.5), 
                    WIDTH//2-int(FZ_CHOICE*2.5), WIDTH//2+FZ_CHOICE,
                    WIDTH//2+int(FZ_CHOICE*5.5), WIDTH//2+FZ_CHOICE*10],
        "coord_y": [HEIGHT-TAB_Y*8-FZ_CHOICE, HEIGHT-TAB_Y*8,
                    HEIGHT-TAB_Y*8-FZ_CHOICE, HEIGHT-TAB_Y*8,
                    HEIGHT-TAB_Y*8-FZ_CHOICE, HEIGHT-TAB_Y*8]
    }
    return game_state

def get_events():
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            events.append("quit")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                events.append("enter")
            elif event.key == pygame.K_ESCAPE:
                events.append("escape")
            elif event.key == pygame.K_SPACE:
                events.append("space")
        elif event.type == pygame.MOUSEMOTION:
            events.append("motion")
            events.insert(0, event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
            events.append("click")
            events.insert(0, event.pos)
    return events

def update_game_state(game_state, events):
    check_keys(game_state, events)
    if game_state["winner"] == "undefind" and game_state["dificulty"] != "undefind":
        if game_state["dificulty"] == "hard":
            game_state["computer_icon"] = pygame.image.load("images\\Злой комп 128.png")
        else:
            game_state["computer_icon"] = pygame.image.load("images\\Добрый комп 128.png")
        if game_state["round_winner"] != "undefind" and game_state["winner"] == "undefind":
            new_round(game_state)
        elif game_state["human_choice"] != "undefind":
            computer_move(game_state, game_state["dificulty"])
            analysis(game_state)
    elif game_state["winner"] != "undefind":
        game_state["game_running"] = False

def check_keys(game_state, events):
    if "quit" in events:
        game_state["program_running"] = False
    elif not game_state["game_running"]:
        if "escape" in events:
            game_state["program_running"] = False
        elif "enter" in events:
            game_state["game_running"] = True
            init_new_game(game_state)
    elif game_state["choice_dificulty"]:
        if "motion" in events:
            game_state["mouse_pos"] = events[0]
            change_cursor(game_state, game_state["mouse_pos"])
        if "click" in events:
            game_state["mouse_pos"] = events[0]
            check_click_choice(game_state, game_state["mouse_pos"])
    elif game_state["game_paused"]:
        if "space" in events:
            game_state["game_paused"] = False
        elif "escape" in events:
            game_state["game_running"] = False
    else:
        if "escape" in events or "space" in events:
            game_state["game_paused"] = True
        if "motion" in events:
            game_state["mouse_pos"] = events[0]
        if "click" in events:
            game_state["mouse_pos"] = events[0]
            check_click_game(game_state, game_state["mouse_pos"])
        change_cursor(game_state, game_state["mouse_pos"])

def check_click_choice(game_state, pos):
    x, y = pos
    if game_state["coord_x"][0] <= x <= game_state["coord_x"][1] and game_state["coord_y"][0] <= y <= game_state["coord_y"][1]:
        game_state["dificulty"] = "easy"
        game_state["choice_dificulty"] = False
        game_state["coord_x"] = [TAB_X, TAB_X+100, TAB_X*2+100, TAB_X*2+184, WIDTH-TAB_X-86, WIDTH-TAB_X]
        game_state["coord_y"] = [HEIGHT-TAB_Y-199, HEIGHT-TAB_Y, HEIGHT-TAB_Y-194, HEIGHT-TAB_Y, HEIGHT-TAB_Y-197, HEIGHT-TAB_Y]
    elif game_state["coord_x"][2] <= x <= game_state["coord_x"][3] and game_state["coord_y"][2] <= y <= game_state["coord_y"][3]:
        game_state["dificulty"] = "medium"
        game_state["choice_dificulty"] = False
        game_state["coord_x"] = [TAB_X, TAB_X+100, TAB_X*2+100, TAB_X*2+184, WIDTH-TAB_X-86, WIDTH-TAB_X]
        game_state["coord_y"] = [HEIGHT-TAB_Y-199, HEIGHT-TAB_Y, HEIGHT-TAB_Y-194, HEIGHT-TAB_Y, HEIGHT-TAB_Y-197, HEIGHT-TAB_Y]
    elif game_state["coord_x"][4] <= x <= game_state["coord_x"][5] and game_state["coord_y"][4] <= y <= game_state["coord_y"][5]:
        game_state["dificulty"] = "hard"
        game_state["choice_dificulty"] = False
        game_state["coord_x"] = [TAB_X, TAB_X+100, TAB_X*2+100, TAB_X*2+184, WIDTH-TAB_X-86, WIDTH-TAB_X]
        game_state["coord_y"] = [HEIGHT-TAB_Y-199, HEIGHT-TAB_Y, HEIGHT-TAB_Y-194, HEIGHT-TAB_Y, HEIGHT-TAB_Y-197, HEIGHT-TAB_Y]

def check_click_game(game_state, pos):
    x, y = pos
    if game_state["coord_x"][0] <= x <= game_state["coord_x"][1] and game_state["coord_y"][0] <= y <= game_state["coord_y"][1]:
        game_state["human_choice"] = "бумага"
    elif game_state["coord_x"][2] <= x <= game_state["coord_x"][3] and game_state["coord_y"][2] <= y <= game_state["coord_y"][3]:
        game_state["human_choice"] = "камень"
    elif game_state["coord_x"][4] <= x <= game_state["coord_x"][5] and game_state["coord_y"][4] <= y <= game_state["coord_y"][5]:
        game_state["human_choice"] = "ножницы"

def change_cursor(game_state, pos):
    x, y = pos
    cursor = pygame.SYSTEM_CURSOR_ARROW
    if (game_state["coord_x"][0] <= x <= game_state["coord_x"][1] and game_state["coord_y"][0] <= y <= game_state["coord_y"][1] or
        game_state["coord_x"][2] <= x <= game_state["coord_x"][3] and game_state["coord_y"][2] <= y <= game_state["coord_y"][3] or
        game_state["coord_x"][4] <= x <= game_state["coord_x"][5] and game_state["coord_y"][4] <= y <= game_state["coord_y"][5]) and not game_state["game_paused"] and game_state["game_running"] and game_state["human_choice"] == "undefind" and game_state["winner"] == "undefind":
        cursor = pygame.SYSTEM_CURSOR_HAND
    pygame.mouse.set_cursor(cursor)

def computer_move(game_state, dificulty):
    if dificulty == "easy" or game_state["last_computer_choice"] == game_state["last_human_choice"]:
            game_state["computer_choice"] = choice(ASSORTIMENT)
            if game_state["computer_choice"] == game_state["human_choice"] and 0 <= randint(0, 100) <= 60:
                while game_state["computer_choice"] == game_state["human_choice"]:
                    game_state["computer_choice"] = choice(ASSORTIMENT)
    elif dificulty == "medium":
        if game_state["last_human_choice"] == "камень" and game_state["last_computer_choice"] == "бумага":
            game_state["computer_choice"] = "ножницы"
        elif game_state["last_human_choice"] == "бумага" and game_state["last_computer_choice"] == "ножницы":
            game_state["computer_choice"] = "камень"
        elif game_state["last_human_choice"] == "ножницы" and game_state["last_computer_choice"] == "камень":
            game_state["computer_choice"] = "бумага"
        elif game_state["last_human_choice"] == "камень" and game_state["last_computer_choice"] == "ножницы":
            game_state["computer_choice"] = "камень"
        elif game_state["last_human_choice"] == "бумага" and game_state["last_computer_choice"] == "камень":
            game_state["computer_choice"] = "бумага"
        elif game_state["last_human_choice"] == "ножницы" and game_state["last_computer_choice"] == "бумага":
            game_state["computer_choice"] = "ножницы"
    else:
        if game_state["human_choice"] == "камень" and randint(1, 100) <= 90:
            game_state["computer_choice"] = "бумага"
        elif game_state["human_choice"] == "бумага" and randint(1, 100) <= 90:
            game_state["computer_choice"] = "ножницы"
        elif game_state["human_choice"] == "ножницы" and randint(1, 100) <= 90:
            game_state["computer_choice"] = "камень"
        else:
            game_state["computer_choice"] = choice(ASSORTIMENT)

def analysis(game_state):
    if (game_state["human_choice"] == "бумага" and game_state["computer_choice"] == "камень" or
            game_state["human_choice"] == "камень" and game_state["computer_choice"] == "ножницы" or 
            game_state["human_choice"] == "ножницы" and game_state["computer_choice"] == "бумага"):
            game_state["human_score"] += 1
            game_state["round_winner"] = "Человек"
    elif game_state["human_choice"] == game_state["computer_choice"]:
        game_state["round_winner"] = "Ничья"
    else:
        game_state["computer_score"] += 1
        game_state["round_winner"] = "Компьютер"
    check_winner(game_state)

def new_round(game_state):
    game_state["rounds"] += 1
    if game_state["rounds"] != 1:
        game_state["last_human_choice"] = game_state["human_choice"]
        game_state["last_computer_choice"] = game_state["computer_choice"]
    game_state["human_choice"] = "undefind"
    game_state["computer_choice"] = "undefind"
    game_state["round_winner"] = "undefind"

def check_winner(game_state):
    if game_state["human_score"] == MAX_SCORE:
        game_state["winner"] = "Человек"
    elif game_state["computer_score"] == MAX_SCORE:
        game_state["winner"] = "Компьютер"

def update_screen(screen, game_state, all_icons):
    main_icon, rock, paper, scissors, big_rock, big_paper, big_scissors, evil_rock, evil_paper, evil_scissors, human_icon, computer_lose, human_lose = all_icons
    screen.fill(BACKGROUND_COLOR)
    if not game_state["game_running"]:
        print_welcome(screen, main_icon)
    elif game_state["choice_dificulty"]:
        print_choice_dificulty(screen, game_state["coord_x"], game_state["coord_y"])
    elif game_state["game_paused"]:
        print_pause(screen, human_icon, game_state["computer_icon"], game_state["human_score"], game_state["computer_score"])
    else:
        if game_state["winner"] == "undefind":
            print_scores(screen, game_state["human_score"], game_state["computer_score"], human_icon, game_state["computer_icon"])
            print_rounds(screen, game_state["rounds"])
            if game_state["human_choice"] == "undefind":
                print_choice(screen, game_state, paper, rock, scissors)
            else:
                print_particular_choice(screen, big_paper, big_rock, big_scissors, game_state["human_choice"])
                waiting(screen)
                cleaning(screen, game_state["human_score"], game_state["computer_score"], human_icon, game_state["computer_icon"], game_state["rounds"], game_state, big_paper, big_rock, big_scissors)
                print_computer_choice(screen, game_state["computer_choice"], evil_rock, evil_paper, evil_scissors)
                print_round_winner(screen, game_state["round_winner"])
                pygame.display.flip()
                pygame.time.wait(1800)
        else:
            print_rounds(screen, game_state["rounds"])
            print_scores(screen, game_state["human_score"], game_state["computer_score"], human_icon, game_state["computer_icon"])
            print_particular_choice(screen, big_paper, big_rock, big_scissors, game_state["human_choice"])
            waiting(screen)
            cleaning(screen, game_state["human_score"], game_state["computer_score"], human_icon, game_state["computer_icon"], game_state["rounds"], game_state, big_paper, big_rock, big_scissors)
            print_computer_choice(screen, game_state["computer_choice"], evil_rock, evil_paper, evil_scissors)
            print_round_winner(screen, game_state["round_winner"])
            pygame.display.flip()
            pygame.time.wait(1800)
            print_winner(screen, game_state["winner"], computer_lose, human_lose, game_state["human_score"], game_state["computer_score"])
            pygame.display.flip()
            pygame.time.wait(5000)
    pygame.display.flip()

def print_welcome(screen, icon):
    icon_rect = icon.get_rect()                                        # Main Icon
    icon_rect.centerx = WIDTH//2
    icon_rect.centery = TAB_Y + 64
    main_font = pygame.font.SysFont("Courier New", FZ_MAIN, bold=True) # Main name
    game_name_text = main_font.render(GAME_TITLE, True, TEXT_COLOR)
    game_name_text_rect = game_name_text.get_rect()
    game_name_text_rect.centerx = WIDTH//2
    game_name_text_rect.centery = 128 + TAB_Y*3
    font = pygame.font.SysFont("Courier New", FZ_MID, bold=True)       # Arrow Text
    text1 = "Нажмите Enter для начала игры"
    text2 = "Нажмите Escape для выхода"
    arrow_text1 = font.render(text1, True, TEXT_COLOR)
    arrow_text2 = font.render(text2, True, TEXT_COLOR)
    arrow_text1_rect, arrow_text2_rect = arrow_text1.get_rect(), arrow_text2.get_rect()
    arrow_text1_rect.center = (WIDTH//2, HEIGHT//2 + TAB_Y*4)
    arrow_text2_rect.center = (WIDTH//2, HEIGHT//2 + TAB_Y*6)
    screen.blit(icon, icon_rect)
    screen.blit(game_name_text, game_name_text_rect)
    screen.blit(arrow_text1, arrow_text1_rect)
    screen.blit(arrow_text2, arrow_text2_rect)

def print_choice_dificulty(screen, coord_x, coord_y):
    main_font = pygame.font.SysFont("Courier New", FZ_MAIN, bold=True)
    text = "Выбери уровень сложности"
    main_text = main_font.render(text, True, TEXT_COLOR)
    main_text_rect = main_text.get_rect()
    main_text_rect.center = (WIDTH//2, TAB_Y + FZ_MAIN)
    font_choice = pygame.font.SysFont("Courier New", FZ_CHOICE, bold=True)
    text_easy = font_choice.render("Лёгкий", True, TEXT_COLOR_EASY)
    text_medium = font_choice.render("Средний", True, TEXT_COLOR_MEDIUM)
    text_hard = font_choice.render("Сложный", True, TEXT_COLOR_HARD)
    text_easy_rect = text_easy.get_rect()
    text_medium_rect = text_medium.get_rect()
    text_hard_rect = text_hard.get_rect()
    text_easy_rect.bottomleft = (coord_x[0], coord_y[1])
    text_medium_rect.bottomleft = (coord_x[2], coord_y[3])
    text_hard_rect.bottomleft = (coord_x[4], coord_y[5])
    screen.blit(main_text, main_text_rect)
    screen.blit(text_easy, text_easy_rect)
    screen.blit(text_medium, text_medium_rect)
    screen.blit(text_hard, text_hard_rect)

def print_pause(screen, human_icon, computer_icon, human_score, computer_score):
    main_font = pygame.font.SysFont("Courier New", FZ_MAIN, bold=True)
    text_pause = main_font.render("Игра на Паузе", True, TEXT_COLOR)
    text_pause_rect = text_pause.get_rect()
    text_pause_rect.center = (WIDTH//2, TAB_Y*3+FZ_MAIN)
    arrow_font = pygame.font.SysFont("Courier New", FZ_MID, bold=True)
    text1 = "Нажмите Space для продолжения игры"
    text2 = "Нажмите Escape для выхода в главное меню"
    arrow_text1 = arrow_font.render(text1, True, TEXT_COLOR)
    arrow_text2 = arrow_font.render(text2, True, TEXT_COLOR)
    arrow_text1_rect = arrow_text1.get_rect()
    arrow_text2_rect = arrow_text2.get_rect()
    arrow_text1_rect.center = (WIDTH//2, TAB_Y*11)
    arrow_text2_rect.center = (WIDTH//2, TAB_Y*11 + FZ_MID*2)
    screen.blit(text_pause, text_pause_rect)
    screen.blit(arrow_text1, arrow_text1_rect)
    screen.blit(arrow_text2, arrow_text2_rect)
    print_scores(screen, human_score, computer_score, human_icon, computer_icon)

def print_scores(screen, human_score, computer_score, human_icon, computer_icon):
    font = pygame.font.SysFont("Courier New", FZ_GAME, bold=True)
    human_icon_rect = human_icon.get_rect()
    computer_icon_rect = computer_icon.get_rect()
    human_icon_rect.topleft = (0, 0)
    computer_icon_rect.topright = (WIDTH, 0)
    text_human_score = font.render(str(human_score), True, TEXT_COLOR)
    text_computer_score = font.render(str(computer_score), True, TEXT_COLOR)
    text_human_score_rect = text_human_score.get_rect()
    text_computer_score_rect = text_computer_score.get_rect()
    text_human_score_rect.center = (64, 128 + 15)
    text_computer_score_rect.center = (WIDTH-64, 128 + 15)
    screen.blit(human_icon, human_icon_rect)
    screen.blit(computer_icon, computer_icon_rect)
    screen.blit(text_human_score, text_human_score_rect)
    screen.blit(text_computer_score, text_computer_score_rect)

def print_rounds(screen, rounds):
    font = pygame.font.SysFont("Courier New", FZ_GAME, bold=True)
    text = font.render("Раунд " + str(rounds), True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH//2, FZ_GAME)
    screen.blit(text, text_rect)

def print_choice(screen, game_state, paper, rock, scissors):
    paper_rect = paper.get_rect()
    rock_rect = rock.get_rect()
    scissors_rect = scissors.get_rect()
    paper_rect.bottomleft = (game_state["coord_x"][0], game_state["coord_y"][1])
    rock_rect.bottomleft = (game_state["coord_x"][2], game_state["coord_y"][3])
    scissors_rect.bottomleft = (game_state["coord_x"][4], game_state["coord_y"][5])
    screen.blit(paper, paper_rect)
    screen.blit(rock, rock_rect)
    screen.blit(scissors,scissors_rect)

def print_particular_choice(screen, big_paper, big_rock, big_scissors, choice):
    big_paper_rect = big_paper.get_rect()
    big_rock_rect = big_rock.get_rect()
    big_scissors_rect = big_scissors.get_rect()
    big_paper_rect.center = (WIDTH//2, HEIGHT-165)
    big_rock_rect.center = (WIDTH//2, HEIGHT-165)
    big_scissors_rect.center = (WIDTH//2, HEIGHT-165)
    if choice == "бумага":
        screen.blit(big_paper, big_paper_rect)
    elif choice == "камень":
        screen.blit(big_rock, big_rock_rect)
    else:
        screen.blit(big_scissors, big_scissors_rect)

def waiting(screen):
    font1 = pygame.font.SysFont("Courier New", FZ_MID, bold=True)
    font2 = pygame.font.SysFont("Courier New", int(FZ_GAME*0.8), bold=True)
    font3 = pygame.font.SysFont("Courier New", FZ_MAIN, bold=True)
    text1 = font1.render("Камень...", True, TEXT_COLOR)
    text2 = font2.render("Ножницы...", True, TEXT_COLOR)
    text3 = font3.render("Бумага!", True, TEXT_COLOR)
    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()
    text3_rect = text3.get_rect()
    text1_rect.center = (WIDTH//2, FZ_GAME*3)
    text2_rect.center = (WIDTH//2, FZ_GAME*5)
    text3_rect.center = (WIDTH//2, FZ_GAME*7)
    screen.blit(text1, text1_rect)
    pygame.display.flip()
    pygame.time.wait(350)
    screen.blit(text2, text2_rect)
    pygame.display.flip()
    pygame.time.wait(350)
    screen.blit(text3, text3_rect)
    pygame.display.flip()
    pygame.time.wait(350)

def print_computer_choice(screen, choice, rock, paper, scissors):
    paper_rect = paper.get_rect()
    rock_rect = rock.get_rect()
    scissors_rect = scissors.get_rect()
    paper_rect.midtop = (WIDTH//2, FZ_GAME*2)
    rock_rect.midtop = (WIDTH//2, FZ_GAME*2)
    scissors_rect.midtop = (WIDTH//2, FZ_GAME*2)
    if choice == "бумага":
        screen.blit(paper, paper_rect)
    elif choice == "камень":
        screen.blit(rock, rock_rect)
    else:
        screen.blit(scissors, scissors_rect)

def print_round_winner(screen, round_winner):
    font = pygame.font.SysFont("Courier New", FZ_GAME, bold=True)
    text = ""
    if round_winner != "undefind":
        if round_winner == "Человек":
            text = font.render("Выиграл Человек (+1)", True, TEXT_COLOR)
        elif round_winner == "Компьютер":
            text = font.render("Выиграл Компьютер (+1)", True, TEXT_COLOR)
        elif round_winner == "Ничья":
            text = font.render("Ничья! (0)", True, TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH//2, HEIGHT//2+FZ_GAME)
        screen.blit(text, text_rect)

def print_winner(screen, winner, computer_lose, human_lose, human_score, computer_score):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont("Courier New", FZ_GAME, bold=True)
    font1 = pygame.font.SysFont("Courier New", FZ_MID, bold=True)
    next = font1.render("Через пару секунд вы автоматически перейдёте в главное меню", True, TEXT_COLOR)
    next_rect = next.get_rect()
    next_rect.midbottom = (WIDTH//2, HEIGHT-FZ_GAME)
    screen.blit(next, next_rect)
    text = ""
    text1 = ""
    computer_lose_rect = computer_lose.get_rect()
    human_lose_rect = human_lose.get_rect()
    computer_lose_rect.center = (WIDTH//2, HEIGHT//4)
    human_lose_rect.center = (WIDTH//2, HEIGHT//4)
    if winner == "Компьютер":
        text = font.render("Со счётом " + str(human_score) + ":" + str(computer_score) + " выигрывает КОМПЬЮТЕР", True, TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH//2, HEIGHT//2)
        screen.blit(human_lose, human_lose_rect)
        screen.blit(text, text_rect)
    else:
        text = font.render("Со счётом " + str(human_score) + ":" + str(computer_score) + " выигрывает ЧЕЛОВЕК", True, TEXT_COLOR)
        text1 = font.render("ПОЗДРАВЛЯЕМ!", True, TEXT_COLOR)
        text_rect = text.get_rect()
        text1_rect = text1.get_rect()
        text_rect.center = (WIDTH//2, HEIGHT//2)
        text1_rect.center = (WIDTH//2, HEIGHT//2 + HEIGHT//6)
        screen.blit(computer_lose, computer_lose_rect)
        screen.blit(text, text_rect)
        screen.blit(text1, text1_rect)

def init_new_game(game_state):
    game_state["human_score"] = 0
    game_state["human_choice"] = "undefind"
    game_state["computer_choice"] = "undefind"
    game_state["last_human_choice"] = "камень"
    game_state["last_computer_choice"] = "камень"
    game_state["round_winner"] = "undefind"
    game_state["winner"] = "undefind"
    game_state["computer_score"] = 0
    game_state["dificulty"] = "undefind"
    game_state["game_paused"] = False
    game_state["choice_dificulty"] = True
    game_state["rounds"] = 1
    game_state["coord_x"] = [WIDTH//2-int(FZ_CHOICE*9.5), WIDTH//2-int(FZ_CHOICE*5.5), 
                    WIDTH//2-int(FZ_CHOICE*2.5), WIDTH//2+FZ_CHOICE*2,
                    WIDTH//2+int(FZ_CHOICE*5.5), WIDTH//2+FZ_CHOICE*10]
    game_state["coord_y"] = [HEIGHT-TAB_Y*8-FZ_CHOICE, HEIGHT-TAB_Y*8,
                    HEIGHT-TAB_Y*8-FZ_CHOICE, HEIGHT-TAB_Y*8,
                    HEIGHT-TAB_Y*8-FZ_CHOICE, HEIGHT-TAB_Y*8]

def cleaning(screen, human_score, computer_score, human_icon, computer_icon, rounds, game_state, big_paper, big_rock, big_scissors):
    screen.fill(BACKGROUND_COLOR)
    print_scores(screen, human_score, computer_score, human_icon, computer_icon)
    print_rounds(screen, rounds)
    print_particular_choice(screen, big_paper, big_rock, big_scissors, game_state["human_choice"])
    pygame.display.flip()

def close_game():
    pygame.quit()
    sys.exit()

main()