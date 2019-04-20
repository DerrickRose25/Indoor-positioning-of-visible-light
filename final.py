import cv2
import numpy as np
import math

error = 0
center_x = []
center_y = []


def get_len(center_x, center_y):  # 获得三个灯构成三角形的三边长度
    x1 = center_x[0] - center_x[1]
    y1 = center_y[0] - center_y[1]
    x2 = center_x[1] - center_x[2]
    y2 = center_y[1] - center_y[2]
    x3 = center_x[0] - center_x[2]
    y3 = center_y[0] - center_y[2]
    len1 = math.len = int(math.sqrt((x1 ** 2) + (y1 ** 2)))
    len2 = math.len = int(math.sqrt((x2 ** 2) + (y2 ** 2)))
    len3 = math.len = int(math.sqrt((x3 ** 2) + (y3 ** 2)))
    # print(len1,len2,len3)
    length = [len1, len2, len3]  # 返回三个边的长度
    return length


def get_min_len(length, center_x, center_y):  # 获得最小的边并返回最小边两点的值
    min_len = sorted(length)[0]
    # print(min_len)
    if min_len == length[0]:
        (x1, x2, y1, y2) = (center_x[0], center_x[1], center_y[0], center_y[1])
        return (x1, x2, y1, y2)
    if min_len == length[1]:
        (x1, x2, y1, y2) = (center_x[1], center_x[2], center_y[1], center_y[2])
        return (x1, x2, y1, y2)
    if min_len == length[2]:
        (x1, x2, y1, y2) = (center_x[0], center_x[2], center_y[0], center_y[2])
        return (x1, x2, y1, y2)


def Calculate_angle():
    direct = ""
    length = get_len(center_x, center_y)
    (x1, x2, y1, y2) = get_min_len(length, center_x, center_y)  # 求出最小边两个点的坐标
    # print((x1,x2,y1,y2))
    if x1 - x2 == 0:
        direct = "right"
        angle = 3
        # print("右偏：{}".format(angle))
    else:
        k = (y1 - y2) / (x1 - x2)  # 求最短边的斜率
        angle = math.atan(k)  # 求弧度
        angle = int(angle * 57.3)  # 求角度，1弧度= 57.3度
        # print(angle)
        # 左转
        if 0 < angle + 3 <= 90:
            # 求与y轴的偏移角度
            angle = 87 - angle
            direct = "left"
            # print("左偏：{}".format(angle))
        # 右转
        elif 90 < angle + 3 < 93:
            angle = -(angle - 87)
            direct = "right"
            # print("右偏：{}".format(angle))
        elif -90 < angle - 3 <= 0:
            angle = -(93 + angle)
            direct = "right"
            # print("右偏：{}".format(angle))
    return direct, angle



def detect(frame):  # 分析三个灯定位并返回坐标
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kernel_dilate = np.ones((12, 12), np.uint8)
    blur = cv2.medianBlur(gray, 9)
    # 二值化
    ret, binary = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(binary, kernel_dilate)
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel_dilate)
    # 寻找轮廓
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    global center_x
    global center_y
    global error
    global flag
    center_x = []
    center_y = []
    count = 0
    arclengthMin = 32.0
    arclengthMax = 190.0
    squareMin = 160.0
    squareMax = 1700.0

    while True:
        for i in range(len(contours)):
            arclength = cv2.arcLength(contours[i], True)
            # print(arclength)
            square = cv2.contourArea(contours[i])
            # print(square)
            (x, y), radius = cv2.minEnclosingCircle(contours[i])
            if (arclength > arclengthMin and arclength < arclengthMax and square > squareMin and square < squareMax):
                count = count + 1
                # print(count)
                center_x.append(x)
                center_y.append(y)
                # cv2.drawContours(frame, contours[i], -1, (0, 0, 255), 2)
                cv2.circle(frame, (int(x), int(y)), 3, (0, 0, 255), -1)
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0))
        # print(center_x,center_y)
        cv2.imshow("frame", frame)

        if count == 3:
            error = 0
            flag = True
            break
        elif count < 3:
            error = error + 1
            arclengthMin = arclengthMin - 3
            arclengthMax = arclengthMax + 3
            squareMin = squareMin - 7
            squareMax = squareMax + 7
            if error >= 15:
                error = 0
                flag = False
                break
        else:
            error = error + 1
            arclengthMin = arclengthMin + 5
            arclengthMax = arclengthMax - 5
            squareMin = squareMin + 10
            squareMax = squareMax - 10
            if error >= 15:
                error = 0
                flag = False
                break


def get_centroid(center_x, center_y):  # 获得三角形质心
    centroid_x = center_x[0] + center_x[1] + center_x[2]
    centroid_y = center_y[0] + center_y[1] + center_y[2]
    centroid_x = centroid_x / 3
    centroid_y = centroid_y / 3
    centroid = (centroid_x, centroid_y)
    print('质心：{}'.format(centroid))
    return centroid


def get_position(centroid):  # 获得摄像头位置
    area = ""
    # 拟合后的函数    x = 11.65 * i + 401；y = 11.89 * i + 116.1
    pos_x = int(((centroid[0] - 401) / 11.65) * 5)
    pos_y = int(((centroid[1] - 116.1) / 11.89) * 5)
    position = [pos_x, pos_y]
    if -20 < pos_x < 20 and -20 < pos_y < 20:
        area = "A区"
    if -40 < pos_y < -20 and pos_y < pos_x < -pos_y:
        area = "B区"
    if -40 < pos_x < -20 and pos_x < pos_y < -pos_x:
        area = "C区"
    if 20 < pos_y < 40 and -pos_y < pos_x < pos_y:
        area = "D区"
    if 20 < pos_x < 40 and -pos_x < pos_y < pos_x:
        area = "E区"

    return area, position


if __name__ == "__main__":
    # cameraCapture = cv2.VideoCapture('http://192.168.12.1:8080/?action=stream')

    cameraCapture = cv2.VideoCapture(0)
    while True:
        # 获取当前帧
        ret, frame = cameraCapture.read()
        # cv2.imshow("camera", frame)
        detect(frame)
        if flag:
            flag = False
            centroid = get_centroid(center_x, center_y)
            area, position = get_position(centroid)  # standard=(402.25, 112.91)standard为摄像头在中心40X40时质心的坐标
            direct,angle = Calculate_angle()
            print("direct:{direct}  {angle}".format(direct = direct,angle = angle))
            print('postion:    {area}     坐标：{position} '.format(area=area, position=position))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cameraCapture.release()
    cv2.destroyAllWindows()
