import cv2
import numpy as np

# 📌 خواندن تصویر واقعی (بدون resize)
img = cv2.imread("responses/resp2.jpg")
if img is None:
    print("❌ تصویر پیدا نشد.")
    exit()

output = img.copy()
alpha = 0.35  # شفافیت

# 🎨 رنگ‌ها (BGR)
colors = [
    (255, 0, 0),    # آبی
    (0, 0, 255),    # قرمز
    (0, 255, 255),  # زرد
    (50, 50, 50)    # مشکی
]

# مختصات بالا-چپ و بالا-راست بلوک‌های ردیف اول
top_blocks = [
    ((86, 629), (302, 629)),
    ((371, 629), (587, 629)),
    ((656, 629), (871, 629)),
    ((940, 629), (1156, 629)),
    ((1222, 629), (1440, 629)),
    ((1509, 629), (1725, 629)),
]

block_height = 956 - 629     # 327px
block_spacing = 9            # ✅ کاهش فاصله برای جا گرفتن بلوک پنجم
blocks_per_column = 5        # ۵ ردیف بلوک

# ترسیم بلوک‌ها
for col_idx, ((x1, y1), (x2, _)) in enumerate(top_blocks):
    block_w = x2 - x1

    for blk in range(blocks_per_column):
        y_top = y1 + blk * (block_height + block_spacing)
        y_bottom = y_top + block_height

        top_left = (x1, y_top)
        bottom_right = (x1 + block_w, y_bottom)

        color_index = (col_idx + blk) % len(colors)
        color = colors[color_index]

        # ترسیم با شفافیت
        overlay = output.copy()
        cv2.rectangle(overlay, top_left, bottom_right, color, -1)
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

# ذخیره خروجی
cv2.imwrite("blocks_final_fixed_spacing.jpg", output)
print("✅ تصویر نهایی با فاصله عمودی 9px ذخیره شد: blocks_final_fixed_spacing.jpg")
