import cv2
import ocr
import datetime


def main():
    images = ocr.get_images()
    for image in images:
        start = datetime.datetime.now()

        print("[INFO]   Loading image...")
        img_src = cv2.imread(image)

        print("[INFO]   Image processing...")
        thresh = ocr.preprocess(img_src)
        date_matrix, ocr_img = ocr.split_matrix_str(thresh)
        char_img = ocr.ocr_preprocessing(ocr_img)
        rec_str = ocr.character_to_str(char_img)
        print("[INFO]   Identification Character...\n" +
                        '【' + rec_str + '】')
        print("[INFO]   Rebuilt the date matrix...")
        rec_code = ocr.dacode_dm(date_matrix)
        print("[INFO]   Date Matrix info is\n"+
                        '【' + rec_code + '】')
        if rec_code == rec_str:
            print("[INFO] Info check        |   SUCCESS!    |")
        else:
            print("[INFO] Info check        |   FAILURE!    |")

        end = datetime.datetime.now()
        print("[INFO]   Time: %3d ms" % ((end-start).total_seconds()*1000))
        print("*****************************************************")


if __name__ == '__main__':
    main()
