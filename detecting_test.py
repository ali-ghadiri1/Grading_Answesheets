import cv2
import numpy as np

# 📌 بارگذاری تصویر اصلی
img = cv2.imread("responses/resp2.jpg")
if img is None:
    print("❌ تصویر پیدا نشد.")
    exit()

output = img.copy()
alpha = 0.35  # شفافیت رنگ‌ها

# 🎨 رنگ‌ها [شماره، A, B, C, D]
colors = [
    (160, 160, 160),  # شماره سوال (خاکستری)
    (255, 0, 0),      # A - قرمز
    (0, 0, 255),      # B - آبی
    (0, 255, 255),    # C - زرد
    (50, 50, 50)      # D - مشکی
]

# 📍 مختصات بالا چپ و راست هر ستون از ردیف اول
top_blocks = [
    ((86, 629), (302, 629)),
    ((371, 629), (587, 629)),
    ((656, 629), (871, 629)),
    ((940, 629), (1156, 629)),
    ((1222, 629), (1440, 629)),
    ((1509, 629), (1725, 629)),
]

# 🧩 مشخصات کلی
block_height = 327
block_spacing = 9
blocks_per_column = 5

# تنظیمات داخل هر بلوک
padding_top_bottom = 19
padding_right = 7
padding_left = 10  # ← اصلاح برای جابجایی ۷px به چپ

num_rows = 10
num_cols = 5

row_height = 17
row_spacing = 13  # فاصله بین ردیف‌ها

col_widths = [38, 26, 26, 26, 26]      # شماره، A-D
col_spacings = [0, 6, 11, 13, 11]     # فاصله بین ستون‌ها (C-D اصلاح شد)

question_number = 1
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.45
thickness = 1

# 🔄 ترسیم برای هر ستون و بلوک
for col_idx, ((x1, y1), (x2, _)) in enumerate(top_blocks):
    block_w = x2 - x1

    for blk in range(blocks_per_column):
        y_top = y1 + blk * (block_height + block_spacing)
        area_top = y_top + padding_top_bottom
        area_left = x1 + padding_left

        for row in range(num_rows):
            y_cell = int(area_top + row * row_height + row * row_spacing if row > 0 else area_top)

            x_cursor = area_left
            for col in range(num_cols):
                if col > 0:
                    x_cursor += col_spacings[col]

                cell_w = col_widths[col]
                top_left = (int(x_cursor), int(y_cell))
                bottom_right = (int(x_cursor + cell_w), int(y_cell + row_height))

                color = colors[col % len(colors)]
                overlay = output.copy()
                cv2.rectangle(overlay, top_left, bottom_right, color, -1)
                cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

                # ✅ چاپ شماره سوال در ستون 0 (وسط‌چین و قرمز)
                if col == 0:
                    text = str(question_number)
                    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
                    text_x = top_left[0] + (cell_w - text_width) // 2
                    text_y = top_left[1] + (row_height + text_height) // 2 - 2  # کمی اصلاح پایین

                    cv2.putText(
                        output,
                        text,
                        (text_x, text_y),
                        font,
                        font_scale,
                        (0, 0, 255),  # 🔴 قرمز
                        thickness,
                        cv2.LINE_AA
                    )

                x_cursor += cell_w

            question_number += 1

# ذخیره نهایی
cv2.imwrite("cell_layout_with_centered_qnums.jpg", output)
print("✅ شماره سوال‌ها قرمز و وسط‌چین شدند. ذخیره شد: cell_layout_with_centered_qnums.jpg")

