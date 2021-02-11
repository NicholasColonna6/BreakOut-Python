"""
	BreakOut Game
	Use the paddle to destroy all bricks on the screen

	By: Nick Colonna
"""
import pygame
import random

display_w = 400		#width of game screen display
display_h = 600		#height of game screen display
ball_size = 10		#dimension of ball
paddle_w = ball_size * 7
paddle_h = 12
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
Main Game Loop

The core functionality of the game is run here
"""
def play_game():
	game_over = False
	paddle_x = display_w/2 - paddle_w/2
	ball_x = display_w/2 - ball_size/2
	ball_y = display_h - ball_size*5
	ball_dx = 0
	ball_dy = 0

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

	create_bricks()

	while game_over == False:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:	# exit game if 'X' at top of window is clicked
				game_over = True
			elif event.type == pygame.KEYDOWN:	# look for left or right arrow key clicks
				if event.key == pygame.K_LEFT:
					paddle.rect.x += -10
				elif event.key == pygame.K_RIGHT:
					paddle.rect.x += 10


		ball_x += ball_dx
		ball_y += ball_dy

		all_sprites.draw(display)

		pygame.display.update()
		display.fill(black)
		clock.tick(speed)


play_game()