import numpy as np
import cv2

image = cv2.imread("duvar.jpg")

center1 = (200, 200)
center2 = (400, 400)
radius = 50
num_edges = 8

global dragging
dragging = None

global move
move = None


points1 = []
for i in range(num_edges):
    angle_deg = 360.0 / num_edges * i
    angle_rad = np.radians(angle_deg)
    x = int(center1[0] + radius * np.cos(angle_rad))
    y = int(center1[1] + radius * np.sin(angle_rad))
    points1.append((x, y))

points1 = np.array(points1, np.int32)
points1 = points1.reshape((-1, 1, 2))


fill_color = (0, 255, 0) 
filled_image = np.zeros_like(image)

cv2.fillPoly(filled_image, [points1], fill_color)  #fill polygon

result = cv2.addWeighted(image, 1, filled_image, 0.4, 0)  # opacity

for point in points1:
    cv2.circle(result, tuple(point[0]), radius=5, color=(0, 0, 255), thickness=-1)



def move_point(event, x, y, flags, param):
    global dragging, center1, move, points1, result
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, point in enumerate(points1):
            if np.sqrt((point[0][0] - x)**2 + (point[0][1] - y)**2) < 10:
                dragging = i
                break
        if dragging is None:
            move = True  

    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging is not None:
            if dragging < len(points1):
                points1[dragging] = [[x, y]]

            filled_image = np.zeros_like(image)
            cv2.fillPoly(filled_image, [points1], fill_color)
            result = cv2.addWeighted(image, 1, filled_image, 0.4, 0)
            for point in points1:
                cv2.circle(result, tuple(point[0]), radius=5, color=(0, 0, 255), thickness=-1)

            cv2.imshow("Custom Shape", result)
        elif move:  
            point_inside = cv2.pointPolygonTest(np.vstack(points1), (x, y), False)
            if point_inside >= 0:  
                delta_x = x - center1[0]
                delta_y = y - center1[1]
                points1 += np.array([delta_x, delta_y], dtype=np.int32)
                center1 = (x, y)
                filled_image = np.zeros_like(image)
                cv2.fillPoly(filled_image, [points1], fill_color)
                result = cv2.addWeighted(image, 1, filled_image, 0.4, 0)
                for point in points1:
                    cv2.circle(result, tuple(point[0]), radius=5, color=(0, 0, 255), thickness=-1)
                cv2.imshow("Custom Shape", result)

    elif event == cv2.EVENT_LBUTTONUP:
        dragging = None
        move = False  

    elif event == cv2.EVENT_RBUTTONDOWN:
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [points1], (255, 255, 255))

        average_color = cv2.mean(image, mask=mask)
        print("Average color:", average_color)



# Create a named window
cv2.namedWindow("Custom Shape")

# Set mouse callback function
cv2.setMouseCallback("Custom Shape", move_point)


cv2.imshow("Custom Shape", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
