#importing and initialising relevant libaries
import pygame
pygame.init()
import pandas as pd

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
# applying the screen setup already set variables
pygame.display.set_caption(SCREENCAPTION)
pygame.display.set_icon(SCREENICON)


# initialising the pygame clock to control the speed the system runs which allows for acurate timer speed
FPS = 60
clock = pygame.time.Clock()


# class for the timer system 
class Timer:
  # initialiing an instance of the class requires the start length in mins and seconds
  def __init__(self, StartMinutes, StartSeconds):
    self.Minutes = StartMinutes
    self.Seconds = StartSeconds
    self.StartMinutes = StartMinutes
    self.StartSeconds = StartSeconds
    # making use of a speed variable meaning i can speed up the timer if wanted
    self.Speed = 1

  # reset method causes timer to return to its start length
  def Reset(self):
    self.Minutes = self.StartMinutes
    self.Seconds = self.StartSeconds

  # method for counting down through the timer
  def decrement(self):
    # counting down by one fraction of the timer speed every frame so the clock is at the right speed
    self.Seconds -= self.Speed/FPS
    # decreasing the minutes when the seconds reach zero so that the minute goes down and the second goes back to 59
    if self.Seconds < 0:
      self.Seconds = 59
      self.Minutes -= 1

  # method to display the timer to the middle of the screen using my add text method
  def display(self):
    # casting the values to an int so only whole nmbers are displayed on the screen as in reality the timer counts to fraction of a second accuracy
    AddText(f"{int(self.Minutes)}:{int(self.Seconds)}", (425, 200), 80, BLACK)

  # method to pause the timer by setting the speed to zero as this means each frame zero is taken from the seconds so timer stays same
  def pause(self):
    self.Speed = 0
  
  # methpd to retun speed to 1 so that the timer returns to counting down by one every second
  def resume(self):
    self.Speed = 1
  
  # checking if the timer is finished and returning true is it has and false if it isnt finished
  def isFinished(self)-> bool:
    finished = False
    # if the minutes and seconds are both less than zero then timer is finished so set value to return as True
    if (self.Minutes < 0):
      finished = True
    else:
      finished = False
    return finished


# creating a class for custim timers holding methods not used by the base pomodoro timer
# class inherits from the timer class which acts as a super class so that customTimer inherits its methods and attributes
class customTimer(Timer):
  def __init__(self, StartMinutes, StartSeconds):
    super().__init__(StartMinutes, StartSeconds)

  # functions used in creation of the custom timer to set its length
  def increaseMinutes(self):
    self.Minutes += 1
  
  def decreaseMinutes(self):
    self.Minutes -= 1
    # checking if the user has set the minutes count bellow zero and restoring it to zero to make impossible to have -ve time
    if self.Minutes < 0:
      self.Minutes = 0

  def increaseSeconds(self):
    self.Seconds += 1
    # creating a max of 59 in the seconds section and making the counter return to zero if the user goes over for faster time selection
    if self.Seconds >= 60:
      self.Seconds = 0

  def decreaseSeconds(self):
    self.Seconds -= 1
    # setting the seconds to 59 if the user tries to go bellow zero seconds to remove error of -ve time and for faster time selection
    if self.Seconds < 0:
      self.Seconds = 59

  
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

  # method checking is the button has been clicked
  def isPressed(self)-> bool:
    # creating a boolean variable to return
    pressed = False
    # using pygame collidepoint method to detect if passed in point is in collision with the objects rect
    # passing in the position of the event which is the position of the mouse click in this instance
    if self.rect.collidepoint(event.pos):
      pressed = True
    return pressed


# function to display text on the Screen
def AddText(text, position, size, colour):
  Font = pygame.font.Font(None, size)
  AddedText = Font.render(text, True, colour)
  Screen.blit(AddedText, position)


# cresting button objects for navigation to the desired timer section
POMODORO_BUTTON = Buttons(EMPTY_BUTTON_IMAGE, "Pomodoro Timer", 220, 200)
CUSTOM_BUTTON = Buttons(EMPTY_BUTTON_IMAGE, "Custom Timer", 220, 300)
# function to activate the menu
def MenuScreen():
  # blanking out the screen and creating a white background each frame to create animation
  Screen.fill(WHITE)
  #calling the draw methonds of the buttons so they display on the screen
  POMODORO_BUTTON.draw_button()
  CUSTOM_BUTTON.draw_button()
  # adding the title to the page for cosmetics with my add text function
  AddText("study timer assistant", (400, 50), 60, BLACK)
  ExcelRows = ReadExcel()
  data_start_y_pos = 150
  for row, line in enumerate(ExcelRows):
    AddText(line, (450, data_start_y_pos + row * 25), 20, BLACK)


# creating objects of the buttons class for pausing and resuming the timer
PAUSE_BUTTON = Buttons(pygame.transform.scale(EMPTY_BUTTON_IMAGE, (SCREENWIDTH/2, 75)), "Pause Timer", 250, 400)
RESUME_BUTTON = Buttons(pygame.transform.scale(EMPTY_BUTTON_IMAGE, (SCREENWIDTH/2, 75)), "Resume Timer", 750, 400)
# creating an instance of the timer class for the main pomodoro timer with initial values of 25 minutes and zero seconds
PomdoroTimer = Timer(25, 0)
def TimerScreen():
  Screen.fill(WHITE)
  # title for the page
  AddText("Study time", (350, 50), 70, BLACK)
  # displaying the timer with the class method
  PomdoroTimer.display()
  # displaying the pause and resume buttons with the class method
  PAUSE_BUTTON.draw_button()
  RESUME_BUTTON.draw_button()
  #SKIP.draw_button()


# loading arrow images for use in buttons in timer creation stage
INCREASE_ARROW_iMAGE = pygame.transform.scale(pygame.image.load("assets\_UpArrowImage.png"), (50, 50))
DECREASE_ARROW_iMAGE = pygame.transform.scale(pygame.image.load("assets\_DownArrowImage.png"), (50, 50))
# cresting increase and decrease buttons for minutes and seconds of the custom timer
MINUTE_INCREASE_BUTTON = Buttons(INCREASE_ARROW_iMAGE, "", 50, 200)
SECOND_INCREASE_BUTTON = Buttons(INCREASE_ARROW_iMAGE, "", 950, 200)
MINUTE_DECREASE_BUTTON = Buttons(DECREASE_ARROW_iMAGE, "", 50, 250) 
SECOND_DECREASE_BUTTON = Buttons(DECREASE_ARROW_iMAGE, "", 950, 250)
# button to start the timer by changing the program page to the custom timer count stage
START_CUSTOM_BUTTON = Buttons(pygame.transform.scale(pygame.image.load("assets\Button.png"), (450, 50)), "start Custom Timer", SCREENWIDTH/2, SCREENHEIGHT*0.8)
# creating the custim timer from the custom timer class (which inherits from the timer class)
CustomTimer = customTimer(0, 0)
# method to display the aspects of the timer creation screen
def CustomTimerCreation():
  Screen.fill(WHITE)
  # displaying page title
  AddText("Create Custom Timer", (200, 50), 60, BLACK)
  # dip;aying the timer using class method
  CustomTimer.display()
  # displaying the buttons using the button class method
  MINUTE_INCREASE_BUTTON.draw_button()
  SECOND_INCREASE_BUTTON.draw_button()
  MINUTE_DECREASE_BUTTON.draw_button()
  SECOND_DECREASE_BUTTON.draw_button()
  START_CUSTOM_BUTTON.draw_button()


SKIP = Buttons(EMPTY_BUTTON_IMAGE, "skip", 0, 0)
#method to display the counting cutom timer screen
def CustomTimerCount():
  Screen.fill(WHITE)
  AddText("Study time", (300, 50), 60, BLACK)
  CustomTimer.display()
  PAUSE_BUTTON.draw_button()
  RESUME_BUTTON.draw_button()
  #SKIP.draw_button()
  

BreakTimer = Timer(5,0)
def BreakTimerScreen():
  Screen.fill(WHITE)
  AddText("break time", (350, 50), 70, BLACK)
  BreakTimer.display()
  AddText("Take a break from study before continuing for better productivity", (100, 450), 30, BLACK)
  #SKIP.draw_button()


#function to read from the excel document for the details of previous study
def ReadExcel() -> list:
  # using pandas to read data from the excel sheet
  df = pd.read_excel("assets/StudyHistory.xlsx")
  # creating a new list to be able to return the excel rows
  Rows = []
  # for eachrow in the excel form
  for index, row in df.iterrows():
    #creating a string using the data in the excel row by adding the title and data item of each collumn to the string
    RowString = ', '.join([f"{col}: {row[col]}" for col in df.columns])
    # adding the new sring to the list of rows to return and dislay on the menu screen
    Rows.append(RowString)
  return Rows


#fucntion to create the display screen for the reflect stage
# creating the boxes and buttons for inputting detail;s about study completed
SUBMIT_BUTTON = Buttons(pygame.transform.scale(pygame.image.load("assets\Button.png"),(150, 80)), "submit", 900, 275)
Subject_Box = Buttons(pygame.transform.scale(pygame.image.load("assets\Button.png"),(700, 150)), "", 500, 150)
Summary_Box = Buttons(pygame.transform.scale(pygame.image.load("assets\Button.png"),(700, 150)), "", 500, 400)
def Reflect():
  Screen.fill(WHITE)
  # title fort the subject text input box
  AddText("what subject did you study?", (300, 50), 30, BLACK)
  # displaying box for text input
  Subject_Box.draw_button()
  # displaying what the user types so theycan see what they are inputting
  AddText(subject_message, (300, 100), 30, BLACK)
  AddText("write a breif summary of your study:", (300, 300), 30, BLACK)
  Summary_Box.draw_button()
  AddText(summary_message, (300, 350), 30, BLACK)
  # displaying the draw button
  SUBMIT_BUTTON.draw_button()


def WriteToExcel():
    # re laod the data so it is accessible in this function
    df = pd.read_excel("assets/StudyHistory.xlsx")
    # create new set of data for the excel line to be written
    NewRecord = {
        "Duration": StudyDuration,
        "Subject": subject_message,
        "Summary": summary_message,
        "Date": pd.Timestamp.now().strftime('%d/%m/%Y')
    }

    # Add the new entry to the DataFrame
    df = pd.concat([df, pd.DataFrame([NewRecord])], ignore_index=True)

    # writing the dataframe to the exce sheet so that the data is saved
    df.to_excel("assets/StudyHistory.xlsx", index = False)



# loading gloabal variables for easy access throughout the program
global Current_Page
global Summary_Box_active
global Subject_Box_active
global subject_message
subject_message = ""
global summary_message
summary_message = ""
Subject_Box_active = 1
Summary_Box_active = 0
Current_Page = "Menu"
global StudyDuration
StudyDuration = 0

# mainloop with running condition to end game
Running = True
while Running:
  # code to detect pygame event
  for event in pygame.event.get():
    # if pygame window x pressed then end the program
    if event.type == pygame.QUIT:
      Running = False

    # checking if mouse button has been clicked for putton press purposes
    if event.type == pygame.MOUSEBUTTONDOWN:
      # checkign for buttons clicked on the menu screen
      if (Current_Page == "Menu"):
        # check for pomodoro timer button press and call pomodoro timer screen in response
        if (POMODORO_BUTTON.isPressed()):
          Current_Page = "Timer"
        # checking for custom timer buttonbeing pressed and calling custom timer in response
        if (CUSTOM_BUTTON.isPressed()):
          Current_Page = "CustomTimerCreation"

      # checking for buttons preessed while in the timer screen
      if (Current_Page == "Timer"):
        #checking if the pause or resume buttons have been pressed by calling the is pressed method of the buttons class and calling the pause3 or resume method of timer class in response
        if (RESUME_BUTTON.isPressed()):
          PomdoroTimer.resume()
        if (PAUSE_BUTTON.isPressed()):
          PomdoroTimer.pause()
        # adding in a skip feature for demo purposes which when pressed sets the timer to only have 5 seconds left
        if (SKIP.isPressed()):
          PomdoroTimer.Minutes = 0
          PomdoroTimer.Seconds = 5

      if (Current_Page == "CustomTimerCount"):
        #checking if the pause or resume buttons have been pressed by calling the is pressed method of the buttons class and calling the pause3 or resume method of timer class in response
        if (RESUME_BUTTON.isPressed()):
          CustomTimer.resume()
        if (PAUSE_BUTTON.isPressed()):
          CustomTimer.pause()
        # adding in a skip feature for demo purposes which when pressed sets the timer to only have 5 seconds left
        if (SKIP.isPressed()):
          CustomTimer.Minutes = 0
          CustomTimer.Seconds = 5

      # adding checks for if the buttons in the timer creattion screen for a custom timer have been pressed and calling the relevant method in response
      if (Current_Page == "CustomTimerCreation"):
        if (MINUTE_INCREASE_BUTTON.isPressed()):
          CustomTimer.increaseMinutes()
        if (SECOND_INCREASE_BUTTON.isPressed()):
          CustomTimer.increaseSeconds()
        if (MINUTE_DECREASE_BUTTON.isPressed()):
          CustomTimer.decreaseMinutes()
        if (SECOND_DECREASE_BUTTON.isPressed()):
          CustomTimer.decreaseSeconds()
        if (START_CUSTOM_BUTTON.isPressed()):
          # setting the length of the break timer to be a fifth of the length of the custom timer similar to the pomodoro timer
          BreakTimer.Minutes = CustomTimer.Minutes * 0.2
          BreakTimer.Seconds = CustomTimer.Seconds * 0.2
          # setting the study duration to a five times the duration of the break timer as this isd the 
          StudyDuration = BreakTimer.Minutes*5
          # moving to the timer page to start the clock
          Current_Page = "CustomTimerCount"

      # adding in a skip feature for demo purposes which when pressed sets the timer to only have 5 seconds left
      if (SKIP.isPressed()) & (Current_Page == "BreakTimer"):
        BreakTimer.Minutes = 0
        BreakTimer.Seconds = 10

      # checking for buttons being pressed in the relection page
      if (Current_Page == "Reflect"):
        # making the pressed text input box active so the user can type in the box they click on
        if (Subject_Box.isPressed()):
          Subject_Box_active = 1
          Summary_Box_active = 0
        # making the pressed text input box active so the user can type in the box they click on
        if (Summary_Box.isPressed()):
          Subject_Box_active = 0
          Summary_Box_active = 1
        # submitting the answers the user has given buy calling the write to excel functions
        # also resetting the messages to be empty so its empty for the next time the reflect screen appears
        if (SUBMIT_BUTTON.isPressed()):
          WriteToExcel()
          subject_message = ""
          summary_message = ""
          # moving the program onto the break stage
          Current_Page = "BreakTimer"
    
    # checkign for key press input from the user
    if event.type == pygame.KEYDOWN:
      # if the subject box has been clicked on and is active
      if (Current_Page == "Reflect") & (Subject_Box_active == 1):
        # if the inputted key is a backspace then remove the last character in the message
        if event.key == pygame.K_BACKSPACE:
          # removing the last letter by using slicing of a string
          subject_message = subject_message[0:len(subject_message)-1]
        else:
          # add the inputted characters to the message that the user types
          subject_message = subject_message + event.unicode 
      # if the summary box has been clicked on and is active
      if (Current_Page == "Reflect") & (Summary_Box_active == 1):
        # if the inputted key is a backspace then remove the last character in the message
        if event.key == pygame.K_BACKSPACE:
          # removing the last letter by using slicing of a string
          summary_message = summary_message[0:len(summary_message)-1]
        else:
          # add the inputted characters to the message that the user types
          summary_message = summary_message + event.unicode


  # calling functions based on the current page being displayed
  match Current_Page:
    case "Menu":
      MenuScreen()

    case "Timer":
      TimerScreen()
      # during the timer stage count down the timer every frame
      PomdoroTimer.decrement()
      # checking if the timer is finished
      if (PomdoroTimer.isFinished()== True) :
        # resetting the tiemr and calling the next age which is the break page
        Current_Page = "Reflect"
        PomdoroTimer.Reset()
        BreakTimer.Minutes = 5
        BreakTimer.Seconds = 0
        # setting the study duration so that it can be saved in the excel
        StudyDuration = 25

    # if in the timer stage of the program
    case "BreakTimer":
      BreakTimerScreen()
      # decrerment the timer
      BreakTimer.decrement()
      if (BreakTimer.isFinished()== True) :
        # mpoving back to the menu screen if timer finished and resetting the timer for next time
        Current_Page = "Menu"
        BreakTimer.Reset()

    case "CustomTimerCreation":
      CustomTimerCreation()

    case "CustomTimerCount":
      CustomTimerCount()
      CustomTimer.decrement()
      if (CustomTimer.isFinished()== True) :
        Current_Page = "Reflect"
        CustomTimer.Reset()

    case "Reflect":
      Reflect()

    # default case for it other casses not activated
    case _:
      MenuScreen()

  # progressing the game clock in the main loop
  clock.tick(FPS)
  # updating the game screen
  pygame.display.update()