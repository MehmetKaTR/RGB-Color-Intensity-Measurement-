from tkinter import *
import cv2 
from PIL import Image, ImageTk
import numpy as np


# Define global variables
cap = None
label_widget = None
label_widget2 = None
photo = None
target_width = 800


def open_camera():
    global cap
    if cap == None:
        video = "videolink" 
        height = 1920
        width = 1080

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

        show_frame() 
    else:
        print("Camera is already opened")


def show_frame():
    global cap
    global photo
    if cap is not None:
        success, image = cap.read()

        if success:
            aspect_ratio = image.shape[1] / image.shape[0]  # Oranı koru
            target_height = int(target_width / aspect_ratio)
            resized_image = cv2.resize(image, (target_width, target_height))
            photo = ImageTk.PhotoImage(image=Image.fromarray(resized_image))
                    
            label_widget.config(image=photo)
            label_widget.image = photo  
                    
        label_widget.after(10, show_frame)


def capture_image():
    global cap, label_widget2
    if cap is not None:
        success, image = cap.read()

        if success:
            global photo
            # Update label with captured frame
            label_widget2.config(image=photo)
            label_widget2.image = photo


def close_camera():
    global cap
    
    if cap is not None:
        cap.release()
        cap = None
    else:
        print("Camera is already closed")


def circle():
    pass



def rectangle():
    pass


def main():
    global label_widget, label_widget2
    
    # Create a GUI app
    app = Tk()
    app.geometry("1200x800")
    app.title("Camera Viewer")
    
    # Bind the app with Escape keyboard to quit app whenever pressed
    app.bind('<Escape>', lambda e: app.quit())
    
    # Create a label to display camera feed
    label_widget = Label(app)
    label_widget.place(relx=0, rely=0)

    label_widget2 = Label(app)
    label_widget2.place(relx=0.6, rely=0.5)  # Change the relative position here
    
    # Create buttons to open and close camera
    open_button = Button(app, text="Open Camera", command=open_camera)
    open_button.place(relx=0.02, rely=0.75, relwidth=0.1, relheight=0.05)
    
    close_button = Button(app, text="Close Camera", command=close_camera)
    close_button.place(relx=0.12, rely=0.75, relwidth=0.1, relheight=0.05)

    capture_button = Button(app, text="Capture Image", command=capture_image)
    capture_button.place(relx=0.22, rely=0.75, relwidth=0.1, relheight=0.05)


    # Create buttons to tool
    circle_button = Button(app, text="Circle", command=circle)
    circle_button.place(relx=0.72, rely=0.02, relwidth=0.1, relheight=0.05)

    rectangle_button = Button(app, text="Rectangle", command=rectangle)
    rectangle_button.place(relx=0.72, rely=0.07, relwidth=0.1, relheight=0.05)

    custom_button = Button(app, text="Custom Tool", command=rectangle)
    custom_button.place(relx=0.72, rely=0.12, relwidth=0.1, relheight=0.05)
    
    # Start the GUI app
    app.mainloop()


if __name__ == "__main__":
    main()
