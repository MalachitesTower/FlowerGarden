import tkinter as tk
root = tk.Tk()
root.geometry("300x150")
  
w = tk.Label(root, text ='GeeksForGeeks', font = "50") 
w.pack()
  
frame = tk.Frame(root, highlightbackground="red", highlightthickness=2, bg="red")
frame.pack(padx=20, pady=20)
  
bottomframe = tk.Frame(root, highlightbackground="blue", highlightthickness=2, bg="light blue")
bottomframe.pack( padx=20, pady=20, side = tk.BOTTOM )
  
b1_button = tk.Button(frame, text ="Geeks1", fg ="red")
b1_button.pack( side = tk.LEFT)
  
b2_button = tk.Button(frame, text ="Geeks2", fg ="brown")
b2_button.pack( side = tk.LEFT )
  
b3_button = tk.Button(frame, text ="Geeks3", fg ="blue")
b3_button.pack( side = tk.LEFT )
  
b4_button = tk.Button(bottomframe, text ="Geeks4", fg ="green")
b4_button.pack( side = tk.LEFT)
  
b5_button = tk.Button(bottomframe, text ="Geeks5", fg ="green")
b5_button.pack( side = tk.LEFT)
  
b6_button = tk.Button(bottomframe, text ="Geeks6", fg ="green")
b6_button.pack( side = tk.LEFT)
  
root.mainloop()
