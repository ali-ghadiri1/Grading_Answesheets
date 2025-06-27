# main.py

import cv2
import csv
from extractor import extract_marked_answers
from answer_key import get_answer_key, compare_with_key, NUM_ACTIVE_QUESTIONS
from layout import get_all_cells

def save_results_to_csv(name, correct, wrong, empty, answer_key, marked_answers):
    total_used = sum(1 for k in answer_key if k is not None)
    score = round(correct / total_used * 100, 2)

    with open("results.csv", mode="w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Correct", "Wrong", "Empty", "Score (%)"])
        writer.writerow([name, correct, wrong, empty, score])
        writer.writerow([])
        writer.writerow(["Q#", "Answer", "Marked", "Result"])
        for i in range(len(answer_key)):
            if answer_key[i] is not None:
                correct_ans = answer_key[i]
                marked = marked_answers[i]
                result = "✔" if marked == correct_ans else ("–" if marked is None else "✘")
                writer.writerow([i + 1, correct_ans, marked if marked else "", result])

def draw_results_on_image(image, marked_answers, answer_key):
    output = image.copy()
    cells = get_all_cells()

    # دسته‌بندی سلول‌ها بر اساس سوال
    from collections import defaultdict
    cell_map = defaultdict(dict)  # { سوال: { گزینه: مختصات } }

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

        # 📌 اگر گزینه‌ای انتخاب کرده
        if marked is not None:
            x1, y1, x2, y2 = cell_map[q].get(marked, (0, 0, 0, 0))
            if marked == correct:
                color = (0, 200, 0)  # ✔ درست
            else:
                color = (0, 0, 255)  # ✘ اشتباه
            cv2.rectangle(output, (x1, y1), (x2, y2), color, 2)

        # ✅ کشیدن گزینه صحیح (حتی اگر نزده یا اشتباه زده)
        if correct != marked:
            x1, y1, x2, y2 = cell_map[q].get(correct, (0, 0, 0, 0))
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 165, 255), 2)

    return output

def main():
    image_path = "responses/resp3.jpg"
    image = cv2.imread(image_path)
    if image is None:
        print("❌ تصویر یافت نشد:", image_path)
        return

    print("📥 تحلیل تصویر...")
    marked_answers = extract_marked_answers(image)
    answer_key = get_answer_key()

    correct, wrong, empty, results = compare_with_key(marked_answers, answer_key)
    save_results_to_csv("Student 1", correct, wrong, empty, answer_key, marked_answers)

    visual = draw_results_on_image(image, marked_answers, answer_key)
    cv2.imwrite("visual_result.jpg", visual)
    print("✅ خروجی تصویری ذخیره شد: visual_result.jpg")
    print("📊 نتیجه:", f"✔ {correct}  ✘ {wrong}  – {empty}")

if __name__ == "__main__":
    main()
