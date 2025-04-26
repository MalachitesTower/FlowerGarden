import pygame
import sys
import math
import random
from statistics import mean
import pickle
import numpy as np

# Initialize Pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flower Game")

# Base Color Setup
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Font Setup
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

# Sidebar properties
sidebar_width = 200
sidebar = pygame.Rect(0, 0, sidebar_width, HEIGHT)

# Button properties
sidebar_button_locations = [(10,10), (10,70), (10,130)]
sidebar_button_properties = [150, 50]
sidebar_button_labels = ["Plant", "[Pollinate]", "Clear"]
sidebar_buttons = []
for i in range(3):
    sidebar_buttons.append(pygame.Rect(sidebar_button_locations[i],
                                  sidebar_button_properties))
# Dirt Properties
dirt_locations = [(300,HEIGHT - 100), (400,HEIGHT - 100), (500,HEIGHT - 100), (600,HEIGHT - 100), (700, HEIGHT - 100)]
dirt_properties = [50, 22] #w, h
dirts = []
for i in range(5):
    dirts.append(pygame.Rect(dirt_locations[i],
                                  dirt_properties))                                                   
dirt_image = pygame.image.load('dirt4.png') 
dirt_image = pygame.transform.scale(dirt_image, (dirt_properties))  # Scale image to button size

# Function to draw petal
def math_petal(center, scale, petal_shape, rotation_angle, num_points=100):
    """
    Generates points for a teardrop shape based on the parametric equation.

    Args:
        center: Tuple (x, y) for the center of the teardrop.
        scale: Scale factor to resize the teardrop.
        petal_shape: The 'm' parameter that defines the shape.
        num_points: Number of points to sample along the curve.

    Returns:
        A list of (x, y) points representing the teardrop shape.
    """
    points = []
    rotation_radians = rotation_angle #math.radians(rotation_angle)  # Convert angle to radians
    print(math.degrees(rotation_radians))
    for i in range(num_points + 1):
        t = math.pi * 2 * i / num_points  # t ranges from 0 to 2π
        x = math.cos(t)
        y = math.sin(t) * (math.sin(0.5 * t) ** petal_shape)
        rotated_x = x * math.cos(rotation_radians) - y * math.sin(rotation_radians)
        rotated_y = x * math.sin(rotation_radians) + y * math.cos(rotation_radians)        
        points.append((
            center[0] + scale * rotated_x,
            center[1] - scale * rotated_y  # Invert y to match screen coordinates
        ))
    return points

def draw_petal(surface, center, radius, height, color, angle, points_count, petal_shape):
    scale = 15  # Scale factor for the teardrop size
    points_petal = math_petal(center, scale, petal_shape, 2*math.pi-angle)
    pygame.draw.polygon(window, color, points_petal)

# Function to draw petals around a circle
def draw_circle_with_petals(surface, center, center_radius, petal_radius, num_petals, petal_distance, center_color, petal_color, petal_height, points_count, petal_shape):
    # Draw the main circle
    pygame.draw.circle(surface, center_color, center, center_radius)
    
    # Calculate and draw each petal
    angle_step = 360 / num_petals
    for i in range(num_petals):
        angle = math.radians(i * angle_step)  # Convert angle to radians
        # Calculate the petal's position and orientation
        start_x = center[0] + center_radius * math.cos(angle)
        start_y = center[1] + center_radius * math.sin(angle)
        
        end_x = center[0] + (center_radius + petal_height) * math.cos(angle)
        end_y = center[1] + (center_radius + petal_height) * math.sin(angle)
        
        # Use a rotated ellipse to draw the petal
        rect = pygame.Rect(0, 0, petal_height, petal_radius)
        rect.center = (start_x + (end_x - start_x) / 2, start_y + (end_y - start_y) / 2)
        #pygame.draw.ellipse(surface, petal_color, rect)
        draw_petal(surface, rect.center, petal_radius, petal_height, petal_color, angle, points_count, petal_shape) 


# Function: Sidebar and buttons
def draw_sidebar():
    # Draw the sidebar
    pygame.draw.rect(window, GRAY, sidebar)

    # Draw buttons
    for i, button in enumerate(sidebar_buttons):
        pygame.draw.rect(window, BLUE, button)
        pygame.draw.rect(window, BLACK, button, 3)  # Border of the button
        text = font.render(sidebar_button_labels[i], True, GRAY)
        text_rect = text.get_rect(center=button.center)
        window.blit(text, text_rect)
        
    for dirt in dirts:
        window.blit(dirt_image, dirt.topleft)

def handle_button_click(pos):
    if sidebar_buttons[0].collidepoint(pos):
        for i in range(5):
            # Flower Properties
            center_radius = random.randint(10, 50)
            petal_radius = random.randint(10, 50)
            petal_height = petal_radius
            num_petals = random.randint(4, 10)  # Number of petals
            petal_distance = 100  # Distance from the center to each petal
            center_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            petal_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            points_count = 50
            petal_shape = random.uniform(0,4)
            random_x = 100*i+300
            random_y = random.randint(0, HEIGHT-100)
            draw_circle_with_petals(window, (random_x, random_y), center_radius, petal_radius, num_petals, petal_distance, center_color, petal_color, petal_height, points_count, petal_shape)

    if sidebar_buttons[2].collidepoint(pos):
        window.fill(WHITE)  # Clear the screen with a white color
    for i, dirt in enumerate(dirts):
        if dirt.collidepoint(pos):
            print(f"Dirt {i + 1} clicked!")

# Main game loop
running = True
window.fill(WHITE)  # Clear the screen with a white color
while running:
    draw_sidebar()  # Draw the sidebar and buttons
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse click
                handle_button_click(event.pos)
    pygame.display.update()  # Update the screen

# Quit Pygame
pygame.quit()
sys.exit()

class Dimensions:
    """This class uses the desired window dimensions to layout the overall design.
        Attributes:
            window = tuple containing the lower left coordinates, width, and height of window
            width = window width
            height = window height
            cnv = canvas, as above
            lbar_nav = navigation window, as above
            lbar_logo = logo image, as above
            lbar_gene = genes, as above
            lbar_ttl = title, as above
        Methods:                 
            layoutPlots: Dictionary of plots containing the plot name and x,y location.
        TODO:
            Write out a layout for the rest of the frames"""
    def __init__(self, width=1000): #Justified to lower left 
        ratios={}
        for i in range(1, 8): ratios["gr"+str(i)] = width*0.618**i
        self.window =    0, 0,        width, ratios["gr1"]
        self.width = self.window[2] 
        self.height = self.window[3]
        self.cnv =       ratios["gr2"], self.height, ratios["gr1"], ratios["gr1"]
        self.lbar_nav =  0, 2*ratios["gr5"]+ratios["gr4"],ratios["gr2"], ratios["gr2"]
        self.lbar_logo = 0,0,ratios["gr4"], ratios["gr5"] #-ratios["gr2"]+ratios["gr4"]
        self.lbar_gene = 0, ratios["gr5"],ratios["gr2"],ratios["gr5"]
        self.lbar_ttl =  ratios["gr4"],0, ratios["gr3"], ratios["gr5"]      #-ratios["gr2"]+ratios["gr4"]
    def layoutAll(self):
        pass
    def layoutPlots(self): #Assumes center justified               
        plots = {"A":[], "B":[], "C":[], "D":[], "E":[]}
        n=1  #intentionally not starting at 0
        for l in plots:
                plotx = round(n*self.cnv[2]/(len(plots)+2)) 
                plots[l]= plotx, 0
                n+=1
        return plots
    
class Seed:
    """This class makes an arbitrary seed
        Methods:
            __init__: Genome imported from the default seed
            importSeed: Genome imported from external seed
            randomSeed: Genome generated randomly
            selfSeed: Genome created from previous with slight variation. Number of variations controlled by self.heri.
        Attributes:
            location: tells me 'where' the seed is. Options are a plot or as a saved seed.
            genome:dictionaries defining the key parameters used for illustrating the plant.
            phenome: parameters used for introducing randomness when creating the plant, and
            herit: parameters used for controlling mixing of parameters of multiple plants.
            parent1: record of previous parent, to be used in lineage tracing later.
            parent2: record of previous parent, to be used in lineage tracing later

        TODO:
            Move the list of parameters to a text doc I can call, one for each named seed variety?
            Can then rewrite so searches for given name, easier to let user save additional named flowers.
            Could also then have limits parameters independent of the genome/phenome
            phenome will eventually introduce randomness even in cloned flowers (angle of growth, height)
            herit contains controls on how genome is modified later
            Work on crispr & clone
            """
    def __init__(self):
        self.genome = {"flower_num":5,
                   "petal_num":4, "petal_rad":80.0, "petal_xFact":2, "petal_line": "#b5e3af", "petal_fill":"#D773A2", "petal_linewid":2.0, "petal_coeff":6,
                   "center_line":"#b2b2ff", "center_fill":"#72c6ff", "center_linewid":1.0,"center_rad":5.0, "center_stipple":"",
                   "layer_num":1, "layer_coeff":2.0,
                   "stemcolor":"#ABCDEF", "stem_thickness":1, "stem_length":200, "stem_angle":np.pi/6,
                   "branch_alt":True}
        self.phenome = {"height":0} #Filling out as needed
        self.heri = {"color":1, "selfing":1} #Filling out as needed
        self.limits = {"petal_num":3,
                       #"petal_rad": 5*(self.genome["center_rad"] + self.genome["center_linewid"]), "petal_xFact":100,
                       #"center_rad": round(self.genome["petal_rad"]/10),
                       "layer_num":0}                
    def importSeed(self, flowername):
        fn = str(flowername) + ".txt"
        with open(fn, "rt") as file:
            flowergenome = pickle.load(fn)
        self.genome = flowergenome 
    def randomSeed(self):
        for key, value in self.genome.items():
            newval = radiationTool(key, value)
            self.genome[key]=newval
        repairTool(self.genome, self.limits)
        self.parent1 = ""
        self.parent2 = ""
    def selfSeed(self):
        for i in range(0, self.heri["selfing"]):
            key, value = random.choice(list(self.genome.items())) #Add a way to have a chance of no change.
            newval = radiationTool(key, value)
            self.genome[key] = newval
        self.parent1 = self #This doesn't seem like it would work. Ask for advice.
        self.parent2 = self
    def breedSeed(self, secondSeed):
        newgenome = []
        for key, value in self.genome.items():
            for geneP1, geneP2 in zip(value, secondSeed.genome[key]) :
                if isinstance(geneP1, int):
                    newval = random.choice(geneP1, geneP2, round((geneP1 + geneP2)/2), random.gauss(mean(geneP1, geneP2)))
                elif isinstance(geneP1, float):
                    newval = random.weibullvariate(round((geneP1 + geneP2)/2), 1)
                    newval = float(abs(newval))
                elif isinstance(geneP1, bool):
                    newval = random.randchoice(geneP1, geneP2)
                else:
                    newval = [create_Colors(start=gene1[1:]+gene2[1:])]
            newgenome[key]=newval
        self.genome = newgenome
        self.parent1 = self
        self.parent2 = secondSeed
    def crisprSeed(self):
        pass
    def cloneSeed(self):
        self.parent1 = self #This doesn't seem like it would work
        self.parent2 = self

class Plant():
    """This class makes an arbitrary seed
        Methods:
            __init__: sets location of the flower
            create_Circle: Draws flower center
            create_Petals: Draws the petals
            create_Flowers: Uses Circle and petals
            create_Nodes: Creates segments within a stem for placement of flowers, additionals stems
            create_Stems: Draws the full stem, interconnecting the nodes
        Attributes:
            location: Should be a plot"""
    def __init__(self, seed, dimensions, canvas):
        self.seed = seed
        self.dimensions = dimensions
        self.canvas = canvas
    def create_Circle(self, x, y, r, **kwargs):
            return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    def create_Petals(self, x, y, petal_num, radius, xFactor, coefficent, **kwargs):
            points = []
            for degrees in range(0, 360-xFactor):
                    radians = math.radians(degrees)
                    distance = math.sin(radians * petal_num) * radius
                    points.append(x+math.cos(coefficent*radians) * distance)
                    points.append(y+math.sin(coefficent*radians) * distance)
            return self.canvas.create_polygon(points,smooth=0, **kwargs)
    def create_Flowers(self, bud_x, bud_y, genes):
            for l in range(genes["layer_num"]):
                    self.create_Petals(bud_x, bud_y, 
                                            petal_num=genes["petal_num"], radius=genes["petal_rad"], xFactor=genes["petal_xFact"], coefficent=genes["petal_coeff"],  
                                            fill=genes["petal_fill"], outline=genes["petal_line"], width=genes["petal_linewid"])
                    self.create_Circle(bud_x, bud_y, r=genes["center_rad"],
                                    fill=genes["center_fill"], outline=genes["center_line"], 
                                    width=genes["center_linewid"])                    
    def create_Nodes(self, x1, y1, angle, length):
        y2 = y1 - length #make use of gene.length
        x2 = angle*(y1-y2)+x1 #make use of gene.angle
        yr = random.weibullvariate(round((y1 + y2)/2), 1) #make use of gene.specialsauce and randomness
        xr = random.weibullvariate(round((y1 + y2)/2), 1)
        nodes = list(x1, y1, xr, yr, x2, y2)
        return nodes

    def create_Stems(self, base_x, base_y, genes):
            phen_angle = 0 
            phen_length = random.uniform(0.1*base_y, 0.9*base_y) #genes["stem_length"]
            mainstem = self.create_Nodes(base_x, base_y, genes["flower_num"], phen_angle, phen_length)
            delta = 2
            #print("mainstem: ", mainstem, "\n phen_angle", phen_angle, delta, "\nBase", base_x, base_y)
            self.canvas.create_line(base_x, base_y, mainstem,
                             fill=genes["stemcolor"], width=genes["stem_thickness"], smooth=True)
            x1 = mainstem[0][0]
            y1 = mainstem[0][1]
 
            if genes["branch_alt"]==False:
                step = 1
            else:
                start = 1
                step = 2

            phen_angle+=delta
            phen_length = phen_length*0.1
            
            for node in mainstem[1:len(mainstem):step]:
                use_length = phen_length #make gene
                use_length -= phen_length*0.5 
                x1 = node[0]; y1 = node[1]
                branch = self.create_Nodes(x1, y1, genes["flower_num"], phen_angle, use_length)
                self.canvas.create_line(x1, y1, branch,
                             fill=genes["stemcolor"], width=genes["stem_thickness"], smooth=False)
                x1 = branch[0][0]
                y1 = branch[0][1]
                self.create_Flowers(x1, y1, genes)            
                
            for node in mainstem[start:len(mainstem):step]:
                use_length = phen_length #make gene
                use_length -= phen_length*0.5
                x1 = node[0]
                y1 = node[1]
                branch = self.create_Nodes(x1, y1, 3, -phen_angle, use_length) 
                self.canvas.create_line(node,branch,
                          fill=genes["stemcolor"], width=genes["stem_thickness"], smooth=False)
                x1 = branch[0][0]
                y1 = branch[0][1]
                self.create_Flowers(x1, y1, genes)
            x1 = mainstem[0][0]
            y1 = mainstem[0][1]
            self.create_Flowers(x1, y1, genes)

            
'''In the process of rewriting the 'nodes' element:
Currently Line A is drawn between the base point and a number of nodes equal to the flower number. The nodes are a random point between the base and every bud. Eg, a one bud flower will have one node between the base and bud. (???).
Currently Line B is drawn between the random node points and each bud at that location.
Line A should be drawn between the base point and the primary bud location. Only the first bud location is assigned by garden.
Line B should be drawn between nodes along the length of Line A and a given Bud (generated as part of stem creation)
Eventually all phen variations will be an easy pass, not repeated in code
'''

'''    def create_Branches(): #write this first, then come back to fix nodes
        if genes["centralized"]==True
            #next nodes radiate out from x2 y2.
            #Needed Varaibles = length, max angle, number of nodes (will change current use case)
        elif genes["alternating"]==True
            #Next nodes are spaced alternately along the length of the first line
            
        else
'''
                    


class Garden():
    """This class makes the garden background and buttons for the canvas
        Methods:
            __init__: sets location of the flower
            create_Dirt: Draws the buttons that flowers grow 'from'
            create_Background: Draws the background
            create_Planting: Places a plant in a plot
            create_EmptyGarden: Draws just the background
            create_FullGarden: Draws the background and puts plants in all plots
        Attributes:
        TODO:
            Create other background options
            """
    def __init__(self, dimensions, canvas):
        self.dimensions = dimensions
        self.canvas = canvas        
    def create_Dirt(self, base_x, base_y):
            image=Image.open('./dirt4.png')
            img=image.resize((80, 40))
            dirt = ImageTk.PhotoImage(img)       
            dirtbutton=tk.Button(canvas, image=dirt, bg='#d0e0e3', fg=None, bd=0)
            dirtbutton.place(x= base_x, y=base_y-40)
            dirt.image = dirt #Cannot delete because of garbage garbaging
    def create_Background(self):
        pass
            #bg = ImageTk.PhotoImage(file = "./flowerbg_2.png")
            #canvas.create_image(0,0, image = bg,  anchor=tk.NW)
            #bg.image = bg #Cannot delete because of garbage garbaging
    def grow_EmptyGarden(self): 
            canvas.delete('all')
            self.create_Background()
            plots = self.dimensions.layoutPlots() #Dimensions.layoutPlots(self.dimensions)
            for plot in plots:
                    base_x = plots[plot][0]
                    base_y = plots[plot][1]
                    self.create_Dirt(base_x, base_y)                    
    def grow_FullGarden(self): 
            canvas.delete('all')
            self.create_Background()
            plots = self.dimensions.layoutPlots()
            for plot in plots:
                    print("Plot Number", plot)
                    try:
                            seed = Seed()
                            newplant = Plant(seed.randomSeed(), self.dimensions, self.canvas)
                    except:
                            newplant = Plant(seed, self.dimensions, self.canvas) #Figure out when except actually triggered
                    base_x = plots[plot][0]
                    base_y = dimensions.height - plots[plot][1]
                    #bud_x = [random.triangular(base_x-(self.dimensions.cnv[2]/7),base_x+(self.dimensions.cnv[2]/7), base_x) for i in range(0, seed.genome["flower_num"]) ]
                    #bud_y = [random.triangular(self.dimensions.cnv[3]-(self.dimensions.cnv[3]/7),0+(self.dimensions.cnv[3]/7),0+(2*self.dimensions.cnv[3]/7)) for i in range(0, seed.genome["flower_num"]) ]
#                   print(type(base_x));print(type(base_y));print(type(bud_x));print(type(bud_y))
                    newplant.create_Stems(base_x, base_y, seed.genome)
                    '''for i in range(seed.genome["flower_num"]):
                            newplant.create_Flowers(bud_x[i], bud_y[i], seed.genome)'''
                    self.create_Dirt(base_x, base_y)

def radiationTool(key, value):
    """Thus function randomizes the gene it is given
        Parameters:
            key: a given gene name
            value: the value for that gene parameter
        Outputs
            The updated new value"""
    if isinstance(value, int):
        newval=random.weibullvariate(value, 1)
        newval=math.ceil(newval)
        newval=int(abs(newval))
    elif isinstance(value, float):
        newval=random.weibullvariate(value, 1)
        newval=float(abs(newval))
    elif isinstance(value, bool):
        newval=random.randchoice(True, False)
    elif isinstance(value, str): 
        newval=[create_Colors()]        
    return newval

def repairTool(genome, limits):
    """This function sets limits on the gene it is given
        Parameters:
            genome: a given gene name
            limits: the value for that gene parameter
        Outputs
            The updated genome"""
    while genome["petal_num"]<limits["petal_num"]:
        genome["petal_num"] += random.randint(1, 5)
    while genome["petal_rad"] <= limits["petal_rad"] and dimensions.cnv[2]*0.5 and dimensions.cnv[3]*0.5:
        genome["petal_rad"] += random.randint(1, 12)
    while genome["petal_xFact"] > limits["petal_xFact"]: 
        genome["petal_xFact"]-= random.randint(1, 30)
    while genome["center_rad"] < limits["center_rad"]:
        genome["center_rad"]+= random.randint(1, 40)
    while genome["layer_num"] <=limits["layer_num"]:
        genome["layer_num"]+= random.randint(1, 2)
    genome["stemcolor"]=make_Green(genome["stemcolor"])
    genome["center_rad"]=limits["center_rad"] #Why did I go with such a strict option?
    return genome

#def crisprTool(genome, key, guide):

def create_Colors(start='#FFFFFF', herit=10):
        """Randomly create a new hex style number or update an old one proportional to heritability. If no inital hex given, a completely random color is provided.
        Parameters:
                start: initial value for hex. Default is white.
                herit: Number of replacements. Default is 10.
        Returns:
                rand_colors: a string of a hex color
        """
        t=0; rand_colors=start
        while t<herit:
                rand_colors = rand_colors.replace(random.choice(rand_colors[1:]), random.choice('0123456789ABCDEF'), 1) #rand_colors = "#"+''.join([random.choice(start) for i in range(6)])
                t+=1                 
        return rand_colors

def make_NotHex(l):
        """Convert hex letter into two digit RGB numbers
        Parameters:
                l: letters or numbers 
        Returns:
                int(l):an integer representing the value of the initial input
        """
        hex={"A":10,"B":11,"C":12,"D":13,"E":14,"F":15}
        if l in hex.keys():
                if DEBUG_L2 == True: print("replaced ", l, " with: ", hex[l])
                l = hex[l]
        return int(l)

def check_Green(color):
        """Check if a hex color is green or not
        Parameters:
                color: initial value for hex.
        Returns:
                Bool: True if is green
        """   
        if DEBUG_L2 == True: print("Now Running: check_Green.\n", "stemcolor: ", color, "\nlength: ", len(color)) 
        rr = make_NotHex(color[1])*16 + make_NotHex(color[2]) #Convert letters and numbers from hex to rgb. Leave out hex.
        gg = make_NotHex(color[3])*16 + make_NotHex(color[4])
        bb = make_NotHex(color[5])*16 + make_NotHex(color[6])
        if gg>rr and gg>bb:
                return True
        else:
                return False        

def make_Green(color):
        """Generate random hex colors until a green color is returned
        Parameters:
                color: initial value for hex.
        Returns:
                color: final value for hex, now green
        """
        if DEBUG_L2 == True: print("Now Running: make_Green.")
        result = check_Green(color)
        if DEBUG_L2 == True: print("is", color," green?: ", result)
        while result is False:
                color=create_Colors(color)
                result = check_Green(color)
                if DEBUG_L2 == True: print("Updated: is ", color, " green?: ", result)
        return color  
        
if __name__ == '__main__':
        hl_debug=0
        if DEBUG == True: hl_debug=2
        
        #Create Frames & Layout
        dimensions = Dimensions(width=1000)

        frame_lbar = tk.Frame(root, highlightthickness=hl_debug, bg="yellow", width=dimensions.lbar_nav[2], height=dimensions.cnv[3])
        frame_rbar = tk.Frame(root, highlightthickness=hl_debug, width=dimensions.cnv[2], height=dimensions.cnv[3])
        frame_lbar.pack(side=tk.LEFT, pady=5, padx=2.5, fill=tk.BOTH)
        frame_rbar.pack(side=tk.RIGHT, pady=5, padx=2.5, fill=tk.BOTH) 

        frame_lbar_top = tk.Frame(frame_lbar)
        frame_lbar_top.pack(side=tk.TOP, fill=tk.BOTH)
        frame_lbar_logo = tk.Frame(frame_lbar_top, highlightthickness=hl_debug, width=dimensions.lbar_logo[2], height=dimensions.lbar_logo[3])
        frame_lbar_ttl = tk.Frame(frame_lbar_top, highlightthickness=hl_debug, width=dimensions.lbar_ttl[2], height=dimensions.lbar_ttl[3])
        frame_lbar_logo.pack(side=tk.LEFT, fill=tk.BOTH) 
        frame_lbar_ttl.pack(side=tk.RIGHT, fill=tk.BOTH)       
        frame_lbar_gene = tk.Frame(frame_lbar, highlightthickness=hl_debug, width=dimensions.lbar_gene[2], height=dimensions.lbar_gene[3])
        frame_lbar_gene.pack(fill=tk.BOTH)
        frame_lbar_bot = tk.Frame(frame_lbar, highlightthickness=1, bg="green", width=dimensions.lbar_nav[2], height=dimensions.lbar_nav[3])
        frame_lbar_bot.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        frame_lbar_nav_l = tk.Frame(frame_lbar_bot, width=dimensions.lbar_nav[2]/2)
        frame_lbar_nav_l.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame_lbar_nav_r = tk.Frame(frame_lbar_bot, width=dimensions.lbar_nav[2]/2)
        frame_lbar_nav_r.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        frame_lbar_nav_l_1=tk.Frame(frame_lbar_nav_l, height=dimensions.lbar_nav[3])
        frame_lbar_nav_l_2=tk.Frame(frame_lbar_nav_l, height=dimensions.lbar_nav[3])
        frame_lbar_nav_l_3=tk.Frame(frame_lbar_nav_l, height=dimensions.lbar_nav[3])
        frame_lbar_nav_r_1=tk.Frame(frame_lbar_nav_r, height=dimensions.lbar_nav[3])
        frame_lbar_nav_r_2=tk.Frame(frame_lbar_nav_r, height=dimensions.lbar_nav[3])
        frame_lbar_nav_r_3=tk.Frame(frame_lbar_nav_r, height=dimensions.lbar_nav[3])
        frame_lbar_nav_l_1.pack(side=tk.TOP, fill=tk.BOTH, expand=True); frame_lbar_nav_r_1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        frame_lbar_nav_l_2.pack(fill=tk.BOTH, expand=True); frame_lbar_nav_r_2.pack(fill=tk.BOTH, expand=True)
        frame_lbar_nav_l_3.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True); frame_lbar_nav_r_3.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        #Place Widgets within Frames & Define Buttons
        canvas = tk.Canvas(frame_rbar, width = dimensions.cnv[2], height = dimensions.cnv[3], bg='#d0e0e3');         canvas.pack(fill=tk.BOTH)
        MyGarden = Garden(dimensions, canvas)

        title = tk.Label(frame_lbar_ttl, text="***SEED***", font=("bold", 20));         title.pack()
        logo = tk.Label(frame_lbar_logo, text="***LOGO***", font=("bold", 20));         logo.pack()
        
        userinput_genes = tk.Entry(frame_lbar_gene, width=50);                         userinput_genes.pack(padx=10, pady=10, side = tk.LEFT, fill=tk.X)
        submit_button = tk.Button(frame_lbar_gene, text = "Submit");         submit_button.pack(pady=10, side = tk.RIGHT)
        
        plant_button = tk.Button(frame_lbar_nav_l_1, text = "ALL NEW",
                                 command = MyGarden.grow_FullGarden);         plant_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        weed_button = tk.Button(frame_lbar_nav_l_2,  text = "[REMOVE]");      weed_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        mix_button = tk.Button(frame_lbar_nav_l_3, text = "[BREED]");         mix_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self_button = tk.Button(frame_lbar_nav_r_1, text = "[SELF]");         self_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        save_button = tk.Button(frame_lbar_nav_r_2, text = "[SAVE]");         save_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        till_button = tk.Button(frame_lbar_nav_r_3, text = "CLEAR ALL",
                                 command = MyGarden.grow_EmptyGarden);        till_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        #Create Plots and Grow Initial Plants from Scratch
        MyGarden.grow_FullGarden()          
        root.mainloop()


'''def draw_petal(surface, center, radius, height, color, points_count):
    cx, cy = center
    tip_x, tip_y = cx, cy + height

    # Generate the top circular arc
    arc_points = []
    for i in range(points_count + 1):
        angle = math.pi + (math.pi * i / points_count)  # From 180° to 360°
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        arc_points.append((x, y))

    # Add the tip of the petal
    arc_points.append((tip_x, tip_y))

    # Complete the petal by closing the shape
    pygame.draw.polygon(surface, color, arc_points)
'''
