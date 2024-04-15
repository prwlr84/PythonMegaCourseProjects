import glob
import os
import time
from threading import Thread

import cv2

from CamAlert.send_mail import send_email

video = cv2.VideoCapture(0)
time.sleep(1)

first_fr = None


def create_gray(frame_data):
    gray = cv2.cvtColor(frame_data, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(gray, (21, 21), 0)


def clear_folder():
    for img in glob.glob('images/*.png'):
        os.remove(img)


status_list = []

while True:
    status = 0
    check, frame = video.read(0)
    count = 0
    gray_gau = create_gray(frame)

    if first_fr is None:
        first_fr = gray_gau

    delta = cv2.absdiff(first_fr, gray_gau)

    thresh_frame = cv2.threshold(delta, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow('my video', gray_gau)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f'images/{count}.png', frame)
            count += 1
            all_images = glob.glob('images/*.png')
            image_to_send = all_images[int(len(all_images) / 2)]

    status_list.append(status)
    status_list = status_list[-2:]
    clean_thread = Thread(target=clear_folder)
    clean_thread.daemon = True

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_to_send, ))
        email_thread.daemon = True

        email_thread.start()

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
clean_thread.start()
