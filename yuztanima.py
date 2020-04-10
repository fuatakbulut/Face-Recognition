# -*- coding: utf-8 -*-
import time

start = time.time()
import cv2
import face_recognition 
import numpy as np
import pickle
import time
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import ImageTk, Image
import threading


#from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#%%
gelenKisiler=[]
window = tk.Tk()
window.geometry("1080x640")
window.wm_title("Yuz tanima")




"""
# file dialog
def openFile():
    file_name = filedialog.askopenfilename(initialdir = "D:\codes\course", title = "select a file...")
    print(file_name)
    img_name = (file_name)
    
    
    img = Image.open(file_name)
    img = ImageTk.PhotoImage(img)
    
    label = tk.Label(window, image = img)
    label.image = img
    label.pack(padx = 15, pady = 15)
    """
#%%

def yuztanima():
    path="11.jpg"
    fotom=cv2.imread(path)
    window_name='Video'
    koordinat=(120,50)
    radius=20
    color=(255,0,0)
    thickness=2
    fotom = cv2.circle(fotom, koordinat, radius, color, thickness) 
    cap = cv2.VideoCapture(0)
    
    while True:
        
        ret, image_np = cap.read()
       
        with open('dataset_faces.dat', 'rb') as f:
            faces = pickle.load(f)
             
        faces_encoded = np.array(list(faces.values()))
        known_face_names = np.array(list(faces.keys()))
        #img = cv2.imread(image_np, 1) #im vardi
        img=image_np
        face_locations = face_recognition.face_locations(img) #yuzun yerini kutuluma, konum
        unknown_face_encodings = face_recognition.face_encodings(img, face_locations)
        face_names = []
        
        for face_encoding in unknown_face_encodings:
            matches = face_recognition.compare_faces(faces_encoded, face_encoding,tolerance=0.45) # yuz kodlamalarinin listesini, uyusup uyusmadiklarini gormek icin
            name = "Taninmiyor"
            giris="Giris Onaylandi"
            face_distances = face_recognition.face_distance(faces_encoded, face_encoding) # oklid mesafesi alinir
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                face_names.append(name)
                        
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                            # Draw a box around the face
                        cv2.rectangle(image_np, (left-20, top-20), (right+20, bottom+20), (255, 0, 0), 2)
                
                            # Draw a label with a name below the face
                        cv2.rectangle(image_np, (left-20, bottom -15), (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(image_np, name, (left -20, bottom +15), font, 1.0, (255, 255, 255), 2)
                        cv2.putText(image_np, giris, (left -20, bottom  -60), font, 1.0, (255, 255, 255), 2)
                        if name in gelenKisiler:
                             continue
                        else:
                            gelenKisiler.append(name)
                            

                            print(gelenKisiler)
            
            
                        
        cv2.imshow('Video', image_np)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
            
                

def KisileriGetir():
    
    
    sonkisiler=[]
    #sonkisiler[0]=gelenKisiler
    i=0
    for i in range(len(gelenKisiler)):
        listBox.insert(i,gelenKisiler[i])
        i=i+1
        
    
   
    

  
        


#"faces/" + f
 # cv2.imwrite('./faces/ahmeaasat.jpg', save_photo)         
def KisiKaydet():
    cap = cv2.VideoCapture(0)
    while True:
        #gelenKisiler=[]
        ret, save_photo = cap.read()
        value=entry.get()
        ek=".jpg"
        bilgi=" Kayıt için k tuşuna basın"
        
        cv2.imshow('Video', save_photo)
       # cv2.putText(save_photo, bilgi, font, 1.0, (255, 255, 255), 2)
        if cv2.waitKey(1) & 0xFF == ord('k'):
            cv2.imwrite("./faces/"+value+ek, save_photo)   #faces klasorune kaydediyorum
            cv2.destroyAllWindows()
            break

def get_encoded_faces():
                encoded = {}
                for dirpath, dnames, fnames in os.walk("./faces"):
                    for f in fnames:
                        if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg"):
                            face = face_recognition.load_image_file("faces/" + f)
                            encoding = face_recognition.face_encodings(face)[0] #yuzler sayisal karsılaga kodlanır(128-dimension)
                            encoded[f.split(".")[0]] = encoding
                with open('dataset_faces.dat', 'wb') as f:
                     pickle.dump(encoded, f) # Save face encodings
                
                message_box=messagebox.showinfo(title = "info", message = "Kişi Kaydedildi")
                print(message_box)
                return encoded
            
        
         
  

            
        #%%
pw = ttk.Panedwindow(window, orient = tk.HORIZONTAL)
pw.pack(fill = tk.BOTH, expand = True)

m2 = ttk.Panedwindow(pw, orient = tk. VERTICAL)

frame2 = ttk.Frame(pw, width = 620, height = 340, relief = tk.RIDGE)
frame3 = ttk.Frame(pw, width = 620, height = 300, relief = tk.RAISED)
m2.add(frame2)
m2.add(frame3)

frame1 = ttk.Frame(pw, width = 460, height = 640, relief = tk.GROOVE)
pw.add(m2)
pw.add(frame1)




entry = tk.Entry(frame2, width = 35)
entry.insert(string = "",index = 0)
entry.place(x=70, y=120) 



button1=tk.Button(frame2, text="Fotoğraf Çek", command=KisiKaydet, width=20, height=3)
button1.place(x=430, y=100)




label1 = tk.Label(frame2, text = "Fotoğraf Çekmek için kamera açılınca k tuşuna basın")
label1.place(x = 35, y = 160)


label2 = tk.Label(frame2, text = "Kişi Adı: ")
label2.place(x = 5, y = 120)

button3=tk.Button(frame2, text="Kişiyi Kaydet", command=get_encoded_faces, width=20, height=3)
button3.place(x=430, y=200)

button2=tk.Button(frame3, text="Kişi Tanımayı Aç", command=yuztanima, width=30, height=6)
button2.place(x=200, y=100)

button3=tk.Button(frame1, text="Gelen Kişileri Listele", command=KisileriGetir, width=20, height=3)
button3.place(x=70, y=20)


listBox = tk.Listbox(frame1, selectmode = tk.MULTIPLE, height=25, width=50)

listBox.place(x = 30, y = 100)

window.mainloop()



                        
                    
                    
                    
                


  
      
      
      
      
                  

#%%
                  
            
    

            



