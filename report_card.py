# report_card.py

import json
from subjects import SUBJECTS

def generate_report(marked, answer_key, header, all_reports=None):
    """
    marked: لیست پاسخ‌های دانش‌آموز (مثل [1, 2, None, 3, ...])
    answer_key: کلید اصلی
    header: اطلاعات هدر (نام، شماره، مدرسه، ...)
    all_reports: لیست گزارش همه دانش‌آموزان برای محاسبه رتبه (اختیاری)
    """

    results = []

    for subj in SUBJECTS:
        start = subj["start"] - 1  # تبدیل به اندیس
        end = subj["end"]
        coef = subj["coefficient"]
        total = end - start

        correct = 0
        wrong = 0
        empty = 0

        for i in range(start, end):
            student_ans = marked[i]
            correct_ans = answer_key[i]

            if student_ans is None:
                empty += 1
            elif student_ans == correct_ans:
                correct += 1
            else:
                wrong += 1

        score = ((correct * 3 - wrong) / (total * 3)) * 100
        score_no_neg = (correct / total) * 100

        results.append({
            "name": subj["name"],
            "coefficient": coef,
            "total": total,
            "correct": correct,
            "wrong": wrong,
            "empty": empty,
            "score": round(score, 2),
            "score_without_negative": round(score_no_neg, 2),
            "school_rank": None,
            "province_rank": None,
            "school_top": None,
            "province_top": None
        })

    report = {
        "header": header,
        "results": results
    }

    if all_reports:
        report = calculate_ranks(report, all_reports)

    return report


def calculate_ranks(report, all_reports):
    for subject in report["results"]:
        name = subject["name"]
        score = subject["score"]
        school = report["header"].get("school")
        province = report["header"].get("province")

        # نمرات از همان مدرسه و درس
        school_scores = [
            s["score"] for r in all_reports
            for s in r["results"]
            if s["name"] == name and r["header"].get("school") == school
        ]

        province_scores = [
            s["score"] for r in all_reports
            for s in r["results"]
            if s["name"] == name and r["header"].get("province") == province
        ]

        subject["school_rank"] = sorted(school_scores, reverse=True).index(score) + 1 if school_scores else None
        subject["province_rank"] = sorted(province_scores, reverse=True).index(score) + 1 if province_scores else None
        subject["school_top"] = max(school_scores) if school_scores else None
        subject["province_top"] = max(province_scores) if province_scores else None

    return report


def save_report_json(report, output_dir="report_cards"):
    import os
    os.makedirs(output_dir, exist_ok=True)
    student_id = report["header"].get("student_id", "unknown")
    file_path = os.path.join(output_dir, f"{student_id}_report.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return file_path
