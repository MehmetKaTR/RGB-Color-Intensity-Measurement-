import cv2
import numpy as np
import sqlite3

sql_file = "intensity.db"

conn = sqlite3.connect(sql_file)
cursor = conn.cursor()


def write_circle_info(center, r, pos):
    query = "INSERT INTO circle VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (None, center[0], center[1], r, pos))
    conn.commit()


def set_circle_info(id, x, y, r, pos):
    query = "UPDATE circle SET x = ?, y = ?, r = ?, positive = ? WHERE id = ?"
    cursor.execute(query, (x, y, r, pos, id))
    conn.commit()


def get_circle_info(mouseX, mouseY):
    query = "SELECT id, x, y, r FROM circle"
    cursor.execute(query)
    circles = cursor.fetchall()

    # En yakın çemberin merkezini ve yarıçapını başlangıçta varsayılan bir değere atayalım
    closest_circle = None
    min_distance = float('inf')  # Sonsuz büyük bir değer

    for circle in circles:
        id = circle[0]
        circle_center = (circle[1], circle[2])
        radius = circle[3]
        distance = np.sqrt((mouseX - circle_center[0])**2 + (mouseY - circle_center[1])**2)
        if distance < min_distance:
            min_distance = distance
            closest_circle = (id, circle_center, radius)

    return closest_circle


def get_all_circle_info():
    query = "SELECT x, y, r FROM circle"
    cursor.execute(query)
    return cursor.fetchall()


def draw_circles_on_image(image, circles):
    for circle in circles:
        center = (circle[0], circle[1])
        radius = circle[2]
        cv2.circle(image, center, radius, (0, 255, 255), 2)


# Global variables
drawing = False  # True if mouse is pressed
ix, iy = -1, -1  # Starting coordinates
r = 20  # Initial radius
circle_center = (ix, iy)  # Circle center
coords = []
dragging = False
result = None

# Function to draw the circle
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, r, circle_center, img_copy, dragging, result, new_circle_center
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        circle_center = (ix, iy)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            r = int(np.sqrt((x - ix) ** 2 + (y - iy) ** 2))  # Calculate radius based on mouse position
            circle_center = (ix, iy)
            cv2.circle(img_copy, circle_center, r, (0, 255, 255), 2)
            cv2.imshow("Circle Window", img_copy)
        elif dragging:
            new_circle_center = (max(0, min(x, 499)), max(0, min(y, 499)))  # 499 is the size of your resized image - 1
            cv2.circle(img_copy, new_circle_center, result[2], (0, 255, 255), 2)
            cv2.imshow("Circle Window", img_copy)


    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # Draw the circle on the original image
        cv2.circle(img_copy, circle_center, r, (0, 255, 255), 2)
        cv2.imshow("Circle Window", img_copy)
        write_circle_info(circle_center, r, 1)

    elif event == cv2.EVENT_RBUTTONDOWN:
        result = get_circle_info(x, y)
        distance = np.sqrt((x - result[1][0])**2 + (y - result[1][1])**2)
        if distance < result[2]:  # Radius of the circle
            dragging = True

    elif event == cv2.EVENT_RBUTTONUP:
        if dragging and result:  # If dragging and result is not None
            dragging = False
            print(new_circle_center)
            cv2.circle(img_copy, new_circle_center, result[2], (0, 255, 255), 2)
            cv2.imshow("Circle Window", img_copy)
            set_circle_info(result[0], new_circle_center[0], new_circle_center[1], result[2], 1)


img = cv2.imread("duvar.jpg")
img = cv2.resize(img, (500, 500))


# Create a named window
cv2.namedWindow("Circle Window")

# Set mouse callback function
cv2.setMouseCallback("Circle Window", draw_circle)

while True:

    img_copy = img.copy()
    # Draw the circle on the image
    circles = get_all_circle_info()
    draw_circles_on_image(img_copy, circles)

    # Display the image
    cv2.imshow('Circle Window', img_copy)

    # Wait for ESC key to exit the loop
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()