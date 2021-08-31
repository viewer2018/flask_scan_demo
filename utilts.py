# coding=utf-8

import traceback
import numpy as np
import cv2
import os
import requests
import base64
import exifread
import StringIO

SUCCEED_BUT_NO_RESULT = 1000

#定义不会被切割的旋转图像函数
def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

# 定义旋转rotate函数
def rotate(image, angle, center=None, scale=1.0):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

#翻折函数
def flip(image):
    img = cv2.flip(image, 1)
    print(img.shape)
    return img


# 定义检测旋转角度的函数
def getRotate(image):
    new_f = StringIO.StringIO(image)
    # Return Exif tags
    tags = exifread.process_file(new_f)
    if not tags:
        return 0
    else:
        if 'Image Orientation' in tags:
            flag = tags['Image Orientation'].printable
            if flag == 'Rotated 90 CW':  # 图像顺时针旋转了90度
                return -90  # 还原图像，逆时针旋转90
            elif flag == 'Rotated 90 CCW':  # 图像逆时针旋转了90度
                return 90  #
            elif flag == 'Rotated 270 CCW':  # 图像逆时针旋转了270度
                return -90
            elif flag == 'Rotated 270 CW':  # 图像顺时针旋转了270度
                return 90
            elif flag == 'Rotated 180' or flag == 'Rotated 180 CCW' or flag == 'Rotated 180 CW':
                return 180
            else:
                return 0
        else:
            return 0


def download_image(img_url, logger=None):
    try:
        res = requests.get(url=img_url, timeout=5)
        if res.status_code == 200:
            return res.content
        else:
            if logger:
                logger.info("download image failed, img_url: %s, status_code: %d" % (img_url, res.status_code))
            else:
                print("download image failed, img_url: %s, status_code: %d" % (img_url, res.status_code))
            return None
    except Exception as e:
        if logger:
            logger.info("except occur when download image: %s, img_url: %s" % (traceback.format_exc(), img_url))
        else:
            print("except occur when download image: %s, img_url: %s" % (traceback.format_exc(), img_url))
        return None

def get_image(param, logger=None, type=0):
    """
    获取图像原始数据
    :param param: 图像的url 或者 base64 码流
    :param type: type=0, param 作为 图像的url, type=1, param 作为 base64 码流
    :return:
    """
    try:
        if 0 == type:
            return download_image(param, logger)
        elif 1 == type:
            return base64.b64decode(param)
        else:
            return None
    except Exception as e:
        if logger:
            logger.info("except occur in get_image: %s" % (traceback.format_exc()))
        else:
            print("except occur in get_image: %s" % (traceback.format_exc()))
        return None


def preprocess(image, logger=None, normal_size=None, is_bgr=True, need_char=True,correct_rotation=0,is_flip=0):
    """
    图片预处理，将网络传递过来的码流信息解码成图像，之后转换成C中的 char* 数据
    注意：需要将参数image 优先转成numpy的类型
    :param normal_size: 是否需要进行归一化操作
    :param is_bgr: 颜色通道是否是bgr, 若为false，那么就是rgb的顺序
    :param need_char: 是否需要转换成 unchar *
    :return:
    """
    angle = getRotate(image)
    np_data = np.array(bytearray(image))
    try:
        cv_image = cv2.imdecode(np_data, cv2.CV_LOAD_IMAGE_COLOR)
        # cv_image = cv2.imdecode(np_data,cv2.cv2.IMREAD_COLOR)#TODO
        if cv_image is None:
            if logger:
                logger.info("imdecode error")
            else:
                print("imdecode error")
            return None, None, None, None

        if angle != 0:
            cv_image = rotate(cv_image, angle)
        # add by qianyi
        # print("correctio rotation:"+str(correct_rotation))
        if int(correct_rotation) == 1:
            cv_image = rotate_bound(cv_image, 90)
            # print("rotated shun 90")
            logger.info("get correction info 1")
        if int(correct_rotation) == 2:
            cv_image = rotate_bound(cv_image, -90)
            # print("rotated ni 90")
            logger.info("get correction info 2")
            # print("")
        if int(correct_rotation) == 3:
            cv_image = rotate_bound(cv_image, 180)
            logger.info("get correction info 3")
        #翻折校正
        if int(is_flip)==1:
            cv_image = flip(cv_image)
            if logger:
                logger.info("flip image")
            else:
                print("flip image")

        height, width, channels = cv_image.shape
        if channels == 4:
            if is_bgr:
                res_image = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2BGR)
            else:
                res_image = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2RGB)
        elif channels == 3:
            if is_bgr:
                res_image = cv_image
            else:
                res_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        elif channels == 1:
            if is_bgr:
                res_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)
            else:
                res_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2RGB)
        else:
            return None, None, None, None
        if height == 0 or height is None or width == 0 or height is None or channels == 0 or channels is None:
            return None, None, None, None
        # 进行缩放转换
        if normal_size is not None:
            if width > height:
                ratio = float(normal_size) / float(width)
            else:
                ratio = float(normal_size) / float(height)
            width = int(width * ratio)
            height = int(height * ratio)
            res_image = cv2.resize(res_image, (width, height))

        if need_char:
            raw = res_image.tobytes()
            return raw, height, width, 3
        else:
            return res_image, height, width, 3
    except Exception as e:
        if logger:
            logger.info("except occur when decode image: %s" % (traceback.format_exc()))
        else:
            print("except occur when decode image: %s" % (traceback.format_exc()))
        return None, None, None, None
        
def get_os_system(param, logger=None, type=0):
    """
    获取图像原始数据
    :param param: 图像的url 或者 base64 码流
    :param type: type=0, param 作为 图像的url, type=1, param 作为 base64 码流
    :return:
    """
    try:
        if 0 == type:
            return os.system(param, logger)
        elif 1 == type:
            return base64.b64decode(param)
        else:
            return None
    except Exception as e:
        if logger:
            logger.info("except occur in get_image: %s" % (traceback.format_exc()))
        else:
            print("except occur in get_image: %s" % (traceback.format_exc()))
        return None