import pytesseract
import cv2

HEADER_FIELDS = {
    "full_name":      (717, 295, 717 + 366, 295 + 45),
    "school":         (726, 372, 726 + 465, 372 + 34),
    "seat_number":    (808, 431, 808 + 307, 431 + 40),
    "grade":          (129, 297, 129 + 484, 297 + 47),
    "city":           (406, 371, 406 + 190, 371 + 43),
    "province":       (117, 365, 117 + 188, 365 + 46),
    "exam_number":    (395, 433, 395 + 194, 433 + 35),
    "student_id":     (98, 432, 98 + 140, 432 + 40)
}


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_header_fields(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = {}

    for key, (x1, y1, x2, y2) in HEADER_FIELDS.items():
        roi = gray[y1:y2, x1:x2]

        if key == "student_id":
            text = pytesseract.image_to_string(roi, lang='eng', config='--psm 7').strip()
        else:
            text = pytesseract.image_to_string(roi, lang='fas', config='--psm 6').strip()

        data[key] = text

    return data




def draw_header_regions(image):
    """
     رسم مستطیل روی نواحی header جهت تست ناحیه‌بندی
    """
    output = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    for idx, (key, (x1, y1, x2, y2)) in enumerate(HEADER_FIELDS.items(), start=1):
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(output, f"{idx}", (x1, y1 - 5), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    return output

