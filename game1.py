from typing import OrderedDict
import arcade
import numpy as np
import networkx as nx

WIDTH = 20
HEIGHT = 20
MARGIN = 5
ROW_COUNT = 8
COLUMN_COUNT = 8
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 400

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BALL_BLUE)
        self.score = 0
        self.edges = [(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(3,6),(4,6)]
        self.G = nx.Graph()
        self.G.add_edges_from(self.edges)
        self.new_round()
        

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        
        for i,row in enumerate(self.link_grid.values()): #print links grid
            for column in range(COLUMN_COUNT):
                if row[column] == 0:
                    self.text_box(column+14,i+3,1,arcade.color.WHITE)
                else:
                    self.text_box(column+14,i+3,1,arcade.color.BLACK)

        for i,row in enumerate(self.ans_grid.values()): #print answer grid
            for column in range(COLUMN_COUNT):
                if row[column] == 0:
                    self.text_box(column+1,i+3,1,arcade.color.WHITE)
                else:
                    self.text_box(column+1,i+3,1,arcade.color.BLACK)

        for column in range(COLUMN_COUNT): #print spectrum slots
            if self.spec_grid[column] == 0:
                self.text_box(column+1,2,1,arcade.color.BALL_BLUE)
            else:
                self.text_box(column+1,2,1,arcade.color.GREEN)

        self.text_box(4.5,1,1,arcade.color.PINK,str(self.source)) #print source node
        self.text_box(4.5,11,1,arcade.color.PINK,str(self.target)) #print target node
        self.text_box(1,13,3,arcade.color.PINK,"Refresh") 
        self.text_box(17,13,4,arcade.color.PINK,"New Round") 
        self.text_box(10,13,2,arcade.color.PINK,"Go!") 
        self.text_box(17,15,4,arcade.color.PINK,"Topology") 
        self.text_box(10,15,4,arcade.color.PINK,"Score: {}".format(self.score))

        for i, edge in enumerate(self.link_grid): #print links next to link grid
            self.text_box(12,i+3,2,arcade.color.PINK,"{}-{}".format(edge[0],edge[1]))

        for i,edge in enumerate(self.ans_grid): #print links next to answer grid
            self.text_box(9,i+3,2,arcade.color.PINK,"{}-{}".format(edge[0],edge[1]))


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
        
        if self.column > 11 and self.column < 22 and self.row > 2 and self.row < 11:# If one of the links in the link grid were clicked 
            self.update_ans_grid()

        elif self.column in [1,2,3] and self.row == 13: #refresh clicked
            self.refresh()

        elif self.column in [17,18,19,20] and self.row == 13: #new round clicked
            self.new_round()

        elif self.row == 2 and self.column < COLUMN_COUNT-self.slots+2 and self.column > 0: #spectrum grid clicked
            self.first_slot = self.column - 1 #move slots position 
            self.update_spec_grid()

        elif self.column in [10,11] and self.row == 13: #GO clicked
            self.check_solution()

        elif self.column in [17,18,19,20] and self.row == 15: #topology clicked
            topology_view = topologyView(self)
            self.window.show_view(topology_view) #show topology diagram 

        else:
            print("Out of bounds")

    def update_spec_grid(self):
        self.spec_grid = np.zeros(COLUMN_COUNT, dtype= int)
        for i in range(self.slots):
            self.spec_grid[self.first_slot+i] = 1

    def update_ans_grid(self):
        """
        Updates answer grid with selected link 
        """
        edge = self.edges[self.row-3] #get the edge that row corresponds to

        if self.ans_grid_count >= ROW_COUNT: #if answer grid if full
            print("Answer grid full!")
        else:
            if self.row not in self.selected: #if link has not already been selected
                self.ans_grid[edge] = self.link_grid[edge] #save edge to answer grid
                self.selected.append(self.row)  
                self.ans_grid_count += 1
            else:
                print("That link has already been selected")

    def refresh(self):
        """
        Refreshes the answer grid
        """
        print("Refresh")
        self.selected = []
        self.ans_grid = {}
        self.ans_grid_count = 0
    
    def new_round(self):
        """
        Initiates new round that contains a solution
        """
        has_solution = False
        while not has_solution:
            self.roundSetup()
            has_solution = self.has_solution()
                                  
    def roundSetup(self):
        """
        Sets up all parameters for a new round
        """
        self.ans_grid_count = 0
        self.selected = []
        self.first_slot = 0
        self.target = np.random.randint(2,7)
        self.source = np.random.randint(1,self.target)
        self.link_grid = OrderedDict()
        self.ans_grid = OrderedDict()
        self.slots = np.random.randint(2,5)

        self.update_spec_grid()#populate spectrum grid

        for edge in self.edges: #populate link grid
            self.link_grid[edge] = np.random.randint(2,size = COLUMN_COUNT) 

    def has_solution(self):
        """
        Checks if round parameters contain a solution
        """
        #find all possible paths between source and target
        all_paths = nx.all_simple_paths(self.G,self.source,self.target) 
        for path in all_paths: #for each possible path
            i = 0 
            all_edges = []
            while i < len(path)-1: #prepare all edges in path
                if path[i] < path[i+1]:
                    all_edges.append((path[i],path[i+1]))
                else:
                    all_edges.append((path[i+1],path[i]))
                i+=1

            temp_ans_grid = {}
            for edge in all_edges: #populate answer grid with edges 
                temp_ans_grid[edge]= self.link_grid[edge]

            #for each possible position of the spectrum slots
            for i in range(COLUMN_COUNT-self.slots+1): 
                if self.is_solution(temp_ans_grid,i): #check if solution is correct
                    return True

    def check_solution(self):
        """
        Checks for solution
        """
        if self.is_solution(self.ans_grid,self.first_slot): #check if solution is correct
                self.score += 10
                win_view = winView(self) 
                self.window.show_view(win_view) #show win screen
        else:
            print("Try again")

    def is_solution(self,ans_grid,first_slot):
        """
        Checks if a path and slot combination is the correct solution for RSA
        """
        edges = []
        for edge in ans_grid.keys(): #save all edges to a list
            edges.append(edge[0])
            edges.append(edge[1])

        if not edges[0] == self.source: #if first node isn't source switch them
            edges = self.swapList(edges,0,1)

        for i in range(1,len(edges)-2,2): #for each edge
            #if second node of the first edge doesn't match with the first node of the next edge
            if not edges[i] == edges[i+1]:
                edges = self.swapList(edges,i+1,i+2) # switch round the next edge

        path = list(dict.fromkeys(edges)) #remove duplicates
        #if first node isn't source or end node isn't target or path doesn't exist
        if path[0] != self.source or path[-1] != self.target or nx.is_path(self.G,path) == False: 
            return False
            
        for row in ans_grid.values(): #for spectrum of each link
            for i in range(self.slots): #for each slot
                if row[first_slot + i] != 0: #if slot in spectrum is occupied 
                    return False
        return True

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

class winView(arcade.View):
    """
    View class for viewing Win screen
    """
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        self.background = arcade.load_texture("pics\youwin.jpg")
    
    def on_draw(self):
        arcade.start_render()
        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,self.background)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.game_view.new_round()
        self.window.show_view(self.game_view)

def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT) #initiate window
    start_view=GameView() #start with game view
    window.show_view(start_view)    
    arcade.run()


if __name__ == "__main__":
    main()