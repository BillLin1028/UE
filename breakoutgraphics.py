"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random
from campy.gui.events.timer import pause

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 20      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 150      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 10        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)
        self.window_width = window_width
        self.window_height = window_height
        # Create a paddle
        self.paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT,x=(window_width - PADDLE_WIDTH) / 2, y=window_height - paddle_height - PADDLE_OFFSET)
        self.paddle.filled = True
        self.paddle.fill_color = "black"
        self.window.add(self.paddle)

    def create_ball(self):
        # Center a filled ball in the graphical window
        self.ball = GOval(BALL_RADIUS*2,BALL_RADIUS*2,x=self.window_width/2-BALL_RADIUS,y=self.window_height/2-BALL_RADIUS)
        self.ball.filled = True
        self.ball.fill_color = "black"
        self.window.add(self.ball)
        # Default initial velocity for the ball
        # Initialize our mouse listeners
    def create_bricks(self):
        bric_y = BRICK_OFFSET
        count = 0
        for row in range(BRICK_ROWS):
            bric_x = 0
            for col in range(BRICK_COLS):
                bric = GRect(BRICK_WIDTH, BRICK_HEIGHT)
                bric.filled = True
                if count <=2:
                    bric.fill_color = 'red'
                elif 2<count<=4:
                    bric.fill_color = 'yellow'
                elif 4<count<=6:
                    bric.fill_color = 'blue'
                elif 6<count<=8:
                    bric.fill_color = 'green'
                else:
                    bric.fill_color = 'orange'
                self.window.add(bric, x=bric_x, y=bric_y)
                bric_x += (BRICK_WIDTH + BRICK_SPACING)
            count+=1
            bric_y += BRICK_HEIGHT + BRICK_SPACING# Draw bricks
    def start(self):
        self.__dx = 0
        self.__dy = 0
        self.is_ball_moving = False
        onmousemoved(self.mouse_moved)
        onmouseclicked(self.ball_drop)



    def mouse_moved(self, event):
        self.paddle.x = event.x - PADDLE_WIDTH / 2

    def ball_drop(self, event):
        if not self.is_ball_moving:
            self.is_ball_moving = True
            self.__dy = INITIAL_Y_SPEED
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx

            while True:
                # Check collision with objects
                top_left = self.window.get_object_at(self.ball.x, self.ball.y)
                top_right = self.window.get_object_at(self.ball.x + 2 * BALL_RADIUS, self.ball.y)
                bottom_left = self.window.get_object_at(self.ball.x, self.ball.y + 2 * BALL_RADIUS)
                bottom_right = self.window.get_object_at(self.ball.x + 2 * BALL_RADIUS, self.ball.y + 2 * BALL_RADIUS)

                # Check collision with bricks
                if top_left is not None and top_left is not self.paddle:
                    self.window.remove(top_left)
                    self.__dy = -self.__dy
                elif top_right is not None and top_right is not self.paddle:
                    self.window.remove(top_right)
                    self.__dy = -self.__dy
                elif bottom_left is not None and bottom_left is not self.paddle:
                    self.window.remove(bottom_left)
                    self.__dy = -self.__dy
                elif bottom_right is not None and bottom_right is not self.paddle:
                    self.window.remove(bottom_right)
                    self.__dy = -self.__dy

                # Check collision with paddle
                if self.ball.y + 2 * BALL_RADIUS >= self.paddle.y:
                    if top_left is self.paddle or top_right is self.paddle or bottom_left is self.paddle or bottom_right is self.paddle:
                        self.__dy = -self.__dy

                # Move the ball
                self.ball.move(self.__dx, self.__dy)

                if self.ball.x + 2 * BALL_RADIUS > self.window.width or self.ball.x <= 0:
                    self.__dx = -self.__dx
                if self.ball.y <= 0:
                    self.__dy = -self.__dy
                if self.ball.y + 2 * BALL_RADIUS > self.window.height:
                    self.game_over()
                    break
                pause(10)


    def game_over(self):
        self.window.remove(self.ball)
        self.is_ball_moving = False

        game_over_label = GLabel("Game Over")
        game_over_label.font = "SansSerif-36"
        self.window.add(game_over_label, (self.window.width - game_over_label.width) / 2,
                        (self.window.height - game_over_label.height) / 2)

        onmouseclicked(self.restart_game)

    def restart_game(self, event):
        self.window.clear()
        self.create_bricks()
        self.create_ball()
        self.window.add(self.paddle)
        self.start()