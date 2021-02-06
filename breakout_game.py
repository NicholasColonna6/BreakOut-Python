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

pygame.init()
d = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption("BreakOut by Nick Colonna")
pygame.display.update()
d.fill((0,0,0))
clock = pygame.time.Clock()


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
			pygame.draw.rect(d, (0,0,250), (i, 30+brick_h*j+15*j, brick_w, brick_h))
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

	while game_over == False:

		for event in pygame.event.get():
			# end game if 'X' at top of window is clicked
			if event.type == pygame.QUIT:
				game_over = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					paddle_x += -10
				elif event.key == pygame.K_RIGHT:
					paddle_x += 10


		ball_x += ball_dx
		ball_y += ball_dy
		pygame.draw.rect(d, (150,150,150), (paddle_x, display_h - ball_size*4, paddle_w, paddle_h))		#draw paddle
		pygame.draw.rect(d, (250,0,0), (ball_x, ball_y, ball_size, ball_size))	#draw ball

		create_bricks()	

		pygame.display.update()
		d.fill((0,0,0))
		clock.tick(speed)

play_game()