import arcade
import numpy as np
#from pyglet.libs.x11.xlib import WidthValue
WIDTH = 20
HEIGHT = 20
MARGIN = 5
ROW_COUNT = 6
COLUMN_COUNT = 8
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BALL_BLUE)
        
        self.new_round()
        

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.grid[row][column] == 0:
                    arcade.draw_rectangle_filled(SCREEN_WIDTH - (column*(WIDTH +MARGIN)+ MARGIN + WIDTH/2), row*(HEIGHT +MARGIN)+HEIGHT/2 + MARGIN + 20,WIDTH,HEIGHT,arcade.color.WHITE,0)
                else:
                    arcade.draw_rectangle_filled(SCREEN_WIDTH - (column*(WIDTH +MARGIN)+ MARGIN + WIDTH/2), row*(HEIGHT +MARGIN)+HEIGHT/2 + MARGIN+ 20,WIDTH,HEIGHT,arcade.color.BLACK,0)
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                if self.ansgrid[row][column] == 0:
                    arcade.draw_rectangle_filled(column*(WIDTH +MARGIN)+ MARGIN + WIDTH/2, row*(HEIGHT +MARGIN)+HEIGHT/2 + MARGIN + 45,WIDTH,HEIGHT,arcade.color.WHITE,0)
                else:
                    arcade.draw_rectangle_filled(column*(WIDTH +MARGIN)+ MARGIN + WIDTH/2, row*(HEIGHT +MARGIN)+HEIGHT/2 + MARGIN+ 45,WIDTH,HEIGHT,arcade.color.BLACK,0)

        for column in range(COLUMN_COUNT):
            if self.specgrid[column] == 0:
                arcade.draw_rectangle_filled(column*(WIDTH +MARGIN)+ MARGIN + WIDTH/2, HEIGHT/2 + MARGIN + 25,WIDTH,HEIGHT,arcade.color.BALL_BLUE,0)
            else:
                arcade.draw_rectangle_filled(column*(WIDTH +MARGIN)+ MARGIN + WIDTH/2, HEIGHT/2 + MARGIN+ 25,WIDTH,HEIGHT,arcade.color.GREEN,0)

        arcade.draw_rectangle_filled(2*MARGIN + (WIDTH +MARGIN),12*(HEIGHT +MARGIN)+HEIGHT/2 + MARGIN,WIDTH*3,HEIGHT,arcade.color.AMARANTH_PINK,0)
        arcade.draw_text("Refresh",MARGIN,12*(HEIGHT +MARGIN)+ MARGIN + 2,arcade.color.BLACK,12)

        arcade.draw_rectangle_filled(18*(WIDTH +MARGIN),12*(HEIGHT +MARGIN)+HEIGHT/2 + MARGIN,WIDTH*5 -5,HEIGHT,arcade.color.AMARANTH_PINK,0)
        arcade.draw_text("New Round",16*(HEIGHT + MARGIN)+MARGIN,12*(HEIGHT +MARGIN)+ MARGIN + 2,arcade.color.BLACK,12)

        arcade.draw_rectangle_filled(4*(WIDTH +MARGIN)+ MARGIN,HEIGHT/2 + MARGIN, WIDTH, HEIGHT,arcade.color.AMARANTH_PINK,0)
        arcade.draw_text(self.source,4*(WIDTH +MARGIN),HEIGHT/2,arcade.color.BLACK,12)

        arcade.draw_rectangle_filled(4*(WIDTH +MARGIN)+ MARGIN,12*(HEIGHT +MARGIN)+HEIGHT/2 + MARGIN, WIDTH, HEIGHT,arcade.color.AMARANTH_PINK,0)
        arcade.draw_text(self.destination,4*(WIDTH +MARGIN),12*(HEIGHT +MARGIN)+HEIGHT/2,arcade.color.BLACK,12)

        arcade.draw_rectangle_filled(11*(WIDTH +MARGIN)+ MARGIN,1*(HEIGHT +MARGIN)+HEIGHT/2, WIDTH*1.5, HEIGHT,arcade.color.AMARANTH_PINK,0)
        arcade.draw_text("1-2",10*(WIDTH +MARGIN)+ MARGIN*3,1*(HEIGHT +MARGIN)+MARGIN,arcade.color.BLACK,12)

        arcade.draw_rectangle_filled(11*(WIDTH +MARGIN)+ MARGIN,2*(HEIGHT +MARGIN)+HEIGHT/2, WIDTH*1.5, HEIGHT,arcade.color.AMARANTH_PINK,0)
        arcade.draw_text("2-3",10*(WIDTH +MARGIN)+ MARGIN*3,2*(HEIGHT +MARGIN)+MARGIN,arcade.color.BLACK,12)

        arcade.draw_rectangle_filled(11*(WIDTH +MARGIN)+ MARGIN,3*(HEIGHT +MARGIN)+HEIGHT/2, WIDTH*1.5, HEIGHT,arcade.color.AMARANTH_PINK,0)
        arcade.draw_text("1-4",10*(WIDTH +MARGIN)+ MARGIN*3,3*(HEIGHT +MARGIN)+MARGIN,arcade.color.BLACK,12)

        arcade.draw_rectangle_filled(11*(WIDTH +MARGIN)+ MARGIN,4*(HEIGHT +MARGIN)+HEIGHT/2, WIDTH*1.5, HEIGHT,arcade.color.AMARANTH_PINK,0)
        arcade.draw_text("3-5",10*(WIDTH +MARGIN)+ MARGIN*3,4*(HEIGHT +MARGIN)+MARGIN,arcade.color.BLACK,12)

        arcade.draw_rectangle_filled(11*(WIDTH +MARGIN)+ MARGIN,5*(HEIGHT +MARGIN)+HEIGHT/2, WIDTH*1.5, HEIGHT,arcade.color.AMARANTH_PINK,0)
        arcade.draw_text("2-5",10*(WIDTH +MARGIN)+ MARGIN*3,5*(HEIGHT +MARGIN)+MARGIN,arcade.color.BLACK,12)

        arcade.draw_rectangle_filled(11*(WIDTH +MARGIN)+ MARGIN,6*(HEIGHT +MARGIN)+HEIGHT/2, WIDTH*1.5, HEIGHT,arcade.color.AMARANTH_PINK,0)
        arcade.draw_text("4-5",10*(WIDTH +MARGIN)+ MARGIN*3,6*(HEIGHT +MARGIN)+MARGIN,arcade.color.BLACK,12)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        column = x // (WIDTH + MARGIN)
        row = y // (HEIGHT + MARGIN)
        if x > (SCREEN_WIDTH - COLUMN_COUNT*(WIDTH +MARGIN)) and x < SCREEN_WIDTH and y > (20 + MARGIN) and y < (ROW_COUNT*(HEIGHT + MARGIN) + 20):
            print(row)
            self.ansgrid[self.count] = np.flipud(self.grid[row-1])
            self.count += 1
        elif column in [0,1,2] and row == 12:
            print("refresh")
            self.ansgrid = np.random.randint(1,size = (ROW_COUNT,COLUMN_COUNT))
            self.count = 0
        elif column in [16,17,18,19] and row == 12:
            print("new round")
            self.new_round()

        else:
            print("Out of bounds")
    
    def new_round(self):
        self.count = 0
        self.destination = str(np.random.randint(2,6))
        self.source = str(np.random.randint(1,int(self.destination)))
        self.grid = np.random.randint(2,size = (ROW_COUNT,COLUMN_COUNT))
        self.ansgrid = np.zeros((ROW_COUNT,COLUMN_COUNT),dtype=int)
        self.specgrid = np.zeros(COLUMN_COUNT, dtype= int)
        self.slots = np.random.randint(1,5)
        self.startslot =np.random.randint(COLUMN_COUNT-self.slots)
        print(self.slots, self.startslot)
        for i in range(self.slots):
            self.specgrid[i + self.startslot] = 1
        print(self.specgrid)

        print(self.grid)



def main():

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()