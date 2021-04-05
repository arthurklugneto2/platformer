import pygame
from Modules.screenSystem import ScreenSystem

# ============================ 
# Application State Variables
# ============================
applicationDone = False

# ============================
# Global Variables
# ============================
# WIDTH = 512
# HEIGHT = 320
# SCALE = 1
WIDTH = 1024
HEIGHT = 640
SCALE = 2
display = None
clock = None
buffer = None

# ===========================
# Global Systems
# ===========================
screenSystem = None

# ===========================
# Application Setup
# ===========================
def setup():

    # init pygame
    pygame.init()
    pygame.font.init()

    # initialize global variables
    global clock
    global display
    global buffer

    clock = pygame.time.Clock()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    buffer = pygame.Surface((int(WIDTH/SCALE),int(HEIGHT/SCALE)))

    # load screen System and initial screen
    global screenSystem
    screenSystem = ScreenSystem()
    screenSystem.loadScreeen('GAME_SCREEN',buffer,display,(WIDTH,HEIGHT),SCALE)
setup()

# ===========================
# Application Loop
# ===========================
while not applicationDone:

    clock.tick(60)
    keys = pygame.key.get_pressed()

    event = pygame.event.get()

    for e in event:
        if e.type == pygame.QUIT:
            applicationDone = True

    screenSystem.update(keys)
    screenSystem.draw(buffer,display,(WIDTH,HEIGHT),keys)
    
    pygame.display.flip()