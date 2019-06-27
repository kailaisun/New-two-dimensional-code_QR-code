#!/usr/bin/env python
# encoding: utf-8
"""
@author: skl
@site:
@software: PyCharm
@file: two-code-detetor.py
@time: 2018/12/10 10:59
"""
import cv2
import numpy as np
import math
import numpy as np


def gamma_trans(img, gamma):
    # 具体做法先归一化到1，然后gamma作为指数值求出新的像素值再还原
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    # 实现映射用的是Opencv的查表函数
    return cv2.LUT(img, gamma_table)


def transform(img, rect):
    rot_mat = cv2.getRotationMatrix2D(rect[0], rect[2], 1.0)
    size = (img.shape[1], img.shape[0])
    rot_img = cv2.warpAffine(img, rot_mat, size)  # 长宽互换
    # cv2.imshow('rot',rot_img)
    # cv2.waitKey(0)
    return rot_img[int(rect[0][1] - rect[1][1] / 2):int(rect[0][1] + rect[1][1] / 2),
                   int(rect[0][0] - rect[1][0] / 2):int(rect[0][0] + rect[1][0] / 2)]


def iscorner(roi):
    ret2, binary = cv2.threshold(
        roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # binary=cv2.dilate(binary,(3,3))
    binary, contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('n', roi)
    # print(len(contours))
    # cv2.waitKey(0)
    if len(contours) < 2:
        return False

    area = []
    for i in range(len(contours)):
        area.append(cv2.contourArea(contours[i]))
    l1 = max(area)
    l0 = min(area)
    # print(area)
    while(1):
        if l0 == 0:
            area.remove(l0)
            l0 = min(area)
        else:
            break  # 最小值不为0
    for i in range(len(hierarchy[0])):
        if hierarchy[0][i][2] != -1:
            l0 = cv2.contourArea(contours[hierarchy[0][i][2]])
            l1 = cv2.contourArea(contours[i])  # 解析层次关系，并赋值l1和l0为主次轮廓
            break
    if l1 / l0 > 1.2and l1 / l0 < 10:  # 二者面积比例限制
        # cv2.imshow('roi', roi)
        # print('succ')
        # print(l1/l0)
        # cv2.waitKey(0)
        return True
    else:
        return False


def IOU(roi_sum):
    rect = []  # 外接矩形保存
    conter = []  # 中心坐标
    r = []  # 边长
    result = []  # 三个存留

    for i in range(len(roi_sum)):
        ret = cv2.minAreaRect(roi_sum[i])
        rect.append(ret)
        conter.append(ret[0])
        r.append(ret[1][0])
    r = np.array(r)
    id = np.argsort(-r)  # 排序保留下标

    result.append(rect[id[0]])
    ii = 1
    while(1):
        if math.sqrt((int(rect[id[ii]][0][0]) - int(rect[id[0]][0][0])) **
                     2 + (int(rect[id[ii]][0][1]) - int(rect[id[0]][0][1]))**2) > 70:

            result.append(rect[id[ii]])
            if ii == 2:
                break
            else:
                ii = ii + 1
        else:
            id = np.delete(id, ii, 0)
    return result
    # for i in range(len(roi_sum)):
    #     for j in range(len(roi_sum)):
    #         dict[i][j]=math.sqrt((rect[i][0][0]-rect[j][0][0])^2+(rect[i][0][1]-rect[j][0][1])^2)
    # print(dict)


def angle(x, y):
    if x == 0:
        if y > 0:
            return 90
        else:
            return -90
    if y == 0:
        if x > 0:
            return 0
        else:
            return 180

    if x > 0 and y > 0:
        return math.atan(y / x) / math.pi * 180
    if x > 0 and y < 0:
        return math.atan(y / x) / math.pi * 180
    if x < 0 and y > 0:
        return 180 + math.atan(y / x) / math.pi * 180
    else:
        return -180 + math.atan(y / x) / math.pi * 180


def sort_three(result):
    if len(result) != 3:
        return False
    sort_result = []
    (x1, y1, x2, y2, x3, y3) = (
        int(result[0][0][0]), int(result[0][0][1]), int(
            result[1][0][0]), int(result[1][0][1]), int(result[2][0][0]),
        int(result[2][0][1]))
    a = math.sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3))
    b = math.sqrt((x1 - x3) * (x1 - x3) + (y1 - y3) * (y1 - y3))
    c = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    A = math.degrees(math.acos((a * a - b * b - c * c) / (-2 * b * c)))
    B = math.degrees(math.acos((b * b - a * a - c * c) / (-2 * a * c)))
    C = math.degrees(math.acos((c * c - a * a - b * b) / (-2 * a * b)))
    if A <= 110 and A >= 70:
        sort_result.append(result[0])
        # print(x1,y1,x2,y2,x3,y3)
        ct3 = angle(x3 - x1, y1 - y3)
        ct2 = angle(x2 - x1, y1 - y2)
        # print(ct3,ct2)
        if ct3 > ct2:
            sort_result.append(result[1])
            sort_result.append(result[2])
        else:
            sort_result.append(result[2])
            sort_result.append(result[1])
    else:
        if B <= 110 and B >= 70:
            sort_result.append(result[1])
            ct3 = angle(x3 - x2, y2 - y3)
            ct1 = angle(x1 - x2, y2 - y1)
            if ct3 > ct1:
                sort_result.append(result[0])
                sort_result.append(result[2])
            else:
                sort_result.append(result[2])
                sort_result.append(result[0])
        else:
            sort_result.append(result[2])
            ct1 = angle(x1 - x3, y3 - y1)
            ct2 = angle(x2 - x3, y3 - y2)
            if ct1 > ct2:
                sort_result.append(result[1])
                sort_result.append(result[0])
            else:
                sort_result.append(result[0])
                sort_result.append(result[1])
    return sort_result


def isblack(x, y, r, img):
    black_img = img[int(y - r / 2):int(y + r / 2),
                    int(x - r / 2):int(x + r / 2)]
    sum = 0
    h = black_img.shape[0]
    w = black_img.shape[1]
    # print(w,h)
    # cv2.imshow('n',black_img)
    # cv2.waitKey(0)
    for i in range(h):
        for j in range(w):
            sum = sum + black_img[i][j]
    # print(sum/(w*h))
    if sum / (w * h) < 200:
        return 1
    else:
        return 0

def CRC(date):
    a = date.copy()
    a.append(0)
    a1, a2 = a[0], a[1]
    for i in range(len(date)-1):
        if a1 == 1:
            a1 = 1-a2
        else:
            a1 = a2
        a2 = a[i+2]
        # print(i,a1,a2)
    if (a1 == 0) & (a1 == 0):
        return True
    else:
        return False



def decoder(result, img):
    x1, y1 = result[0][0][0], result[0][0][1]
    x2, y2 = result[1][0][0], result[1][0][1]
    x3, y3 = result[2][0][0], result[2][0][1]
    x9, y9 = x2 + x3 - x1, y2 + y3 - y1
    r = min(result[0][1][0], result[1][1][0], result[2][1][0])
    t4 = isblack((x1 + x2) / 2, (y1 + y2) / 2, r, img)
    t5 = isblack((x1 + x3) / 2, (y1 + y3) / 2, r, img)
    t6 = isblack((x2 + x3) / 2, (y2 + y3) / 2, r, img)
    t9 = isblack(x9, y9, r, img)
    t7 = isblack((x9 + x2) / 2, (y9 + y2) / 2, r, img)
    t8 = isblack((x3 + x9) / 2, (y3 + y9) / 2, r, img)
    # CRC([t4, t5, t6, t7, t8, t9])
    return [1, 1, 1, t4, t5, t6, t7, t8, t9], t4*16 + \
        t5 * 8 + t6 * 4 + t7 * 2 + t8, CRC([t4, t5, t6, t7, t8, t9])


image = cv2.imread('./images/crc31.jpg')
img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
area = 100
img_gamma = gamma_trans(img, 1.5)  # gamma矫正
ret2, binary = cv2.threshold(
    img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # OTSU阈值处理  ret2 为计算出的阈值
binary = cv2.erode(binary, (3, 3))
binary = cv2.dilate(binary, (3, 3))
binary, contours, hierarchy = cv2.findContours(
    binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
roi_sum = []
for i in range(0, len(contours)):
    if cv2.contourArea(contours[i]) < area:
        continue

    rect = cv2.minAreaRect(contours[i])  # 最小外接矩形
    rate = min(rect[1][0], rect[1][1])
    if rate > 10 and rect[1][0] < binary.shape[0] / \
            4 and rect[1][0] < binary.shape[0] / 4:
        # cv2.drawContours(image, contours[i], -1, (255, 0, 0), thickness=2)
        # cv2.imshow('im',image)
        roi = transform(img, rect)  # 旋转roi
        # roi=binary[max(x-2,0):x+w+2,max(y-2,0):y+h+2]
        if (iscorner(roi)):
            roi_sum.append(contours[i])

if roi_sum:
    result = IOU(roi_sum)
    result = sort_three(result)  # 三个区域排序
    for it in range(len(result)):
        print(result[it][0])
    result = decoder(result, binary)

    print(result)
    cv2.imshow('result', image)
    cv2.waitKey(0)
