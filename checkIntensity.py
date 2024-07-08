import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk

class CustomShapeEditor:
    def __init__(self, video_source=0, radius=50, num_edges=10, center=(200, 200), fill_color=(0, 255, 0)):
        self.video_source = video_source
        self.radius = radius
        self.num_edges = num_edges
        self.center = center
        self.fill_color = fill_color
        self.points = None
        self.dragging = None
        self.move = None
        self.image = None
        self.filled_image = None
        self.result = None
        self.capture = cv2.VideoCapture(self.video_source, cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.create_window()

    def generate_points(self):
        points = []
        for i in range(self.num_edges):
            angle_deg = 360.0 / self.num_edges * i
            angle_rad = np.radians(angle_deg)
            x = int(self.center[0] + self.radius * np.cos(angle_rad))
            y = int(self.center[1] + self.radius * np.sin(angle_rad))
            points.append((x, y))

        points = np.array(points, np.int32)
        return points.reshape((-1, 1, 2))

    def create_window(self):
        _, frame = self.capture.read()
        aspect_ratio = frame.shape[1] / frame.shape[0]  # Keep the ratio
        target_height = int(800 / aspect_ratio)
        resized_image = cv2.resize(frame, (800, target_height))
        image_height, image_width, _ = resized_image.shape  # Get height and width of the image

        self.points = self.generate_points()
        self.filled_image = np.zeros_like(frame)
        #cv2.fillPoly(self.filled_image, [self.points], self.fill_color) you can fill the area
        self.result = cv2.addWeighted(frame, 1, self.filled_image, 0.4, 0)

        # Convert the result to RGB (from BGR) and then to PIL Image
        self.result = cv2.cvtColor(self.result, cv2.COLOR_BGR2RGB)
        self.result = Image.fromarray(self.result)

        self.root = tk.Tk()
        self.root.title("Custom Shape Editor")

        # Convert the PIL Image to tkinter PhotoImage
        self.result_tk = ImageTk.PhotoImage(self.result)

        self.canvas = tk.Canvas(self.root, width=image_width, height=image_height)
        self.canvas.pack()

        # Display the image on canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.result_tk)

        # Draw red circles at the points
        for point in self.points:
            x, y = point[0]
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red", outline="red")

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.move_point)
        self.canvas.bind("<B1-Motion>", self.move_point)
        self.canvas.bind("<ButtonRelease-1>", self.move_point)
        self.canvas.bind("<Button-3>", self.get_average_color)  # Sağ tıklama olayı atanıyor
        self.root.after(0, self.update_result)  # Update the result continuously
        self.root.mainloop()

    def move_point(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if event.type == tk.EventType.ButtonPress:
            for i, point in enumerate(self.points):
                if np.sqrt((point[0][0] - x)**2 + (point[0][1] - y)**2) < 10:
                    self.dragging = i
                    break
            if self.dragging is None:
                self.move = True
        elif event.type == tk.EventType.Motion:
            if self.dragging is not None:
                self.points[self.dragging] = [[x, y]]
                self.update_result()
            elif self.move:
                point_inside = cv2.pointPolygonTest(self.points, (x, y), False)
                if point_inside >= 0:
                    delta_x = x - self.center[0]
                    delta_y = y - self.center[1]
                    self.points += np.array([delta_x, delta_y], dtype=np.int32)
                    self.center = (x, y)
                    self.update_result()
        elif event.type == tk.EventType.ButtonRelease:
            self.dragging = None
            self.move = False

    def update_result(self):
        _, frame = self.capture.read()
        aspect_ratio = frame.shape[1] / frame.shape[0]  # Keep the ratio
        target_height = int(800 / aspect_ratio)
        resized_frame = cv2.resize(frame, (800, target_height))

        # Fill image boyutlarını da yeniden boyutlandır (reshaping)
        resized_filled_image = cv2.resize(self.filled_image, (resized_frame.shape[1], resized_frame.shape[0]))

        # cv2.addWeighted() işlemini yeniden boyutlandırılmış görüntüler üzerinde uygula (apply on the image)
        self.result = cv2.addWeighted(resized_frame, 1, resized_filled_image, 0.4, 0)

        # Convert the result to RGB (from BGR) and then to PIL Image
        self.result = cv2.cvtColor(self.result, cv2.COLOR_BGR2RGB)
        self.result = Image.fromarray(self.result)

        # Update the PhotoImage
        self.result_tk = ImageTk.PhotoImage(self.result)

        # Update canvas image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.result_tk)

        # Draw red circles at the points
        for point in self.points:
            x, y = point[0]
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red", outline="red")



    def get_average_color(self, event):
        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))
        _, frame = self.capture.read()
        aspect_ratio = frame.shape[1] / frame.shape[0]  # Keep the ratio
        target_height = int(800 / aspect_ratio)
        resized_image = cv2.resize(frame, (800, target_height))

        mask = np.zeros(resized_image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [self.points], (255, 255, 255))

        # Maskeyi yeniden boyutlandır
        mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

        average_color = cv2.mean(frame, mask=mask)
        print("Average color:", average_color)



# Example ...
editor_1 = CustomShapeEditor(video_source=0, radius=50, num_edges=8, center=(200, 200))
