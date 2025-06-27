# extractor.py

import cv2
from layout import get_all_cells

def extract_marked_answers(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    cells = get_all_cells()
    total_questions = max(cell['question'] for cell in cells)
    answers = [None] * total_questions

    current_q = None
    current_options = []

    for cell in cells:
        q = cell['question']
        opt = cell['option']
        x1, y1, x2, y2 = cell['x1'], cell['y1'], cell['x2'], cell['y2']
        roi = thresh[y1:y2, x1:x2]

        total_pixels = roi.size
        dark_pixels = cv2.countNonZero(roi)
        fill_ratio = dark_pixels / total_pixels

        if q != current_q and current_q is not None:
            # تحلیل پاسخ سوال قبلی
            marked = [opt_i for opt_i, ratio in current_options if ratio > 0.5]
            answers[current_q - 1] = marked[0] if len(marked) == 1 else None
            current_options = []

        current_q = q
        current_options.append((opt, fill_ratio))

    # سوال آخر
    if current_q is not None:
        marked = [opt_i for opt_i, ratio in current_options if ratio > 0.5]
        answers[current_q - 1] = marked[0] if len(marked) == 1 else None

    return answers
