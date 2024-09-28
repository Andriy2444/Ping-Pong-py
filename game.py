from tkinter import *
import random
import time


# Create class Ball.

class Ball:
    def __init__(self, canvas_ball, paddle_ball, color):
        self.canvas = canvas_ball
        self.paddle = paddle_ball
        self.id = canvas_ball.create_oval(10, 10, 25, 25, fill=color)  # Create oval (id).
        self.canvas.move(self.id, 200, 275)  # Start position of the ball.
        starts = [-3, -2, -1, 1, 2, 3]  # Possible starting speeds for the ball.
        random.shuffle(starts)  # Randomize the starting speed.
        self.x = starts[0]  # Set horizontal speed.
        self.y = -3  # Set initial vertical speed.
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    # Check if the ball hits the paddle.
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)  # Get paddle position.

        # Check for collision with paddle.
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                return True
        return False

    # Move the ball and handle collisions.
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        # Check for collision with the top of the canvas.
        if pos[1] <= 0:
            self.y = startSpeed + score / acceleration
        # Check if the ball hits the bottom.
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        # Check if the ball hits the paddle.
        if self.hit_paddle(pos):
            self.y = -startSpeed - 2 - (score / acceleration)  # Subtract 2 for additional acceleration after hitting
            result()
        # Check for collision with the left wall.
        if pos[0] <= 0:
            self.x = startSpeed + score / acceleration
        # Check for collision with the right wall.
        if pos[2] >= self.canvas_width:
            self.x = -startSpeed - score / acceleration


# Create class Paddle.
class Paddle:
    def __init__(self, canvas_paddle, color):
        self.canvas = canvas_paddle
        self.id = canvas_paddle.create_rectangle(0, 0, 100, 10, fill=color)  # Create the paddle.
        self.canvas.move(self.id, 200, 300)  # Start position of the paddle.
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()

        # Bind keys for paddle movement.
        # Turn left
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-a>', self.turn_left)

        # Stand
        self.canvas.bind_all('<KeyPress-Down>', self.stand)
        self.canvas.bind_all('<KeyPress-s>', self.stand)

        # Turn Right
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-d>', self.turn_right)

        # Bind mouse movement to control paddle
        self.canvas.bind_all('<Motion>', self.mouse_move)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    # Move paddle left.
    def turn_left(self, evt):
        self.x = -startSpeed - score / acceleration

    # Stop paddle movement.
    def stand(self, evt):
        self.x = 0

    # Move paddle right.
    def turn_right(self, evt):
        self.x = startSpeed + score / acceleration

    # Move paddle according to mouse position.
    def mouse_move(self, evt):
        paddle_pos = self.canvas.coords(self.id)
        mouse_x = evt.x
        paddle_width = paddle_pos[2] - paddle_pos[0]
        # Move the paddle to follow the mouse, keeping it centered under the cursor
        self.canvas.coords(self.id, mouse_x - paddle_width / 2, paddle_pos[1], mouse_x + paddle_width / 2, paddle_pos[3])

# Function to update the score.
def result():
    global score
    score += 1
    print(score)
    lbl1.config(text=score)


# Main game loop.
def run_game():
    while True:
        if not ball.hit_bottom:  # Continue until the ball hits the bottom.
            ball.draw()  # Draw the ball.
            paddle.draw()  # Draw the paddle.
        else:
            # Game end
            canvas.create_text(250, 150, text='Game Over\n:(', font=("Times New Roman", 40))
            tk.update()
            time.sleep(3)
            break
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)  # Delay to control game speed.


# Initialize the Tkinter window.
tk = Tk()
tk.title("Game")
tk.resizable(False, False)  # Disable window resizing.x
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
canvas.config(cursor="none")
tk.update()
score = 0
startSpeed = 3
acceleration = 100  # Set acceleration factor.
# Game speed = startSpeed + (score/acceleration)
# Game speed is 3.2 when score is 20(3 + (20/100) = 3.2)


lbl1 = Label(tk, text=f"{0}", font=("Impact", 20))  # Create a label for the score.
lbl1.place(x=15, y=15)  # Position the score label.
paddle = Paddle(canvas, 'red')  # Create the paddle.
ball = Ball(canvas, paddle, 'red')  # Create the ball.

run_game()
