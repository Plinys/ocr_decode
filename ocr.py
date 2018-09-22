import glob
import cv2
import numpy as np
import tesserocr
from PIL import Image
from pylibdmtx.pylibdmtx import decode

Debugwindow = False

'''-------get image from the 'img' folder--------'''
def get_images():
    images = glob.glob(r'.\img\*.bmp')
    if (images):
        print ("【GET IMAGES SUCCESS】")
    else:
        print("【FAIL TO GET IMAGES】 can't find .bmp file")
    return images

'''------image preprocessing :convert to gray, threshold, medianblur to get feature------'''
def preprocess(img_src):
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    thresh = cv2.medianBlur(thresh, 13)     # noise removal
    if Debugwindow:
        show_debug_windows("thresh_debug", thresh)
    return thresh

'''--------show correlate image when debug---------'''
def show_debug_windows(str, img):
    cv2.namedWindow(str, cv2.WINDOW_NORMAL)
    cv2.imshow(str, img)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()

'''--------from the srouce image split the character and date matrix--------'''
def split_matrix_str(img):
    kernal = np.ones((40,40), np.uint8)
    dilation = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernal)
    _, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = cv2.boundingRect(contours[-1])
    date_matrix = img[y+20:y+h-20, x+30:x+w-30]
    ocr_img = img.copy()
    ocr_img[y:y+h, x:x+h] = [0]

    if Debugwindow:
        img_clone = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2BGR)
        rect_matrix = cv2.rectangle(img_clone, (x,y), (x+w,y+h), (0,255,0), 2)
        show_debug_windows("rect_matrix_debug", rect_matrix)
        show_debug_windows("date_matrix_debug", date_matrix)
        show_debug_windows("ocr_img_debug", ocr_img)

    return date_matrix, ocr_img

'''------preprocess for the part of characters, get single char-------'''
def ocr_preprocessing(ocr_img):
    rect_list = []
    kernal = np.ones((15,7), np.uint8)
    dilate = cv2.morphologyEx(ocr_img, cv2.MORPH_DILATE, kernal)
    # show_debug_windows("char_dilate_debug", dilate)
    _, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        x = x - 8
        y = y - 15
        w = w + 16
        h = h + 30
        rect_list.append([x,y,w,h])

        # if Debugwindow:
        #     rect_str = dilate.copy()
        #     rect_str = cv2.cvtColor(rect_str, cv2.COLOR_GRAY2BGR)
        #     cv2.rectangle(rect_str, (x,y), (x+w, y+h), (0,255,255), 3)
        #     show_debug_windows("rect_around_str_debug", rect_str)

    rect_list = sorted(rect_list, key = lambda y:y[1])
    line1 = sorted(rect_list[0:7], key = lambda x:x[0])
    line2 = sorted(rect_list[7:14], key = lambda x:x[0])
    rect_list = line1 + line2
    char_img = []
    for (x,y,w,h) in rect_list:
        temp = dilate[y:y+h, x:x+w]
        char_img.append(temp)

    if Debugwindow:
        rect_str = dilate.copy()
        rect_str = cv2.cvtColor(rect_str, cv2.COLOR_GRAY2BGR)
        for (x,y,w,h) in rect_list:
            cv2.rectangle(rect_str, (x,y), (x+w, y+h), (0,255,255), 3)
            show_debug_windows("rect_around_str_debug", rect_str)

    return char_img


def character_to_str(char_img):
    rec_str = ""
    char_type = ['ALP', 'ALP', 'ALP', 'ALP', 'DIG', 'ALP', 'DIG',
                 'ALP', 'ALP', 'DIG', 'DIG', 'DIG', 'ALP', 'DIG']
    with tesserocr.PyTessBaseAPI(psm=tesserocr.PSM.SINGLE_CHAR, path=r'D:\install\Tesseract-OCR\tessdata') as api:
        for index, temp_img in enumerate(char_img):
            cfg = ''
            if char_type[index] == 'ALP':
                cfg = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            elif char_type[index] == 'DIG':
                cfg = "1234567890"

            temp_img = Image.fromarray(temp_img)
            api.SetVariable("tessedit_char_whitelist", cfg)
            api.SetImage(temp_img)
            result_char = api.GetUTF8Text()
            result_char = result_char.replace("\n", "")
            if len(result_char) == 0:
                result_char = "_"
            rec_str = rec_str + result_char
        if len(rec_str)==0:
            print("[ERROR INFO]     can't Identification the Character")
    return rec_str


def dacode_dm(dm_img):
    grid_w = 10
    dm_img = cv2.resize(dm_img, (grid_w * 18, grid_w * 18), interpolation=cv2.INTER_CUBIC)
    #show_debug_windows("date_matrix", dm_img)
    im_gen = np.ones((grid_w * 18, grid_w * 18), dtype=np.uint8)
    im_gen = im_gen * 255

    for i in range(18):
        for j in range(18):
            x, y = j *grid_w, i * grid_w
            area = 0
            temp = dm_img[y:y+grid_w, x:x+grid_w]
            _, contours, hierarchy = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if (len(contours) > 0):
                cnt_sorted = sorted(contours, key=len)
                area = cv2.contourArea(cnt_sorted[-1])
            else:
                area = 0
            if area > 0.45 * grid_w * grid_w or j == 0 or i == 17:
                im_gen[y:y+grid_w, x:x+grid_w] = [0]
    dm_new = np.ones((28*grid_w, 28*grid_w), dtype=np.uint8)
    dm_new = 255 * dm_new
    dm_new[5*grid_w : 23*grid_w, 5*grid_w:23*grid_w] = im_gen
    rst = decode(dm_new, timeout=100)
    dm_str = ''
    if len(rst)==0:
        print("[ERROR INFO]     Unable to decode DM code")
    else:
        dm_str = str(rst[0][0]).split("'")[1]
        dm_str = dm_str.replace(" ", "")

    if Debugwindow:
        show_debug_windows("date_matrix", dm_img)
        show_debug_windows("rebuilt_dm", dm_new)
    return dm_str
