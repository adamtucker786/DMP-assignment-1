import pygame
pygame.init()

# create constants for screen setup
SCREENWIDTH = 1000
SCREENHEIGHT = 500
SCREENCAPTION = "asssignment 1 DMP"
SCREENICON = pygame.image.load("assets\RandomLogo.jpg")

WHITE = 255, 255, 255

#creating display with a caption and icon using function from pygame libary
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption(SCREENCAPTION)
pygame.display.set_icon(SCREENICON)



# function to activate the menu
def DisplayMenu():
  screen.fill(WHITE)

global Current_Page 
Current_Page = "Menu"
# mainloop with running condition to end game
Running = True
while Running:
  # code to detect pygame event
  for event in pygame.event.get():
    # if pygame window x pressed then end the program
    if event.type == pygame.QUIT:
      Running = False

  match Current_Page:
    case "Menu":
      DisplayMenu()
    case _:
      DisplayMenu()
      pass

  pygame.display.update()