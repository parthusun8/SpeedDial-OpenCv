import time
import cv2
import handtrackingmodule as htm
from twilio.rest import Client

TWILIO_PHONE_NUMBER = "+xx xx xxxxx"
account_sid = "ENTER YOUR SID HERE"
auth_token = "ENTER YOUR AUTH TOKEN HERE"
client = Client(account_sid, auth_token)
client_numbers = ["+xx xx xxxxx", "+xx xx xxxxx", "+xx xx xxxxx", "+xx xx xxxxx", "+xx xx xxxxx",
                  "+xx xx xxxxx"]

################################
wCam, hCam = 640, 480
################################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0
detector = htm.handDetector(detect_con=0.75)
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.find_Hands(img)
    Landmark_list = detector.locateHands(img, draw=False)
    label = detector.get_label(img)
    count = 0
    if len(Landmark_list) != 0:
        result = []
        if label == "Left":
            # Thumb
            if Landmark_list[4][1] < Landmark_list[5][1]:
                result.append(1)
            else:
                result.append(0)
        else:
            # Thumb
            if Landmark_list[4][1] > Landmark_list[5][1]:
                result.append(1)
            else:
                result.append(0)

        # 4 Fingers
        for tip in range(1, 5):
            if Landmark_list[tipIds[tip]][2] < Landmark_list[tipIds[tip] - 2][2]:
                # print(Landmark_list[4][2])
                result.append(1)
            else:
                result.append(0)

        # print(result)

        count = result.count(1)
        print(count)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
    # 1, (255, 0, 0), 2)
    cv2.putText(img, str(int(count)), (50, 450), cv2.FONT_ITALIC, 3, (128, 0, 128), 2)
    if count == 0:
        pass
    elif count == 1:
        cv2.putText(img, "CALLING .. ", (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 2)
        time.sleep(1)
        call = client.calls.create(
            to=client_numbers[0],
            from_=TWILIO_PHONE_NUMBER,
            url="http://static.fullstackpython.com/phone-calls-python.xml",
            method="GET"
        )
        time.sleep(5)
    elif count == 2:
        cv2.putText(img, "CALLING .. ", (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 2)
        time.sleep(1)
        call = client.calls.create(
            to=client_numbers[1],
            from_=TWILIO_PHONE_NUMBER,
            url="http://static.fullstackpython.com/phone-calls-python.xml",
            method="GET"
        )
        time.sleep(5)
    elif count == 3:
        cv2.putText(img, "CALLING .. ", (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 2)
        time.sleep(1)
        call = client.calls.create(
            to=client_numbers[2],
            from_=TWILIO_PHONE_NUMBER,
            url="http://static.fullstackpython.com/phone-calls-python.xml",
            method="GET"
        )
        time.sleep(5)
    elif count == 4:
        cv2.putText(img, "CALLING .. ", (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 2)
        time.sleep(1)
        call = client.calls.create(
            to=client_numbers[3],
            from_=TWILIO_PHONE_NUMBER,
            url="http://static.fullstackpython.com/phone-calls-python.xml",
            method="GET"
        )
        time.sleep(5)
    elif count == 5:
        cv2.putText(img, "CALLING .. ", (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 2)
        time.sleep(1)
        call = client.calls.create(
            to=client_numbers[4],
            from_=TWILIO_PHONE_NUMBER,
            url="http://static.fullstackpython.com/phone-calls-python.xml",
            method="GET"
        )
        time.sleep(5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
