import pygame
import random
import sys


# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Sound
plob_sound = pygame.mixer.Sound("pong.ogg")
plob_sound.set_volume(0.5)
score_sound = pygame.mixer.Sound("score.ogg")
score_sound.set_volume(0.5)
menu_sfx = pygame.mixer.Sound("menu_sfx.mp3")

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')
icon = pygame.image.load("Pong.png")
pygame.display.set_icon(icon)

# Colors
light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')

# Text Font
big_font = pygame.font.Font("freesansbold.ttf", 100)
option_font = pygame.font.Font("freesansbold.ttf", 60)
end_font = pygame.font.Font("freesansbold.ttf", 50)
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# Windows
menu = True
game = False


# --------------------------------------------------------------------------------------------------------------------
def display_page(Page):
    title = big_font.render(f'PONG GAME', True, light_grey)
    title_pos = title.get_rect(center=(screen_width / 2, screen_height / 5))
    screen.blit(title, title_pos)

    if Page == 1:
        option_play = option_font.render(f'Play', True, light_grey)
        option_sound = option_font.render(f'Sound', True, light_grey)
        option_exit = option_font.render(f'Exit', True, light_grey)
    else:
        option_play = option_font.render(f'Normal', True, light_grey)
        option_sound = option_font.render(f'Hard', True, light_grey)
        option_exit = option_font.render(f'Back', True, light_grey)

    option_play_pos = option_play.get_rect(center=(screen_width / 2, screen_height / 3 + 100))
    option_sound_pos = option_sound.get_rect(center=(screen_width / 2, screen_height / 3 + 250))
    option_exit_pos = option_exit.get_rect(center=(screen_width / 2, screen_height / 3 + 400))
    screen.blit(option_play, option_play_pos)
    screen.blit(option_sound, option_sound_pos)
    screen.blit(option_exit, option_exit_pos)


# Variables
selected = 0
sound = True
page = 1
game_mode = 1


# --------------------------------------------------------------------------------------------------------------------
def play_sound(sound_name):
    if sound:
        sound_name.play()


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if (ball.top <= 0 and ball_speed_y < 0) or (ball.bottom >= screen_height and ball_speed_y > 0):
        play_sound(plob_sound)
        ball_speed_y *= -1

    # Player Score
    if ball.left <= 0:
        play_sound(score_sound)
        score_time = pygame.time.get_ticks()
        player_score += 1

    # Opponent Score
    if ball.right >= screen_width:
        play_sound(score_sound)
        score_time = pygame.time.get_ticks()
        opponent_score += 1

    if ball.colliderect(player) and ball_speed_x > 0:
        play_sound(plob_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
            ball_speed_y = random.randint(2, 8) * random.choice((1, -1))
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y = random.randint(2, 8) * random.choice((1, -1))
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y = random.randint(2, 8) * random.choice((1, -1))

    if ball.colliderect(opponent) and ball_speed_x < 0:
        play_sound(plob_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
            ball_speed_y = random.randint(2, 8) * random.choice((1, -1))
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y = random.randint(2, 8) * random.choice((1, -1))
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y = random.randint(2, 8) * random.choice((1, -1))


def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai():
    if opponent.top + 50 < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom - 50 > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_start():
    global ball_speed_x, ball_speed_y, score_time

    ball.center = (screen_width / 2, screen_height / 2)
    current_time = pygame.time.get_ticks()

    if current_time - score_time < 700:
        number_three = basic_font.render("3", True, light_grey)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = basic_font.render("2", True, light_grey)
        screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = basic_font.render("1", True, light_grey)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_y, ball_speed_x = 0, 0
    else:
        ball_speed_x = ball_speed * random.choice((1, -1))
        ball_speed_y = random.randint(2, 8) * random.choice((1, -1))
        score_time = 0


def win_lose():
    global ball_speed_x, ball_speed_y, game_end
    ball_speed_x = 0
    ball_speed_y = 0
    ball.center = (screen_width / 2, screen_height / 2)
    game_end = True

    if player_score >= winning_score:
        win_text = end_font.render(f"You Win!", True, light_grey)
        text_rect = win_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(win_text, text_rect)

    elif opponent_score >= winning_score:
        lose_text = end_font.render(f"You Lose...", True, light_grey)
        text_rect = lose_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(lose_text, text_rect)

    close_game_text = end_font.render(f"Press Enter To Return To Menu.", True, light_grey)
    close_game_text_rect = close_game_text.get_rect(center=(screen_width / 2, screen_height / 2 + 70))
    screen.blit(close_game_text, close_game_text_rect)


# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Game Variables
ball_speed = 8
ball_speed_x = ball_speed * random.choice((1, -1))
ball_speed_y = random.randint(2, 8) * random.choice((1, -1))
player_speed = 0
opponent_speed = 6
score_time = 0
game_end = False
player_score = 0
opponent_score = 0
winning_score = 2


# --------------------------------------------------------------------------------------------------------------------
while True:

    # Render Main Menu
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and selected < 2:
                    selected += 1
                    play_sound(menu_sfx)
                    print(selected)
                if event.key == pygame.K_UP and selected > 0:
                    selected -= 1
                    play_sound(menu_sfx)
                    print(selected)
                if event.key == pygame.K_RETURN:
                    if page == 1:
                        if selected == 0:
                            page = 2
                        if selected == 1:
                            if sound:
                                sound = False
                            else:
                                sound = True
                            print(sound)
                        if selected == 2:
                            pygame.quit()
                            sys.exit()
                    else:
                        if selected == 0:
                            menu = False
                            game = True
                            opponent_speed = 5
                            ball_speed = 8
                        if selected == 1:
                            menu = False
                            game = True
                            opponent_speed = 7
                            ball_speed = 10
                        if selected == 2:
                            page = 1
                    play_sound(menu_sfx)

        screen.fill(bg_color)
        display_page(page)
        pygame.draw.line(screen, light_grey, (screen_width / 2 - 50, screen_height / 3 + 150*(selected + 1)),
                         (screen_width / 2 + 50, screen_height / 3 + 150*(selected + 1)), 5)
        if not sound and page == 1:
            pygame.draw.line(screen, light_grey, (screen_width / 2 - 100, screen_height / 3 + 250),
                                                 (screen_width / 2 + 100, screen_height / 3 + 250), 5)
        pygame.display.flip()
        clock.tick(60)

    # Render Game
    if game:
        page = 1
        game_end = False
        score_time = pygame.time.get_ticks()
        player_score = 0
        opponent_score = 0
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_speed -= 7
                if event.key == pygame.K_DOWN:
                    player_speed += 7
                if (event.key == pygame.K_RETURN and game_end) or event.key == pygame.K_ESCAPE:
                    menu = True
                    game = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_speed += 7
                if event.key == pygame.K_DOWN:
                    player_speed -= 7

        # Game Logic
        ball_animation()
        player_animation()
        opponent_ai()

        # Visuals
        screen.fill(bg_color)
        if player_score < winning_score and opponent_score < winning_score:
            pygame.draw.rect(screen, light_grey, player)
            pygame.draw.rect(screen, light_grey, opponent)
            pygame.draw.ellipse(screen, light_grey, ball)
            pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

            if score_time:
                ball_start()

            player_text = basic_font.render(f'{player_score}', True, light_grey)
            screen.blit(player_text, (660, 470))

            opponent_text = basic_font.render(f'{opponent_score}', True, light_grey)
            screen.blit(opponent_text, (600, 470))
        else:
            win_lose()

        pygame.display.flip()
        clock.tick(60)
