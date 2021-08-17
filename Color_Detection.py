import PIL
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import Image,ImageTk
import tkinter as tk
import cv2
import pandas as pd



def try_login():               # this my login function  
    if name_entry.get()==default_name and password_entry.get() == default_password:
       messagebox.showinfo("LOGIN SUCCESSFULLY","WELCOME")
       log.destroy()
    else:
       messagebox.showwarning("login failed","Please try again" )
       log.mainloop()


default_name=("user")      #DEFAULT LOGIN ENTRY
default_password=("py36")


log=Tk()                   #this login ui
log.title("Tone Grabber-LOGIN")
log.geometry("400x400+400+200")
log.resizable(width=FALSE,height=FALSE)


LABEL_1 = Label(log,text="USER NAME")
LABEL_1.place(x=50,y=100)
LABEL_2 = Label(log,text="PASSWORD")
LABEL_2.place(x=50,y=150)

BUTTON_1=tk. Button(text="login",command=try_login)
BUTTON_1.place(x=50,y=200)
BUTTON_1=tk. Button(text="cancel",command=lambda:exit())
BUTTON_1.place(x=200,y=200)

name_entry=Entry(log,width=30)
name_entry.place(x=150,y=100)
password_entry=tk. Entry(log,width=30,show="*")
password_entry.place(x=150,y=150)

log. mainloop()                               


root=Tk()



#Paths of image anf csv file
csv_path='colors.csv'

#reading csv file
index=['color','color_name','hex','R','G','B']
df=pd.read_csv(csv_path,names=index,header=None)



#declaring global variables
clicked=False
r=g=b=xpos=ypos=0

#function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R,G,B):
	minimum = 1000
	for i in range(len(df)):
		d = abs(R-int(df.loc[i,'R']))+abs(G-int(df.loc[i,'G']))+abs(B-int(df.loc[i,'B']))
		if d <= minimum:
			minimum = d
			cname = df.loc[i,'color_name']
	return cname
          
        

def select_image():
    fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Select Image File",filetypes=(("JPG File","*.jpg"),("PNG File","*.png"),("All Files","*.*")))
    img=Image.open(fln)
    img=ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image=img
    Open_cv(fln)

def Open_cv(fln):
         cv2.namedWindow('image')
         def identify_color(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDBLCLK:
                global b, g, r, xpos, ypos, clicked
                clicked = True
                xpos = x
                ypos = y
                b, g, r = img[y,x]
                b = int(b)
                g = int(g)
                r = int(r)  
         img = cv2.imread(fln)
         img = cv2.resize(img,(800,600))
         cv2.setMouseCallback('image',identify_color)
         while(1):
                 cv2.imshow('image',img)
                 if clicked:
                         cv2.rectangle(img, (20,20), (600,60), (b,g,r), -1)
                         text = get_color_name(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
                         cv2.putText(img, text, (50,50), 2,0.8, (255,255,255),2,cv2.LINE_AA)
                         if r+g+b >=600:
                                 cv2.putText(img, text, (50,50), 2,0.8, (0,0,0),2,cv2.LINE_AA)
                 if cv2.waitKey(20) & 0xFF == 27:
                         break
         cv2.destroyAllWindows()



     
frm=Frame(root)
frm.pack(side=BOTTOM,padx=15,pady=15)

lbl=Label(root)
lbl.pack()

btn=Button(frm,text="Browse Image",command=select_image)
btn.pack(side=tk.LEFT)

btn2=Button(frm,text="Exit",command=lambda:exit(),bg="red")
btn2.pack(side=tk.LEFT,padx=5)

root.title("Tone Grabber")
root.geometry("300x350")
root.mainloop()
