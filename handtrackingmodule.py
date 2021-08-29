import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, num_hands=2, detect_con=0.5, tracking_con=0.5):
        self.mode = mode
        self.maxHands = num_hands
        self.detection_confidence = detect_con
        self.tracking_confidence = tracking_con
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detection_confidence, self.tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def find_Hands(self, img, Draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if Draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS,
                                               self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=2,
                                                                       circle_radius=2),
                                               self.mpDraw.DrawingSpec(color=(224, 224, 224), thickness=2, circle_radius=2))
        return img

    def locateHands(self, img, handNo=0, draw=True, finger_point=4):
        Landmark_lists = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, Lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(Lm.x * w), int(Lm.y * h)
                # print(id, cx, cy)
                Landmark_lists.append([id, cx, cy])
                if draw:
                    if id == finger_point:
                        cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

        return Landmark_lists

    def get_label(self, img):
        myHand = self.results.multi_handedness
        label = "HandNotFound"
        if myHand != None:
            if myHand[0].classification[0].label == "Left":
                label = "Right"
            else:
                label = "Left"
        return label


def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.find_Hands(img)
        LandmarkList = detector.locateHands(img, finger_point=0)
        # if len(LandmarkList) != 0:
        # print(LandmarkList[4])

        label = detector.get_label(img)
        print(label)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3, (250, 0, 250), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
