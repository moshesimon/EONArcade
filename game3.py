from typing import OrderedDict
import arcade
import numpy as np
import networkx as nx
import time
from itertools import islice

WIDTH = 20
HEIGHT = 20
MARGIN = 5
ROW_COUNT = 8
COLUMN_COUNT = 8
SCREEN_WIDTH = 1150
SCREEN_HEIGHT = 350
TIME = 30

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BALL_BLUE)
        self.high_score = 0
        self.new_game()
        
    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        k = 0
        for path in self.paths:
            for i,row in enumerate(self.path_grid(path).values()): #print links grid
                for column in range(COLUMN_COUNT):
                    if row[column] == 0:
                        self.text_box(column+1 + k*9,i+3,1,arcade.color.WHITE)
                    else:
                        self.text_box(column+1 + k*9,i+3,1,arcade.color.BLACK)
            self.text_box(1 + k*9,8,8,arcade.color.PINK,f"Path {k+1}: {path}")
            k +=1

        for column in range(COLUMN_COUNT*5 + 4): #print slots
            if self.spec_grid[column] == 0:
                self.text_box(column+1,2,1,arcade.color.BALL_BLUE)
            else:
                self.text_box(column+1,2,1,arcade.color.GREEN)

        self.text_box(1,10,12,arcade.color.PINK,str(f"Request: (Source:{self.source}, Target:{self.target}, Slots:{self.slots})")) #print source node
        #self.text_box(1,15,2,arcade.color.PINK,self.timer)
        #self.text_box(1,13,3,arcade.color.PINK,"Refresh") 
        #self.text_box(16,12,4,arcade.color.PINK,"New Game") 
        #self.text_box(13,12,2,arcade.color.PINK,"Go!") 
        self.text_box(18,12,4,arcade.color.PINK,"Topology") 
        self.text_box(8,12,4,arcade.color.PINK,"Score: {}".format(self.score))
        self.text_box(1,12,6,arcade.color.PINK,"High Score: {}".format(self.high_score))
        self.text_box(13,12,4,arcade.color.PINK,"BLOCKS: {}".format(self.blocks))
        #self.sprit_list.draw()


        

    def path_grid(self, path):
        i = 0 
        all_edges = []
        while i < len(path)-1: #prepare all edges in path
            if path[i] < path[i+1]:
                all_edges.append((path[i],path[i+1]))
            else:
                all_edges.append((path[i+1],path[i]))
            i+=1

        temp_path_grid = {}
        for edge in all_edges: #populate answer grid with edges 
            temp_path_grid[edge]= self.link_grid[edge]
        return temp_path_grid


    def text_box(self,col,row,width,colour,text=None):
        """
        Prints a rectangle with given dimensions and colour and inserts given text 
        """
        if width%2 == 0:
            arcade.draw_rectangle_filled((col + width/2)*(MARGIN+WIDTH) - (MARGIN+WIDTH)/2,row*(MARGIN+HEIGHT),width*(WIDTH+MARGIN)-MARGIN,HEIGHT,colour)
        else:
            arcade.draw_rectangle_filled((col + width//2)*(MARGIN+WIDTH),row*(MARGIN+HEIGHT),width*(WIDTH+MARGIN)-MARGIN,HEIGHT,colour)
        if text: #print text
            arcade.draw_text(text,col*(MARGIN+WIDTH)-(WIDTH/4),row*(MARGIN+HEIGHT)-(WIDTH/4),arcade.color.BLACK,12)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        self.column = int((x +(WIDTH+MARGIN)/2)// (WIDTH + MARGIN)) #sets the column the mouse was pressed in
        self.row = int((y+(HEIGHT+MARGIN)/2) // (HEIGHT + MARGIN)) #sets the row the mouse was pressed in
        
        if self.column in [17,18,19,20] and self.row == 13: #new round clicked
            self.new_game()

        elif self.row == 2 and self.column < (COLUMN_COUNT*5 + 4)-self.slots+2 and self.column > 0: #spectrum grid clicked
            self.first_slot = self.column - 1 #move slots position 
            self.update_spec_grid()

        elif self.column in [10,11] and self.row == 13: #GO clicked
            self.check_solution()

        elif self.column in [18,19,20,21] and self.row == 12: #topology clicked
            topology_view = topologyView(self)
            self.window.show_view(topology_view) #show topology diagram 
                
        else:
            print("Out of bounds")

    def on_key_press(self, key, modifiers):

        if key == arcade.key.RIGHT and self.first_slot < (COLUMN_COUNT*5 + 4)-self.slots:
            self.first_slot+=1
            self.update_spec_grid()
        elif key == arcade.key.LEFT and self.first_slot > 0:
            self.first_slot -=1
            self.update_spec_grid()
        elif key == arcade.key.ENTER:
            self.check_solution()

    def update_link_grid(self):
        for edge in self.ans_grid.keys():
            grid = self.link_grid[edge]
            for i in range(self.slots):
                grid[self.temp_first_slot+i] = 1
            self.link_grid[edge] = grid

    def update_spec_grid(self):
        self.spec_grid = np.zeros(COLUMN_COUNT*5 + 4, dtype= int)
        for i in range(self.slots):
            self.spec_grid[self.first_slot+i] = 1

    def refresh(self):
        """
        Refreshes the answer grid
        """
        print("Refresh")
        self.selected = []

    
    def new_game(self):
        self.score = 0
        self.blocks = 0
        self.edges = [(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(3,6),(4,6)]
        self.G = nx.Graph()
        self.G.add_edges_from(self.edges)
        self.link_grid = OrderedDict()
        for edge in self.edges: #populate link grid
            self.link_grid[edge] = np.zeros(COLUMN_COUNT, dtype= int)
        self.new_round()                  
                        
    def new_round(self):
        """
        Sets up all parameters for a new round
        """
        self.first_slot = 0
        self.target = np.random.randint(2,7)
        self.source = np.random.randint(1,self.target)
        p = nx.shortest_simple_paths(self.G,self.source,self.target)
        self.paths = list(islice(p,5))
        self.slots = np.random.randint(2,5)
        self.update_spec_grid()#populate spectrum grid

    def check_solution(self):

        if self.is_solution():
            self.score += 10
            self.update_link_grid()
            self.new_round()
        else:
            self.blocks += 1
            if self.blocks > 3:
                self.high_score = self.score
                self.new_game()
            else:
                print("Try again")

    def is_solution(self):
        """
        Checks for solution
        """
        if not self.spec_grid[8] == 1 and not self.spec_grid[17] == 1 and not self.spec_grid[26] == 1 and not self.spec_grid[35] == 1:
            self.path_selected = self.first_slot//9
            self.ans_grid = self.path_grid(self.paths[self.path_selected])
            self.temp_first_slot = self.first_slot - self.path_selected*9
            for row in self.ans_grid.values(): #for spectrum of each link
                for i in range(self.slots): #for each slot
                    if row[self.temp_first_slot + i] != 0: #if slot in spectrum is occupied 
                        return False
            return True
        else:
            return False

    def swapList(self,sl,pos1,pos2):
        """
        Swaps position of two elements in a list
        """
        temp = sl[pos1]
        sl[pos1] = sl[pos2]
        sl[pos2] = temp
        return sl

class topologyView(arcade.View):
    """
    View class for viewing topology
    """

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        self.background = arcade.load_texture("pics\Figure_3.png")

    def on_draw(self):
        arcade.start_render()
        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,self.background)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.window.show_view(self.game_view)

def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT) #initiate window
    start_view=GameView() #start with game view
    window.show_view(start_view)    
    arcade.run()


if __name__ == "__main__":
    main()