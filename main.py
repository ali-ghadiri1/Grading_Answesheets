import os
import cv2
import numpy as np
import csv
from answer_key import answer_key

# تنظیمات فرم
NUM_QUESTIONS = 200
NUM_COLUMNS = 5
QUESTIONS_PER_COLUMN = 40
NUM_OPTIONS = 4  # A, B, C, D

def load_images_from_folder(folder):
    images = []
    filenames = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img = cv2.imread(os.path.join(folder, filename))
            if img is not None:
                images.append(img)
                filenames.append(filename)
    return images, filenames

def preprocess(image):
    image = cv2.resize(image, (800, 1100))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

def crop_answer_area(thresh):
    # مختصات جدول پاسخ‌ها - نیاز به تنظیم دقیق با توجه به تصویر واقعی
    x, y, w, h = 70, 230, 660, 830
    return thresh[y:y+h, x:x+w]

def split_questions(image):
    h, w = image.shape
    col_width = w // NUM_COLUMNS
    row_height = h // QUESTIONS_PER_COLUMN

    questions = []

    for col in range(NUM_COLUMNS):
        for row in range(QUESTIONS_PER_COLUMN):
            x_start = col * col_width
            y_start = row * row_height
            q_area = image[y_start:y_start + row_height, x_start:x_start + col_width]

            option_width = col_width // NUM_OPTIONS
            options_boxes = []
            for i in range(NUM_OPTIONS):
                x_opt = i * option_width
                opt_box = q_area[:, x_opt:x_opt + option_width]
                options_boxes.append(opt_box)

            questions.append(options_boxes)

    return questions

def get_marked_option(question_options):
    filled = [cv2.countNonZero(opt) for opt in question_options]
    min_val = min(filled)
    min_idx = filled.index(min_val)

    # آستانه تشخیص پاسخ صحیح
    if min_val < 0.7 * max(filled):
        return min_idx
    return None  # هیچ گزینه‌ای به‌صورت واضح پر نشده

def evaluate_answer_sheet(image, answer_key):
    thresh = preprocess(image)
    answer_area = crop_answer_area(thresh)
    questions = split_questions(answer_area)

    user_answers = []
    correct_count = 0

    for i, q in enumerate(questions):
        selected = get_marked_option(q)
        user_answers.append(selected)

        if selected is not None and i < len(answer_key):
            if selected == answer_key[i]:
                correct_count += 1

    return user_answers, correct_count

def main():
    images, filenames = load_images_from_folder("responses")

    with open("output.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ["Filename", "Score", "Total", "Unanswered"]
        writer.writerow(header)

        for img, name in zip(images, filenames):
            user_answers, score = evaluate_answer_sheet(img, answer_key)
            unanswered = sum(1 for ans in user_answers if ans is None)
            writer.writerow([name, score, len(answer_key), unanswered])

    print("✅ تصحیح کامل شد. خروجی در output.csv ذخیره شد.")

if __name__ == "__main__":
    main()
