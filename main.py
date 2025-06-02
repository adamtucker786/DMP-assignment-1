import pygame
pygame.init()


# create constants for Screen setup
SCREENWIDTH = 1000
SCREENHEIGHT = 500
SCREENCAPTION = "asssignment 1 DMP"
SCREENICON = pygame.image.load("assets\RandomLogo.jpg")

# colours
WHITE = 255, 255, 255
BLACK = 0,0,0

# fonts
BUTTON_FONT = pygame.font.SysFont("comicsansms", 40)

#creating display with a caption and icon using function from pygame libary
Screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption(SCREENCAPTION)
pygame.display.set_icon(SCREENICON)


clock = pygame.time.Clock()

class Timer:
  def __init__(self, StartMinutes, StartSeconds):
    self.Minutes = StartMinutes
    self.Seconds = StartSeconds
    self.StartMinutes = StartMinutes

  def Reset(self):
    self.Minutes = self.StartMinutes
    self.Seconds = self.StartSeconds

  def decrement(self):
    self.Seconds -= 1
    if self.Seconds < 0:
      self.Seconds = 59
      self.Minutes -= 1

  def isFinished(self):
    if self.Minutes < 0 and self.Seconds < 0:
      return True
    else:
      return False


EMPTY_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load("assets\Button.png"), (400, 75))
# class for buttons which takes inputs for the images and text to display and displays the text in that Image
# also takes coordinate position to display the buttons at
class Buttons:
  def __init__(self, Image, text, x_pos, y_pos):
    self.costume_index = 0
    self.Image = Image
    self.x_pos = x_pos
    self.y_pos = y_pos
    # command will create a set of coordinates that correspond to the size and location of the Image and text
    self.rect = self.Image.get_rect(center=(self.x_pos, self.y_pos))
    self.text = text
    self.button_text = BUTTON_FONT.render(self.text, True, (0,0,0))
    self.text_rect = self.button_text.get_rect(center=(self.x_pos, self.y_pos))

  # this method of the class will display the object to the Screen at the given Screen position
  def draw_button(self):
    Screen.blit(self.Image, self.rect)
    Screen.blit(self.button_text, self.text_rect)

  def isPressed(self, event):
    pass    



# function to display text on the Screen
def AddText(text, position, size, colour):
  Font = pygame.font.Font(None, size)
  AddedText = Font.render(text, True, colour)
  Screen.blit(AddedText, position)


POMODORO_BUTTON = Buttons(EMPTY_BUTTON_IMAGE, "Pomodoro Timer", 220, 200)
CUSTOM_BUTTON = Buttons(EMPTY_BUTTON_IMAGE, "Custom Timer", 220, 300)
# function to activate the menu
def MenuScreen():
  Screen.fill(WHITE)
  POMODORO_BUTTON.draw_button()
  CUSTOM_BUTTON.draw_button()
  AddText("study timer assistant", (400, 50), 60, BLACK)


PomdoroTimer = Timer(25, 0)
def TimerScreen():
  Screen.fill(WHITE)
  AddText("Study time", (300, 50), 60, BLACK)
  AddText(f"{PomdoroTimer.Minutes}:{PomdoroTimer.Seconds}", (400, 200), 60, BLACK)


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
    if event.type == pygame.MOUSEBUTTONDOWN:
      if (POMODORO_BUTTON.rect.collidepoint(event.pos)) & (Current_Page == "Menu"):
        Current_Page = "Timer"


  match Current_Page:
    case "Menu":
      MenuScreen()
    case "Timer":
      TimerScreen()
      PomdoroTimer.decrement()
      if PomdoroTimer.isFinished():
        Current_Page = "Menu"
      clock.tick(1)
    case _:
      MenuScreen()

  pygame.display.update()