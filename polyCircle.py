import numpy as np
import cv2

class CustomShapeEditor:
    def __init__(self, image_path, radius=50, num_edges=10, center=(200, 200), fill_color=(0, 255, 0)):
        self.image_path = image_path
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
        self.image = cv2.imread(self.image_path)
        self.points = self.generate_points()
        self.filled_image = np.zeros_like(self.image)
        cv2.fillPoly(self.filled_image, [self.points], self.fill_color)
        self.result = cv2.addWeighted(self.image, 1, self.filled_image, 0.4, 0)
        for point in self.points:
            cv2.circle(self.result, tuple(point[0]), radius=5, color=(0, 0, 255), thickness=-1)
        cv2.imshow("Custom Shape", self.result)
        cv2.setMouseCallback("Custom Shape", self.move_point)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def move_point(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, point in enumerate(self.points):
                if np.sqrt((point[0][0] - x)**2 + (point[0][1] - y)**2) < 10:
                    self.dragging = i
                    break
            if self.dragging is None:
                self.move = True
        elif event == cv2.EVENT_MOUSEMOVE:
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
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = None
            self.move = False
        elif event == cv2.EVENT_RBUTTONDOWN:
            mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [self.points], (255, 255, 255))
            average_color = cv2.mean(self.image, mask=mask)
            print("Average color:", average_color)

    def update_result(self):
        self.filled_image = np.zeros_like(self.image)
        cv2.fillPoly(self.filled_image, [self.points], self.fill_color)
        self.result = cv2.addWeighted(self.image, 1, self.filled_image, 0.4, 0)
        for point in self.points:
            cv2.circle(self.result, tuple(point[0]), radius=5, color=(0, 0, 255), thickness=-1)
        cv2.imshow("Custom Shape", self.result)

image_path_1 = "duvar.jpg"
editor_1 = CustomShapeEditor(image_path_1, radius=50, num_edges=16, center=(200, 200))

