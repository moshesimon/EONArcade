import arcade
from arcade.color import FALU_RED
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

WIDTH = 20
HEIGHT = 20
MARGIN = 5
ROW_COUNT = 7
COLUMN_COUNT = 8
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 400


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.BALL_BLUE)
        self.score = 0
        self.new_round()
        

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        
        for i,row in enumerate(self.grid.values()): # print links grid
            for column in range(COLUMN_COUNT):
                if row[column] == 0:
                    self.text_box(column+14,i+3,1,arcade.color.WHITE)
                else:
                    self.text_box(column+14,i+3,1,arcade.color.BLACK)
        if self.ans_grid:
            for i,row in enumerate(self.ans_grid.values()):
                for column in range(COLUMN_COUNT):
                    if row[column] == 0:
                        self.text_box(column+1,i+3,1,arcade.color.WHITE)
                    else:
                        self.text_box(column+1,i+3,1,arcade.color.BLACK)

        for column in range(COLUMN_COUNT):# print slots
            if self.specgrid[column] == 0:
                self.text_box(column+self.first_slot+1,2,1,arcade.color.BALL_BLUE)
            else:
                self.text_box(column+self.first_slot+1,2,1,arcade.color.GREEN)

        self.text_box(4.5,1,1,arcade.color.PINK,str(self.source))
        self.text_box(4.5,10,1,arcade.color.PINK,str(self.target))
        self.text_box(1,13,3,arcade.color.PINK,"Refresh")
        self.text_box(17,13,4,arcade.color.PINK,"New Round")
        self.text_box(10,13,2,arcade.color.PINK,"Go!")
        self.text_box(10,15,3,arcade.color.PINK,"Score: {}".format(self.score))
        for i, edge in enumerate(self.grid):
            self.text_box(12,i+3,2,arcade.color.PINK,"{}-{}".format(edge[0],edge[1]))
        if self.ans_grid:
            for i,edge in enumerate(self.ans_grid):
                self.text_box(9,i+3,2,arcade.color.PINK,"{}-{}".format(edge[0],edge[1]))


    def text_box(self,col,row,width,colour,text=None):
        if width%2 == 0:
            arcade.draw_rectangle_filled((col + width/2)*(MARGIN+WIDTH) - (MARGIN+WIDTH)/2,row*(MARGIN+HEIGHT),width*(WIDTH+MARGIN)-MARGIN,HEIGHT,colour)
        else:
            arcade.draw_rectangle_filled((col + width//2)*(MARGIN+WIDTH),row*(MARGIN+HEIGHT),width*(WIDTH+MARGIN)-MARGIN,HEIGHT,colour)
        if text:
            arcade.draw_text(text,col*(MARGIN+WIDTH)-(WIDTH/4),row*(MARGIN+HEIGHT)-(WIDTH/4),arcade.color.BLACK,12)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        column = int((x +(WIDTH+MARGIN)/2)// (WIDTH + MARGIN))
        row = int((y+(HEIGHT+MARGIN)/2) // (HEIGHT + MARGIN))
        
        if column > 13 and column < 21 and row > 2 and row < 10:
            edge = self.edges[row-3]
            if self.count >= ROW_COUNT:
                print("Answer grid full!")
            else:
                if row not in self.selected:
                    self.ans_grid[edge] = self.grid[edge]
                    self.selected.append(row)  
                    self.count += 1
                else:
                    print("That link has already been selected")
        elif column in [1,2,3] and row == 13: # refresh
            self.refresh()
        elif column in [17,18,19,20] and row == 13: # new round
            print("New Round")
            self.new_round()
        elif row == 2 and column < COLUMN_COUNT-self.slots+2:
            self.first_slot = column - 1
        elif column in [10,11] and row == 13:
            if self.is_solution(self.ans_grid,self.first_slot):
                self.score += 1
                self.new_round()
                print("Well Done!!!")
            else:
                print("Try again")
                #self.refresh()

        else:
            print("Out of bounds")

    def refresh(self):
        print("Refresh")
        self.selected = []
        self.ans_grid = {}
        self.count = 0
    
    def new_round(self):
        has_solution = False
        self.edges = [(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(1,5),]
        self.G = nx.Graph()
        self.G.add_edges_from(self.edges)
        #nx.draw_networkx(self.G)
        #plt.show()
        while not has_solution:
            self.count = 0
            self.selected = []
            self.first_slot = 0
            self.target = np.random.randint(2,6)
            self.source = np.random.randint(1,self.target)
            self.grid = {}
            for edge in self.edges:
                self.grid[edge] = np.random.randint(2,size = COLUMN_COUNT)
            self.ans_grid = {}
            self.specgrid = np.zeros(COLUMN_COUNT, dtype= int)
            self.slots = np.random.randint(1,5)
            for i in range(self.slots):
                self.specgrid[i] = 1
            all_paths = nx.all_simple_paths(self.G,self.source,self.target)
            
            for path in all_paths:
                i = 0 
                all_edges = []
                while i < len(path)-1:
                    if path[i] < path[i+1]:
                        all_edges.append((path[i],path[i+1]))
                    else:
                        all_edges.append((path[i+1],path[i]))
                    i+=1
                temp_ans_grid = {}
                for edge in all_edges:
                    temp_ans_grid[edge]= self.grid[edge]
                    
                for i in range(COLUMN_COUNT-self.slots+2):
                    if self.is_solution(temp_ans_grid,i):
                        has_solution = True
                        #print("Solution exists!")
                        
                        break 
                if has_solution:
                    break
            
        


    def is_solution(self,ans_grid,first_slot):
        G = nx.Graph()
        G.add_edges_from(ans_grid.keys())
        try:
            nx.has_path(G,self.source,self.target)
            #print("Path Found!")
            for row in ans_grid.values():
                for i in range(self.slots):
                    if row[first_slot + i] != 0:
                        #print("Wrong solution")
                        return False
            return True
        except:
            #print("No path exists")
            return False


def main():

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)

    arcade.run()


if __name__ == "__main__":
    main()