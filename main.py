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

FPS = 60
clock = pygame.time.Clock()


class Timer:
  def __init__(self, StartMinutes, StartSeconds):
    self.Minutes = StartMinutes
    self.Seconds = StartSeconds
    self.StartMinutes = StartMinutes
    self.StartSeconds = StartSeconds
    self.Speed = 1

  def Reset(self):
    self.Minutes = self.StartMinutes
    self.Seconds = self.StartSeconds

  def decrement(self):
    self.Seconds -= self.Speed/FPS
    if self.Seconds < 0:
      self.Seconds = 59
      self.Minutes -= 1

  def display(self):
    AddText(f"{int(self.Minutes)}:{int(self.Seconds)}", (400, 200), 80, BLACK)

  def pause(self):
    self.Speed = 0
  
  def resume(self):
    self.Speed = 1

  def isFinished(self):
    if self.Minutes < 0:
      return True
    else:
      return False


class customTimer(Timer):
  def __init__(self, StartMinutes, StartSeconds):
    super().__init__(StartMinutes, StartSeconds)

  def increaseMinutes(self):
    self.Minutes += 1

  def decreaseMinutes(self):
    self.Minutes -= 1

  def increaseSeconds(self):
    self.Seconds += 1

  def decreaseSeconds(self):
    self.Seconds -= 1

  


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

  def isPressed(self)-> bool:
    pressed = False
    if self.rect.collidepoint(event.pos):
      pressed = True
    return pressed
  
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


PAUSE_BUTTON = Buttons(EMPTY_BUTTON_IMAGE, "Pause Timer", 200, 400)
RESUME_BUTTON = Buttons(EMPTY_BUTTON_IMAGE, "Resume Timer", 600, 400)
PomdoroTimer = Timer(0, 10)
def TimerScreen():
  Screen.fill(WHITE)
  AddText("Study time", (300, 50), 60, BLACK)
  PomdoroTimer.display()
  PAUSE_BUTTON.draw_button()
  RESUME_BUTTON.draw_button()


INCREASE_ARROW_iMAGE = pygame.transform.scale(pygame.image.load("assets\_UpArrowImage.png"), (50, 50))
DECREASE_ARROW_iMAGE = pygame.transform.scale(pygame.image.load("assets\_DownArrowImage.png"), (50, 50))
MINUTE_INCREASE_BUTTON = Buttons(INCREASE_ARROW_iMAGE, "", 50, 200)
SECOND_INCREASE_BUTTON = Buttons(INCREASE_ARROW_iMAGE, "", 950, 200)
MINUTE_DECREASE_BUTTON = Buttons(DECREASE_ARROW_iMAGE, "", 50, 250) 
SECOND_DECREASE_BUTTON = Buttons(DECREASE_ARROW_iMAGE, "", 950, 250)
START_CUSTOM_BUTTON = Buttons(pygame.transform.scale(pygame.image.load("assets\Button.png"), (450, 50)), "start Custom Timer", SCREENWIDTH/2, SCREENHEIGHT*0.8)
CustomTimer = customTimer(0, 0)
def CustomTimerCreation():
  Screen.fill(WHITE)
  AddText("Create Custom Timer", (200, 50), 60, BLACK)
  CustomTimer.display()
  MINUTE_INCREASE_BUTTON.draw_button()
  SECOND_INCREASE_BUTTON.draw_button()
  MINUTE_DECREASE_BUTTON.draw_button()
  SECOND_DECREASE_BUTTON.draw_button()
  START_CUSTOM_BUTTON.draw_button()



def CustomTimerCount():
  Screen.fill(WHITE)
  AddText("Study time", (300, 50), 60, BLACK)
  CustomTimer.display()
  PAUSE_BUTTON.draw_button()
  RESUME_BUTTON.draw_button()
  


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
      if (POMODORO_BUTTON.isPressed()) & (Current_Page == "Menu"):
        Current_Page = "Timer"
      if (CUSTOM_BUTTON.isPressed()) & (Current_Page == "Menu"):
        Current_Page = "CustomTimerCreation"
      if (RESUME_BUTTON.isPressed()) & (Current_Page == "Timer"):
        PomdoroTimer.resume()
      if (PAUSE_BUTTON.isPressed()) & (Current_Page == "Timer"):
        PomdoroTimer.pause()
      if (RESUME_BUTTON.isPressed()) & (Current_Page == "CustomTimerCount"):
        CustomTimer.resume()
      if (PAUSE_BUTTON.isPressed()) & (Current_Page == "CustomTimerCount"):
        CustomTimer.pause()
      if (MINUTE_INCREASE_BUTTON.isPressed()) & (Current_Page == "CustomTimerCreation"):
        CustomTimer.increaseMinutes()
      if (SECOND_INCREASE_BUTTON.isPressed()) & (Current_Page == "CustomTimerCreation"):
        CustomTimer.increaseSeconds()
      if (MINUTE_DECREASE_BUTTON.isPressed()) & (Current_Page == "CustomTimerCreation"):
        CustomTimer.decreaseMinutes()
      if (SECOND_DECREASE_BUTTON.isPressed()) & (Current_Page == "CustomTimerCreation"):
        CustomTimer.decreaseSeconds()
      if (START_CUSTOM_BUTTON.isPressed()) & (Current_Page == "CustomTimerCreation"):
        Current_Page = "CustomTimerCount"


  match Current_Page:
    case "Menu":
      MenuScreen()

    case "Timer":
      TimerScreen()
      PomdoroTimer.decrement()
      if (PomdoroTimer.isFinished()== True) :
        Current_Page = "Menu"
        PomdoroTimer.Reset()

    case "CustomTimerCreation":
      CustomTimerCreation()

    case "CustomTimerCount":
      CustomTimerCount()
      CustomTimer.decrement()
      if (CustomTimer.isFinished()== True) :
        Current_Page = "Menu"
        CustomTimer.Reset()

    case _:
      MenuScreen()

  clock.tick(FPS)
  pygame.display.update()