from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 200
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    
    def __init__(self):

        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE)-1) * SPACE_SIZE
            if [x, y] not in snake.coordinates:
                break

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):

    if is_paused:
        return
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    if not is_paused:
        next_turn(snake, food)
    pause_button.config(text="Resume" if is_paused else "Paused")

def check_collisions(snake):
    x,y = snake.coordinates[0]

    if  x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
        
    return False


def game_over():
    global restart_button, restart_button_id
    canvas.delete("snake")
    canvas.delete("food")

    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

    if restart_button_id is None:
        restart_button = Button(window, text="Restart", font=("consolas", 20), command=restart_game)
        restart_button_id = canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 100, window=restart_button, tag="restart-button")



def restart_game():
    global score, direction, snake, food, restart_button, restart_button_id 

    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))

    canvas.delete("all")
    canvas.delete("restart-button")

    if restart_button:
        restart_button.destroy()
        restart_button = None

    restart_button_id = None

    snake = Snake()
    food = Food()

    next_turn(snake, food)

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'
is_paused = False
restart_button = None
restart_button_id = None

top_frame = Frame(window)
top_frame.pack(pady=10)

label = Label(top_frame, text="Score:{}".format(score), font=('consolas', 20))
label.pack(side=LEFT, padx=10)

pause_button = Button(top_frame, text="Pause", font=('consolas', 12), command=lambda: toggle_pause())
pause_button.pack(side=LEFT, padx=5)



canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")


window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()