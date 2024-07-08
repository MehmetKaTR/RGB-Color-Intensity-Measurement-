RGB Color Intensity Measurement using OpenCV
This Python script utilizes OpenCV to measure the color intensity within a custom-defined shape overlaid on a live video feed.

Features
Custom Shape Editing: Define a polygonal shape with adjustable parameters such as radius, number of edges, and center coordinates.
Live Video Feed: Displays the real-time video feed with the custom shape overlaid.
Interactive Editing: Allows dragging and moving of the shape vertices directly on the video feed.
Color Measurement: Right-clicking within the shape calculates and prints the average RGB color intensity of the pixels within that area.
Installation
Clone the repository:
bash
Copy code
git clone https://github.com/MehmetKaTR/checkIntensity.git  
Navigate to the project directory and install dependencies:
Copy code
pip install -r requirements.txt
Usage
Run the script:
Copy code
python custom_shape_editor.py
The application window will open with the live video feed and interactive editing tools.
Left-click and drag vertices of the shape to modify its position.
Right-click within the shape to print the average RGB color intensity.
Requirements
Python 3.x
OpenCV
NumPy
Tkinter
Pillow (PIL)
Example
python
Copy code
from custom_shape_editor import CustomShapeEditor

# Example usage:
editor = CustomShapeEditor(video_source=0, radius=50, num_edges=8, center=(200, 200))
