import numpy as np
import cv2

# Kamerayı aç
cap = cv2.VideoCapture(0)

# Lucas-Kanade parametrelerini ayarla
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Rastgele renkler oluştur
color = np.random.randint(0, 255, (100, 3))

# İlk kareyi yakala ve gri tonlamaya dönüştür
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

# İlk anahtar noktaları bul
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

# Maske oluştur
mask = np.zeros_like(old_frame)

while True:
    # Yeni kareyi al ve griye dönüştür
    ret, frame = cap.read()
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Optik akışı hesapla
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # İyi noktaları seç
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    # Her iyi nokta için iz sürme ve daire çizme
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel().astype(int)
        c, d = old.ravel().astype(int)
        mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
        frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)

    # İzleri kareye ekle
    img = cv2.add(frame, mask)

    # Göster
    cv2.imshow('frame', img)

    # Çıkış için ESC tuşuna basılmasını bekleyin
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # Sonraki döngü için hazırlık yap
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

# Pencereyi kapat ve kamerayı serbest bırak
cv2.destroyAllWindows()
cap.release()
