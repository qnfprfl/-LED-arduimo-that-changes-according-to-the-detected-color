#-*- coding: utf-8 -*-
import cv2
import numpy as np

#아두이노 통신용
#from CSerial import CSerial

def nothing(a):

    pass


def trackbar(cap):
    window_name = "COLOR_DETECTION"

    # 트랙바 담을 윈도우 생성
    cv2.namedWindow(window_name)

    # 트랙바 생성
    cv2.createTrackbar("thresh_val", window_name, 0, 255, nothing)
    cv2.createTrackbar("lower_h", window_name, 0, 255, nothing)
    cv2.createTrackbar("lower_s", window_name, 0, 255, nothing)
    cv2.createTrackbar("lower_v", window_name, 0, 255, nothing)
    cv2.createTrackbar("upper_h", window_name, 120, 255, nothing)
    cv2.createTrackbar("upper_s", window_name, 120, 255, nothing)
    cv2.createTrackbar("upper_v", window_name, 120, 255, nothing)

    while True:

        if (not cap.isOpened()):
            print("Cannot capture video")
            break
        ret, frame = cap.read()
        # threshold 값 트랙바에서 찾기
        thresh_val = cv2.getTrackbarPos("thresh_val", window_name)
        lower_h = cv2.getTrackbarPos("lower_h", window_name)
        lower_s = cv2.getTrackbarPos("lower_s", window_name)
        lower_v = cv2.getTrackbarPos("lower_v", window_name)
        upper_h = cv2.getTrackbarPos("upper_h", window_name)
        upper_s = cv2.getTrackbarPos("upper_s", window_name)
        upper_v = cv2.getTrackbarPos("upper_v", window_name)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        H = cv2.inRange(hsv, (lower_h, lower_s, lower_v), (upper_h, upper_s, upper_v))
        blurred = cv2.blur(H, (5, 5))
        ret, thresh = cv2.threshold(blurred, thresh_val, 255, 0)
        kernel = np.ones((5, 5), np.uint8)
        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # opencv 낮은버전(정확히 기억안남)에서는
        # im2, contours, hierarchy = cv2.findContours(opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # 라고 해도 상관없었는데 높은버전 되면서 오류발생함
        im2 = opened
        contours, hierarchy = cv2.findContours(opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 디텍션 이외의 정보 지우기
        for cnt in contours:
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
            # contour에서 일정 면적 이상만 저장하여 나중에 그림
            if cv2.contourArea(cnt) > 10000:
                print(cv2.contourArea(cnt))

        cv2.imshow("원본", frame)

        cv2.imshow(window_name, im2)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

'''''''''''''''''''''''''''''''''''''''
아두이노 시리얼통신용 다른 주석처리된 부분도 같이 해제
def InitializeArduino():
    obj=CSerial()
    res = obj.ConnectArduino()
    if res == True:
        print ("Connected to ", obj.PORT)
    else:
        exit(1)

    return obj
'''''''''''''''''''''''''''''''''''''''

def GetColorValue(outputcolor):
    if outputcolor == "black":
        return (0, 255, 0)
    elif outputcolor == "red":
        return (255, 255, 255)
    elif outputcolor == 'white':
        return (255,0,0)
    elif outputcolor == 'blue':
        return (153,0,133)
    else:
        return (0, 0, 0)


def main():
    #아두이노 통신용
    #arduino = InitializeArduino()

    #색상값 저장 경로
    path = "C:\\color.txt"

    videopath = "C:\\Users\\example\\Desktop\\temp\\test.mp4"
    f= open(path, "r")
    text = f.readlines()
    count = len(text)

    cap = cv2.VideoCapture(0)

    #값찾기용
    #trackbar(cap)

    while True:

        if (not cap.isOpened()):
            print("Cannot capture video")
            break
        ret, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for i in range(count):
            strdata = text[i].split(' ')

            detect = cv2.inRange(hsv, (0,0,0), (255,255,255))
            detect = cv2.inRange(hsv, (int(strdata[2]), int(strdata[3]), int(strdata[4])), (int(strdata[5]), int(strdata[6]), int(strdata[7])))
            blurred = cv2.blur(detect, (5, 5))
            ret, thresh = cv2.threshold(blurred, int(strdata[1]), 255, 0)
            kernel = np.ones((5, 5), np.uint8)
            opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

            im2 = opened
            contours, hierarchy = cv2.findContours(opened, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if cv2.contourArea(cnt) > 10000:

                    print(strdata[0])
                    (r, g, b) = GetColorValue(strdata[0])
                    # 아두이노 통신용
                    #arduino.write_color(r, g, b)

                    break

            #cv2.imshow("원본", frame)

            #if cv2.waitKey(1000) & 0xFF == ord('q'):
            #    break

main()
