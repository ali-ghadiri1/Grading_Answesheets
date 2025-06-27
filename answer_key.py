# answer_key.py
NUM_ACTIVE_QUESTIONS = 130
def get_answer_key():
    """
    خروجی: لیست 300تایی شامل عدد 1 تا 4 (برای گزینه A تا D) یا None
    فقط سوالات استفاده‌شده مقدار دارند (مثلاً 125 سوال اول)
    """
    raw = {
        1: 3, 2: 2, 3: 3, 4: 2, 5: 2, 6: 1, 7:2 , 8:3 , 9:2 , 10:4 , 11:1 , 12:2, 13:1 , 14:3 , 15:2, 16:4 , 17:4 , 18:3 , 19:2 ,
        20: 3, 21: 1, 22: 3, 23: 1, 24: 2, 25: 4
        # ... تا حداکثر 125 سوال
    }

    key = [None] * 300
    for q, val in raw.items():
        if 1 <= q <= NUM_ACTIVE_QUESTIONS and (val is None or val in [1, 2, 3, 4]):
            key[q - 1] = val
    return key

def compare_with_key(marked_answers, answer_key):
    correct = 0
    wrong = 0
    empty = 0
    results = []

    for i in range(len(answer_key)):
        correct_ans = answer_key[i]
        marked = marked_answers[i]

        if correct_ans is None:
            results.append(None)
            continue

        if marked == correct_ans:
            correct += 1
            results.append("✔")
        elif marked is None:
            empty += 1
            results.append("–")
        else:
            wrong += 1
            results.append("✘")

    return correct, wrong, empty, results
