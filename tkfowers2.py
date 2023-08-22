#TODO
        #Convert each petal to an image, create ability to overlay petals, change alpha, sat, and brightness, and change location for creation of extra petals. 
        #https://www.tutorialspoint.com/how-can-i-vary-a-shape-s-alpha-with-tkinter
        #Set up heritability/Epigenetics
        #Grow multiple branches (that look nice)
        #Rewrite plots for indive flowers
        #Rerite as Classes
        

import tkinter as tk
from PIL import Image,ImageTk
import random
import math
from statistics import mean

#Set Display Variables
WIDTH, HEIGHT = 1400, 650 #tk.winfo_screenwidth(), tk.winfo_screenheight()
root = tk.Tk()
root.geometry("1400x650") #write as concatenate

#Set DEBUG
DEBUG=False #False 
DEBUG_L2=False

def _seed_DefaultPlant():
        """Sets the default parameter information for an arbitrary plant.
        Parameters:
                NULL
        Returns:
                dict:dictionaries defining the key parameters including genes: parameters used for illustrating the plant, epig: parameters used for introducing randomness when creating the plant, and herit: parameters used for controlling mixing of parameters of multiple plants.
        """
        
        GENES={"flower_num":5,
               "petal_num":4, "petal_rad":80.0, "petal_xFact":2, "petal_line": "#b5e3af", "petal_fill":"#D773A2", "petal_linewid":2.0, "petal_coeff":6,
               "center_line":"#b2b2ff", "center_fill":"#72c6ff", "center_linewid":1.0,"center_rad":5.0, "center_stipple":"",
               "layer_num":1, "layer_coeff":2.0,
               "stemcolor":"#ABCDEF", "thickness":10
               }        
        
        #Set Default Heritability (not yet used)
        HERIT={"color":1 }

        #Set Default Epigenetics (not yet used)
        EPIGE={}

        return {"genes":GENES, "herit":HERIT, "epige":EPIGE}

def _seed_RandomPlant():
        """Randomly creates new parameter information for any given plant.
        Parameters:
                NULL
        Returns:
                genes:dictionaries defining the key parameters used for illustrating the plant.
        TODO:
                Will eventually include epig: parameters used for introducing randomness when creating the plant, and herit: parameters used for controlling mixing of parameters of multiple plants.
        """

        genes = _seed_DefaultPlant()["genes"]
        for key, value in genes.items():
                if isinstance(value, int):
                        newval=random.weibullvariate(value, 1)
                        newval=math.ceil(newval)
                        newval=int(abs(newval))
                        genes.update({key:newval})
                elif isinstance(value, float):
                        newval=random.weibullvariate(value, 1)
                        newval=float(abs(newval))
                        genes.update({key:newval})
                elif isinstance(value, bool):
                        newval=random.randchoice(True, False)
                        genes.update({key:newval})
                elif isinstance(value, str): 
                        newval=[create_Colors()]        
                        genes.update({key:newval})      
        genes = create_Reason(genes)
        return genes

def _seed_SelfedPlant(genes):
        """Randomly changes parameter information for a provided plant.
        Parameters:
                genes:dictionaries defining the key parameters used for illustrating the plant.
        Returns:
                genes:dictionaries defining the key parameters used for illustrating the plant.
        TODO:
                Will eventually include epig: parameters used for introducing randomness when creating the plant, and herit: parameters used for controlling mixing of parameters of multiple plants.
        """

        for key, value in genes.items():
                if isinstance(value, int):
                        newval=random.weibullvariate(value, value*heritability)
                        newval=round(newval)
                        newval=int(newval)
                        genes[key]=newval
                elif isinstance(value, float):
                        newval=random.weibullvariate(value, value*heritability)
                        genes[key]=newval
                elif isinstance(value, boolean):
                        genes[key]=random.randchoice(True, False)
                elif isinstance(value, string): 
                        genes[key]=[create_Colors(start=value[1:])]
        return genes

def _seed_BredPlant(genes1, genes2):
        """Randomly changes parameter information based on two provided plants.
        Parameters:
                genes1:dictionaries defining the key parameters used for illustrating the plant.
                genes2:dictionaries defining the key parameters used for illustrating the plant.
        Returns:
                genes:dictionaries defining the key parameters used for illustrating the plant.
        TODO:
                Will eventually include epig: parameters used for introducing randomness when creating the plant, and herit: parameters used for controlling mixing of parameters of multiple plants.
        """

        gene=dict()
        for gene1, gene2 in zip(genes1.values(), genes2.values()) :
                if isinstance(gene, int):
                        gene=random.choice(gene1, gene2, mean(gene1, gene2), random.gauss(mean(gene1, gene2)))
                else:
                        gene=[create_Colors(start=gene1[1:]+gene2[1:])]
        return genes


def create_Plots():
        """Randomly changes parameter information based on two provided plants.
        Parameters:
                NULL
        Returns:
                plots: dictionary of plots containing the plot name and x,y location.
        """
        plots = {"A":[], "B":[], "C":[], "D":[], "E":[]}
        n=1  #intentionally not starting at 0
        for l in plots:
                plot_w = round(n*WIDTH/(len(plots)+2))
                plots[l]=(plot_w), HEIGHT
                n+=1                
        return plots

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

def linspace(start, stop, n):
    if n == 1:
        yield stop
        return
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i

def create_Reason(genes):
        while genes["petal_num"]<3:
                genes["petal_num"] += random.randint(1, 5)
        while genes["petal_rad"] <= 5*(genes["center_rad"] + genes["center_linewid"]):
                genes["petal_rad"] += random.randint(1, 12)
        while genes["petal_xFact"]>100: 
                genes["petal_xFact"]-= random.randint(1, 30)
        while genes["center_rad"] < 2*genes["center_linewid"]:
                genes["center_rad"]+= random.randint(1, 40)
        while genes["layer_num"] <=0:
                genes["layer_num"]+= random.randint(1, 2)
        genes["stemcolor"]=make_Green(genes["stemcolor"][0])
        genes["center_rad"]=round(genes["petal_rad"]/10)
        return genes

def _create_Circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_Circle = _create_Circle

def _create_Petals(self, x, y, petal_num, radius, xFactor, coefficent, **kwargs):
        points = []
        for degrees in range(0, 360-xFactor):
                radians = math.radians(degrees)
                distance = math.sin(radians * petal_num) * radius
                points.append(x+math.cos(coefficent*radians) * distance)
                points.append(y+math.sin(coefficent*radians) * distance)
        return self.create_polygon(points,smooth=0, **kwargs)
tk.Canvas.create_Petals = _create_Petals

def create_Nodes(x1, y1, x2, y2, var = 5):
        node = [random.triangular(round(x1-(WIDTH/7)), round(x2+(WIDTH/7)), (x1+x2)/2),
                 (y1+y2)/2]
        return node

def _create_Flowers(self, bud_x, bud_y, genes):
        for l in range(genes["layer_num"]):
                self.create_Petals(bud_x, bud_y, 
                                        petal_num=genes["petal_num"], radius=genes["petal_rad"], xFactor=genes["petal_xFact"], coefficent=genes["petal_coeff"],  
                                        fill=genes["petal_fill"], outline=genes["petal_line"], width=genes["petal_linewid"])
                self.create_Circle(bud_x, bud_y, r=genes["center_rad"],
                                fill=genes["center_fill"], outline=genes["center_line"], 
                                width=genes["center_linewid"]) # stipple=genes["center_stipple"]
tk.Canvas.create_Flowers = _create_Flowers

def _create_Stems(self, bud_x, bud_y, base_x, base_y, genes): #add herit and var
        nodes = []        
        for node in range(0, genes["flower_num"]):
                nodes+=[create_Nodes(bud_x[node], bud_y[node], base_x, base_y)]
        def myfunc(e):
                return e[0]
        nodes.sort(key=myfunc)
        
        if DEBUG_L2 == True: print("Nodes", nodes)
        self.create_line(base_x, base_y, nodes, #bud_x[0], bud_y[0],
                         fill=genes["stemcolor"], width=genes["thickness"], smooth=False)
        for node in range(0, genes["flower_num"]):
                self.create_line(nodes[node], bud_x[node], bud_y[node],
                         fill=genes["stemcolor"], width=genes["thickness"], smooth=False)
tk.Canvas.create_Stems = _create_Stems

def _create_Dirt(self, base_x, base_y):
        image=Image.open('./dirt4.png')
        img=image.resize((80, 40))
        dirt = ImageTk.PhotoImage(img)       
        dirtbutton=tk.Button(canvas, image=dirt)
        dirtbutton.place(x= base_x-25, y=base_y-110)
        dirt.image = dirt #Cannot delete because of garbage garbaging
tk.Canvas.create_Dirt = _create_Dirt      

def _grow_Background(self):
        bg = ImageTk.PhotoImage(file = "./flowerbg_2.png") #TODO: Create other background options
        canvas.create_image(0,0,image = bg, anchor=tk.NW)
        bg.image = bg #Cannot delete because of garbage garbaging
tk.Canvas.grow_Background = _grow_Background

def _grow_EmptyGarden(self): #Create Plots and Grow Plants
        canvas.delete('all')
        canvas.grow_Background()
        plots=create_Plots()
        for plot in plots:
                base_x = plots[plot][0]
                base_y = plots[plot][1]
                canvas.create_Dirt(base_x, base_y)

tk.Canvas.grow_EmptyGarden = _grow_EmptyGarden

def _grow_FullGarden(self): #Create Plots and Grow Plants
        canvas.delete('all')
        canvas.grow_Background()
        plots=create_Plots()
        for plot in plots:
                try:
                        genes = _seed_RandomPlant()
                except:
                        genes = _seed_DefaultPlant()["genes"]
                base_x = plots[plot][0]
                base_y = plots[plot][1]
                bud_x = [random.triangular(base_x-(WIDTH/7),base_x+(WIDTH/7), base_x) for i in range(genes["flower_num"]) ]
                bud_y = [random.triangular(HEIGHT-(HEIGHT/7),0+(HEIGHT/7),0+(2*HEIGHT/7)) for i in range(genes["flower_num"]) ]
                canvas.create_Stems(bud_x, bud_y, base_x, base_y, genes)
                for i in range(genes["flower_num"]):
                        canvas.create_Flowers(bud_x[i], bud_y[i], genes)
                canvas.create_Dirt(base_x, base_y)
tk.Canvas.grow_FullGarden = _grow_FullGarden

def _grow_SingleFlower(self):
        if DEBUG == True: hl_debug=2
        

def button_disambig():
        if DEBUG == True: hl_debug=2
        

if __name__ == '__main__':
        hl_debug=0
        if DEBUG == True: hl_debug=2
        
        #Create Frame Layout
        frame_top = tk.Frame(root, highlightthickness=hl_debug, width=WIDTH-100)
        frame_top.place(x=10, y=4)
        frame_left = tk.Frame(root, highlightthickness=hl_debug)
        frame_left.place(x=10, y=50)
        frame_right = tk.Frame(root, highlightthickness=hl_debug)
        frame_right.place(x=WIDTH-90, y=50)

        #Place Widgets within Frames & Define Buttons
        canvas = tk.Canvas(frame_left, width = WIDTH-110, height = HEIGHT-60, bg='white') 
        canvas.pack()
        title = tk.Label(frame_top,
                         text="***SEED***", font=("bold", 20))
        title.pack(side=tk.LEFT)
        submit_button = tk.Button(frame_top,
                       text = "Submit")
        submit_button.pack(side = tk.RIGHT)
        userinput_genes = tk.Entry(frame_top,
                             width = 50)
        userinput_genes.pack(padx=10, side = tk.RIGHT)

        subtitle = tk.Label(frame_right,
                         text="GARDEN!")
        subtitle.pack(pady=10)

        plant_button = tk.Button(frame_right, width=10, text = "ALL NEW",
                                 command = canvas.grow_FullGarden)
        plant_button.pack(pady=5)
        weed_button = tk.Button(frame_right,
                       width=10, text = "[REMOVE]")
        weed_button.pack(pady=5)
        mix_button = tk.Button(frame_right,
                       width=10, text = "[BREED]")
        mix_button.pack(pady=5)
        self_button = tk.Button(frame_right,
                       width=10, text = "[SELF]")
        self_button.pack(pady=5)
        save_button = tk.Button(frame_right,
                       width=10, text = "[SAVE]")
        save_button.pack(pady=5)

        till_button = tk.Button(frame_right, width=10, text = "CLEAR ALL",
                                 command = canvas.grow_EmptyGarden)
        till_button.pack(pady=5)

        #Create Plots and Grow Initial Plants from Scratch
        canvas.grow_FullGarden()          
        root.mainloop()


