"""
    BreakOut Game
    Use the paddle to destroy all bricks on the screen

    By: Nick Colonna
"""
import pygame
import random

display_w = 400     
display_h = 600     
ball_size = 10
ball_move = 5
paddle_w = ball_size * 7
paddle_h = 12
paddle_move = 10
brick_w = ball_size * 5
brick_h = 15
speed = 30
black = (0,0,0)
white = (255,255,255)
grey = (160,160,160)
blue = (51,153,255)
green = (153,255,51)
red = (255,51,51)
yellow = (255,255,51)
cyan = (102,255,255)
brick_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

pygame.init()
display = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption("BreakOut by Nick Colonna")
pygame.display.update()
display.fill(black)
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("comicsansms", 20)
play_again_message = font_style.render("Press Q to Quit or SPACE to Play Again", True, cyan)


"""
Class is derived from the Sprite class from pygame
This class is used to create objects for the ball, paddle, and bricks.
"""
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])    #creates a surface to draw sprite
        self.image.fill(white)

        pygame.draw.rect(self.image, color, [0,0, width, height])   #all objects in this game are rectangles

        self.rect = self.image.get_rect()   # links surface to rectangle object

"""
Function to help create all the bricks
"""
def create_bricks():
    num_bricks = display_w // (brick_w + 10)    # bricks that can fit in one row
    
    for row in range(0, 5):   # 5 rows of bricks
        x = 15  #x coordinate of brick
        count = 0
        colors = [blue, red, green]
        while count < num_bricks:
            x += 10
            brick = Block(colors[(count+row) % 3], brick_w, brick_h)   #create brick
            brick.rect.x = x
            brick.rect.y = 30 + brick_h*row + 15*row   # top space + (height of brick * row number) + (spacing * row number)
            brick_list.add(brick)
            all_sprites.add(brick)
            x += brick_w
            count += 1

"""
Score keeping function to display score on screen
""" 
def get_score(score):
    score_message = font_style.render("Score: {}".format(score), True, white)
    display.blit(score_message, [5 , 1])


"""
Main game function containing game loop

The core functionality of the game is run here
"""
def play_game():
    game_over = False
    game_end = False
    outcome = False
    reset = False
    begin_game = True
    paddle_x = display_w/2 - paddle_w/2
    ball_x = display_w/2 - ball_size/2
    ball_y = display_h - ball_size*5
    ball_dx = random.choice([random.randint(-ball_move, -1), random.randint(1, ball_move)])
    ball_dy = -ball_move
    score = 0
    num_lives = 2


    # create the user paddle
    paddle = Block(grey, paddle_w, paddle_h)
    paddle.rect.x = display_w/2 - paddle_w/2
    paddle.rect.y = display_h - ball_size*4
    all_sprites.add(paddle)

    # create the ball
    ball = Block(white, ball_size, ball_size)
    ball.rect.x = display_w/2 - ball_size/2
    ball.rect.y = display_h - ball_size*5
    all_sprites.add(ball)

    # create bricks
    create_bricks()

    # Game Loop
    while game_over == False:
        # Loser loop runs when user runs out of lives
        while game_end == True:
            display.fill(black)
            get_score(score)
            if outcome == True:
                outcome_message = font_style.render("WINNER!", True, green)
            else:
                outcome_message = font_style.render("LOSER!", True, red)
            display.blit(outcome_message, [160, display_h / 2 - 25])
            display.blit(play_again_message, [15, display_h / 2])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # exit game if 'X' at top of window is clicked
                    game_over = True
                    game_end = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: # quit game if Q pressed
                        game_over = True
                        game_end = False
                    elif event.key == pygame.K_SPACE: # restart game is Space pressed
                        brick_list.empty()
                        all_sprites.empty()
                        play_game()

        # exit game if 'X' at top of window is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                game_over = True

        # move to next iteration of loop if game is now over
        if game_over:
            continue

        # look for left or right arrow key clicks
        keys = pygame.key.get_pressed()    
        if keys[pygame.K_LEFT]:
            if paddle.rect.x - paddle_move <= paddle_move:
                paddle.rect.x = paddle_move
            else:
                paddle.rect.x += -paddle_move
        elif keys[pygame.K_RIGHT]:
            if paddle.rect.x + paddle_move >= (display_w - paddle_w - paddle_move):
                paddle.rect.x = (display_w - paddle_w - paddle_move)
            else:
                paddle.rect.x += paddle_move

                
        # check if ball hit any bricks hit
        bricks_hit = pygame.sprite.spritecollide(ball, brick_list, True)
        if bricks_hit != []:
            ball_dy *= -1
            score += len(bricks_hit)

        # if brick list is empty, player is a winner!
        if len(brick_list) == 0:
            game_end = True
            outcome = True

        # check if ball hit paddle
        paddle_hit = pygame.sprite.collide_rect(ball, paddle)
        if paddle_hit == True:
            ball_dy *= -1

        # check if ball hits display boundaries
        if ball.rect.x + ball_dx <= 0:
            ball_dx *= -1
        elif ball.rect.x + ball_dx >= (display_w - ball_size):
            ball_dx *= -1
        if ball.rect.y + ball_dy <= 0:
            ball_dy *= -1
        elif ball.rect.y + ball_dy >= (display_h - ball_size):
            num_lives -= 1
            if num_lives == 0:  # game over if no lives left
                game_end = True
                outcome = False
            else:       # restart ball and paddle if still have lives remaining
                ball.rect.x = display_w/2 - ball_size/2
                ball.rect.y = display_h - ball_size*5
                paddle.rect.x = display_w/2 - paddle_w/2
                paddle.rect.y = display_h - ball_size*4
                ball_dx = random.choice([random.randint(-ball_move, -1), random.randint(1, ball_move)])
                ball_dy = -ball_move
                reset = True

        # don't move balls if first starting game or is beginning new life
        if not reset and not begin_game:
            ball.rect.x += ball_dx
            ball.rect.y += ball_dy

        all_sprites.draw(display)

        get_score(score)
        pygame.display.update()
        display.fill(black)
        clock.tick(speed)
        
        if reset == True:
            pygame.time.wait(1000)
            reset = False
        if begin_game == True:
            pygame.time.wait(1500)
            begin_game = False

    #quit out of pygame when game over
    pygame.display.quit()
    pygame.quit()

play_game()