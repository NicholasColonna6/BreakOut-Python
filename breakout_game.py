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
grey = (150,150,150)
blue = (0,0,255)
red = (250,0,0)
brick_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

pygame.init()
display = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption("BreakOut by Nick Colonna")
pygame.display.update()
display.fill(black)
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("comicsansms", 20)

class Block(pygame.sprite.Sprite):
	def __init__(self, color, width, height):
		super().__init__()

		self.image = pygame.Surface([width, height])
		self.image.fill(white)
		self.image.set_colorkey(white)

		pygame.draw.rect(self.image, color, [0,0, width, height])

		self.rect = self.image.get_rect()

"""
Function to help create all the bricks to start the game
"""
def create_bricks():
	# we need to draw all the bricks here
	# we need to store the dimensions of the bricks in some sort of data structure to enable checking if collide
	

	#THIS IS A VERY NAIVE WAY TO DISPLAY THE BLOCKS, NEEDS IMPOVEMENT
	num_bricks = display_w // (brick_w + 10)

	for j in range(0, 5):
		i = 15
		count = 0
		while count < num_bricks:
			i += 10
			brick = Block(blue, brick_w, brick_h)
			brick.rect.x = i
			brick.rect.y = 30 + brick_h*j + 15*j
			brick_list.add(brick)
			all_sprites.add(brick)
			#pygame.draw.rect(display, blue, (i, 30+brick_h*j+15*j, brick_w, brick_h))
			i += brick_w
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
	paddle_x = display_w/2 - paddle_w/2
	ball_x = display_w/2 - ball_size/2
	ball_y = display_h - ball_size*5
	ball_dx = random.choice([random.randint(-ball_move, -1), random.randint(1, ball_move)])
	ball_dy = -ball_move
	score = 0

	#create the user paddle
	paddle = Block(grey, paddle_w, paddle_h)
	paddle.rect.x = display_w/2 - paddle_w/2
	paddle.rect.y = display_h - ball_size*4
	all_sprites.add(paddle)

	#create the ball
	ball = Block(red, ball_size, ball_size)
	ball.rect.x = display_w/2 - ball_size/2
	ball.rect.y = display_h - ball_size*5
	all_sprites.add(ball)

	#create bricks
	create_bricks()

	# Game Loop
	while game_over == False:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:	# exit game if 'X' at top of window is clicked
				game_over = True
			elif event.type == pygame.KEYDOWN:	# look for left or right arrow key clicks
				if event.key == pygame.K_LEFT:
					if paddle.rect.x - paddle_move <= 0:
						paddle.rect.x = 0
					else:
						paddle.rect.x += -paddle_move
				elif event.key == pygame.K_RIGHT:
					if paddle.rect.x + paddle_move >= (display_w - paddle_w):
						paddle.rect.x = (display_w - paddle_w)
					else:
						paddle.rect.x += paddle_move

		# check if ball hit any bricks hit
		bricks_hit = pygame.sprite.spritecollide(ball, brick_list, True)
		if bricks_hit != []:
			ball_dy *= -1
			score += len(bricks_hit)

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
		
		ball.rect.x += ball_dx
		ball.rect.y += ball_dy

		all_sprites.draw(display)


		get_score(score)
		pygame.display.update()
		display.fill(black)
		clock.tick(speed)


play_game()