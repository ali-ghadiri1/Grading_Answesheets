# main.py

import cv2
import os
import zipfile
import shutil
from extractor import extract_marked_answers
from answer_key import get_answer_key, compare_with_key, NUM_ACTIVE_QUESTIONS
from layout import get_all_cells
from alignment import align_form_using_markers
from collections import defaultdict
from header_reader import read_header_fields, read_header_fields, draw_header_regions



TEMP_DIR = "unzipped"
OUTPUT_DIR = "graded"
ZIP_PATH = "uploads/uploaded.zip"

def draw_results_on_image(image, marked_answers, answer_key):
    output = image.copy()
    cells = get_all_cells()

    cell_map = defaultdict(dict)
    for cell in cells:
        q = cell['question']
        opt = cell['option']
        cell_map[q][opt] = (cell['x1'], cell['y1'], cell['x2'], cell['y2'])

    for q in range(1, len(answer_key) + 1):
        if q > NUM_ACTIVE_QUESTIONS:
            continue

        correct = answer_key[q - 1]
        marked = marked_answers[q - 1]

        if correct is None:
            continue

        if marked is not None:
            coords = cell_map[q].get(marked)
            if coords:
                color = (0, 200, 0) if marked == correct else (0, 0, 255)
                cv2.rectangle(output, coords[:2], coords[2:], color, 2)

        if marked != correct:
            coords = cell_map[q].get(correct)
            if coords:
                cv2.rectangle(output, coords[:2], coords[2:], (0, 165, 255), 2)

    return output

def process_all_from_zip():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(TEMP_DIR)

    image_files = []
    for root, _, files in os.walk(TEMP_DIR):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                full_path = os.path.join(root, f)
                image_files.append(full_path)

    if not image_files:
        print("⚠️ هیچ تصویری یافت نشد!")
        return

    answer_key = get_answer_key()

    for filepath in image_files:
        print(f"🔍 پردازش: {filepath}")
        image = cv2.imread(filepath)
        if image is None:
            print(f"❌ تصویر قابل خواندن نیست: {filepath}")
            continue

        # 🔁 نرمال‌سازی با ۴ مارکر
        aligned = align_form_using_markers(image)
        if aligned is None:
            print(f"⛔️ هم‌راستاسازی ممکن نبود: {filepath}")
            continue
        image = aligned  # تصویر نرمال‌شده را جایگزین می‌کنیم

        base_name = os.path.splitext(os.path.basename(filepath))[0]


        # ⬛️ فقط برای تست: کشیدن نواحی هدر
        header_test = draw_header_regions(image)
        test_out_path = os.path.join(OUTPUT_DIR, f"{base_name}_header_debug.jpg")
        cv2.imwrite(test_out_path, header_test)

        #خواندن هدر برگه
        header_data = read_header_fields(image)
        print("📋 اطلاعات سربرگ:")
        for k, v in header_data.items():
            print(f"  {k}: {v}")

        marked_answers = extract_marked_answers(image)
        correct, wrong, empty, _ = compare_with_key(marked_answers, answer_key)
        visual = draw_results_on_image(image, marked_answers, answer_key)

        base_name = os.path.splitext(os.path.basename(filepath))[0]
        out_path = os.path.join(OUTPUT_DIR, f"{base_name}_graded.jpg")
        cv2.imwrite(out_path, visual)
        print(f"✅ ذخیره شد: {out_path} (✔={correct} ✘={wrong} –={empty})")

if __name__ == "__main__":
    process_all_from_zip()
