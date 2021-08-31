import cv2
import numpy as np
import os


def cut(img):
    # crop image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    cnts, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = sorted(cnts, key=cv2.contourArea)[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    new_img = img[y:y + h, x:x + w]

    return new_img


def trans_bg(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    roi, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros(img.shape, img.dtype)

    cv2.fillPoly(mask, roi, (255,) * img.shape[2], )

    masked_image = cv2.bitwise_and(img, mask)

    return masked_image


def four_channels(img):
    height, width, channels = img.shape
    if channels < 4:
        new_img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        return new_img

    return img


def resize_to_1024(img):
    desired_size = 1024

    old_size = img.shape[:2]  # old_size is in (height, width) format

    if old_size[0] > desired_size:

        reducer = 920

        ratio = float(reducer) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        img = cv2.resize(img, (new_size[1], new_size[0]))

        delta_w = desired_size - new_size[1]
        delta_h = desired_size - new_size[0]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)

    else:
        delta_w = desired_size - old_size[1]
        delta_h = desired_size - old_size[0]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)

    new_im = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 252, 255])

    return new_im


def image_mask_resize(new_folder_name):
    image_path = "static/images_for_mask/" + new_folder_name
    save_image_path = "static/masked_images/" + new_folder_name
    
    os.mkdir(save_image_path)
    images = os.listdir(image_path)

    for image in images:
        s_img = cv2.imread(f"{image_path}/{image}", cv2.IMREAD_UNCHANGED)

        s_img = four_channels(s_img)

        s_img = cut(s_img)

        s_img = trans_bg(s_img)

        s_img = resize_to_1024(s_img)

        filename = image.split(".")[0] + '.png'
        cv2.imwrite(f"{save_image_path}/{filename}", s_img)
