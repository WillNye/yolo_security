import errno
import os
import sys
import threading
from datetime import datetime as dt, timedelta

import cvlib as cv
import cv2

from config import BASE_VIDEO_PATH, FPS, HORIZONTAL_PIXEL_COUNT, VERTICAL_PIXEL_COUNT, VIDEO_CAPTURE_SOURCE
from yolo_email import send_email

cap = cv2.VideoCapture(VIDEO_CAPTURE_SOURCE)
cap.set(3, HORIZONTAL_PIXEL_COUNT)
cap.set(4, VERTICAL_PIXEL_COUNT)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
cur_second = dt.now().second
remaining_scans = 2


while True:
    file_path = '{}/{}/{}/{}/{}/{}_output.avi'.format(BASE_VIDEO_PATH,
                                                      dt.now().year, dt.now().month, dt.now().day, dt.now().hour,
                                                      dt.now().strftime("%Y_%m_%d__%H_%M"))

    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    stop_at = dt.now() + timedelta(minutes=1)
    out = cv2.VideoWriter(file_path, fourcc, float(FPS), (int(cap.get(3)), int(cap.get(4))))
    sending_email = False
    detected_objects = dict()
    detected_objects['person'] = 0

    while dt.now() < stop_at:
        ret, frame = cap.read()

        if dt.now().second != cur_second:
            cur_second = dt.now().second
            remaining_scans = 2

            if detected_objects['person'] >= 3 and not sending_email:
                sending_email = True
                status = cv2.imwrite('detected_person.jpg', frame)
                email_thread = threading.Thread(target=send_email, args=(), kwargs={})
                email_thread.start()

        if detected_objects['person'] <= 3 and remaining_scans > 0:
            remaining_scans -= 1

            bbox, label, conf = cv.detect_common_objects(frame)
            if 'person' in label:
                detected_objects['person'] += 1

        if ret:
            out.write(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                out.release()
                sys.exit(0)
        else:
            cap.release()
            cv2.destroyAllWindows()
            break

    # Release the capture
    out.release()
    if sending_email:
        email_thread.join()
