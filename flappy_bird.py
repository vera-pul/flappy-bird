from sense_hat import SenseHat
from random import randint
from time import sleep

sense = SenseHat()

PIPE_COLOR = (0, 255, 0)
BG_COLOR = (0, 0, 128)
BIRD_COLOR = (255, 128 , 0)
HIT_BIRD_COLOR = (255, 0, 0)
MATRIX_SIZE = 8
SPEED = 1
PIPE_FREQUENCY = 3

game_over = False
pipes_passed = 0
x = 0
y = 0

frame = [[BG_COLOR for column in range(MATRIX_SIZE)] for row in range(MATRIX_SIZE)]

def flatten(matrix):
    """ Convert matrix to array. """
    flattened = [pixel for row in matrix for pixel in row]
    return flattened

def add_pipes(matrix):
    """
    Add a pipe to the end of the matrix with a random 3 squares large gap.
    """
    for row in matrix:
        row[-1] = PIPE_COLOR
    gap = randint(1, MATRIX_SIZE - 2)
    matrix[gap][-1] = BG_COLOR
    matrix[gap - 1][-1] = BG_COLOR
    matrix[gap + 1][-1] = BG_COLOR
    return matrix

def move_pipes(matrix):
    """
    Move all pipes one square to the left.
    """
    for row in matrix:
        for i in range(MATRIX_SIZE - 1):
            row[i] = row[i + 1]
        row[-1] = BG_COLOR
    return matrix

def move_bird(event):
    """
    Move the bird according to a joystick inteaction.
    Set game over if the bird hits a pipe.
    """
    global y
    global x
    global game_over
    sense.set_pixel(x, y, BG_COLOR)
    if event.action == "pressed":
        if event.direction == "up" and y > 0:
            y -= 1
        elif event.direction == "down" and y < MATRIX_SIZE - 1:
            y += 1
        elif event.direction == "right" and x < MATRIX_SIZE - 1:
            x += 1
        elif event.direction == "left" and x > 0:
            x -= 1
    
    game_over = is_game_over(x, y, frame, game_over)
    draw_bird(x, y, game_over)
        
def drop_bird(x, matrix):
    """
    Move the bird one squre down.
    Set game over if the bird hits a pipe.
    """
    global y
    global game_over
    sense.set_pixel(x, y, BG_COLOR)
    if y < MATRIX_SIZE - 1:
        y += 1
    game_over = is_game_over(x, y, matrix, game_over)
    draw_bird(x, y, game_over)
            
def is_game_over(x, y, matrix, game_over):
    """
    Checks if the game should be over.
    """
    if matrix[y][x] == PIPE_COLOR or game_over:
        return True
    else:
        return False
    
def draw_bird(x, y, game_over):
    """
    Draw the bird a color dependent on wether the game should be over.
    """
    if game_over:
        sense.set_pixel(x, y, HIT_BIRD_COLOR)
    else:
        sense.set_pixel(x, y, BIRD_COLOR)
        
def has_pipe_passed(matrix):
    """
    Return true if a pipe reaches the left edge.
    """
    for i in range(MATRIX_SIZE):
        if matrix[i][0] == PIPE_COLOR:
            return True
        else:
            return False

# interacting with the joystick triggers an event
sense.stick.direction_any = move_bird

# Actual gameplay
while not game_over:
    # Add pipes every couple seconds
    frame = add_pipes(frame)
    for i in range(PIPE_FREQUENCY):
        frame = move_pipes(frame)
        sense.set_pixels(flatten(frame))
        # Update score
        if has_pipe_passed(frame):
            pipes_passed += 1
        # After game over, let bird flap around until next pipe is added
        game_over = is_game_over(x, y, frame, game_over)
        draw_bird(x, y, game_over)
        # Drop bird twice in a single frame
        drop_bird(x, frame)
        sleep(float(SPEED) / 2)
        drop_bird(x, frame)
        sleep(float(SPEED) / 2)
# Game over (shows how many pipes reached the left edge)
sense.show_message(str(pipes_passed))
sense.clear()

