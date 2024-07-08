import cv2

video = "videolink"  # 
height = 1920
width = 1080
target_width = 800  # Hedef pencere genişliği

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Kamera çerçevesi boş.")
        continue

    # Çerçeveyi hedef genişliğe yeniden boyutlandır
    aspect_ratio = image.shape[1] / image.shape[0]  # Oranı koru
    target_height = int(target_width / aspect_ratio)
    resized_image = cv2.resize(image, (target_width, target_height))

    cv2.imshow('Compare Intensity', resized_image)
    if cv2.waitKey(5) & 0xFF == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
