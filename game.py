import pygame
# For fps
import time
# For RNG
import random

#Initialize and set caption
pygame.init()

#GLobal variables for screen size
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
CAR_WIDTH = 55

#Misc config
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Pod racing")

#Global colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_ARRAY = [COLOR_BLACK, COLOR_RED, COLOR_BLUE, COLOR_GREEN]

# Link to Roboto file
Roboto = "Roboto/Roboto-Medium.ttf"

#Game clock
clock = pygame.time.Clock()

#Car image
carImage = pygame.image.load('car.png')

# Displays car
def car(x, y):
	gameDisplay.blit(carImage, (x, y))

# Creates text object
# @param: pygame loaded font file, message
# @return: Text surface, outer boundary of surface
def text_objects(text, font):
	textSurface = font.render(text, True, COLOR_BLACK)
	return textSurface, textSurface.get_rect()

# Displays message
# Wraps text_objects function and updates display
def display_msg(text):
	centerText = pygame.font.Font(Roboto, 40)
	textSurface, textRectangle = text_objects(text, centerText)
	textRectangle.center = ((DISPLAY_WIDTH/2), (DISPLAY_HEIGHT/2))
	gameDisplay.blit(textSurface, textRectangle)

	pygame.display.update()

	time.sleep(2)

	game_loop()

# Draws obstacle at random x/y coordinate
# @param:
# Obstacle x, y coordinates, width, height, 
def draw_obstacles(obs_x, obs_y, obs_width, obs_height, color):
	pygame.draw.rect(gameDisplay, color, [obs_x, obs_y, obs_width, obs_height])

# Display game stats
# @param:
# Stat to display, count of stat, position to display at
def game_stats(message, count, position):
	font = pygame.font.Font(Roboto, 25)
	counter = font.render(message + str(count), True, COLOR_BLACK)
	gameDisplay.blit(counter, position)

# User crash
def crash():
	display_msg("You crashed! Restarting game.")


def game_loop():
	#State of crash
	exit_game = False

	#initial car position
	car_x = 400
	car_y = 500
	x_change = 0

	#obstacle initial config
	obs_speed = 7
	obs_width = 80
	obs_height = 80
	obs_dodged = 0
	obs_init_x = random.randrange(0, DISPLAY_WIDTH - obs_width)
	# Negative initial y to give user time to adjust
	obs_init_y = -400
	obs_color = COLOR_ARRAY[random.randint(0, 3)]

	level = 0

	#Main game loop
	while not exit_game: 

		for event in pygame.event.get():
			# User quit
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			# Left or right
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_change = -8
				if event.key == pygame.K_RIGHT:
					x_change = 8

			#Stop pressing left or right
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					x_change = 0

		car_x = car_x + x_change
		gameDisplay.fill(COLOR_WHITE)

		draw_obstacles(obs_init_x, obs_init_y, obs_width, obs_height, obs_color)
		obs_init_y += obs_speed
		car(car_x, car_y)
		game_stats("Dodged: ", obs_dodged, (10, 10))
		game_stats("Level: ", level, (700, 10))

		if car_x > DISPLAY_WIDTH - CAR_WIDTH or car_x < 0:
			crash()

		# Make objects appear after they go off screen
		if obs_init_y > DISPLAY_HEIGHT:
			obs_init_y = 0 - obs_height
			obs_init_x = random.randrange(0, DISPLAY_WIDTH)
			obs_dodged += 1
			obs_color = COLOR_ARRAY[random.randint(0, 3)]
			if obs_dodged % 3 == 0:
				obs_speed += 2.5
				level += 1

		# Logic to handle box-car crashes
		if car_y < obs_init_y + obs_height:
			if car_x + CAR_WIDTH > obs_init_x and car_x + CAR_WIDTH < obs_init_x + obs_width or car_x > obs_init_x and car_x < obs_init_x + obs_width:
				crash()

		pygame.display.flip() 
		clock.tick(30)

game_loop()
pygame.quit()
quit()