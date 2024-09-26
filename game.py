from tkinter import *
import random
import time


# Create class ball.

class Ball:
    def __init__(self, canvas_ball, paddle_ball, color):
        self.canvas = canvas_ball
        self.paddle = paddle_ball
        self.id = canvas_ball.create_oval(10, 10, 25, 25, fill=color)  # Create oval (id).
        self.canvas.move(self.id, 200, 275)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    #
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3 + res / acceleration
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos):
            self.y = -5.5 - res / acceleration
            result()
        if pos[0] <= 0:
            self.x = 3 + res / acceleration
        if pos[2] >= self.canvas_width:
            self.x = -3 - res / acceleration


# Create class paddle_ball.
class Paddle:
    def __init__(self, canvas_paddle, color):
        self.canvas = canvas_paddle
        self.id = canvas_paddle.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-a>', self.turn_left)

        self.canvas.bind_all('<KeyPress-Down>', self.stand)
        self.canvas.bind_all('<KeyPress-s>', self.stand)

        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-d>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -3 - res / acceleration

    def stand(self, evt):
        self.x = 0

    def turn_right(self, evt):
        self.x = 3 + res / acceleration


tk = Tk()
tk.title("Game")
tk.resizable(False, False)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()
res = 0
acceleration = 100


def result():
    global res
    res += 1
    print(res)
    lbl1.config(text=res)


lbl1 = Label(tk, text=f"{0}", font=("Impact", 20))
lbl1.place(x=15, y=15)
paddle = Paddle(canvas, 'red')
ball = Ball(canvas, paddle, 'red')
while 1:
    if not ball.hit_bottom:
        ball.draw()
        paddle.draw()
    else:
        canvas.create_text(250, 150, text='Game Over\n:(', font=("Times New Roman", 40))
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)    
