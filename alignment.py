# alignment.py

import cv2
import numpy as np

# مختصات مرجع مربع‌های فرم استاندارد (در تصویر ایده‌آل)
REFERENCE_POINTS = np.float32([
    [87, 63],        # بالا چپ
    [1696, 63],      # بالا راست
    [87, 2466],      # پایین چپ
    [1696, 2466]     # پایین راست
])

WARP_WIDTH = 1700   # عرض تصویر هدف (اختیاری، بر اساس فرم)
WARP_HEIGHT = 2500  # ارتفاع تصویر هدف

def align_form_using_markers(image):
    """
    تلاش برای پیدا کردن 4 مربع گوشه‌ای و اجرای perspective transform
    اگر موفق باشد، تصویر نرمال‌شده را برمی‌گرداند. اگر نه، None.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    # کوچک‌سازی نویزهای اطراف
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    clean = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # پیدا کردن کانتور مربع‌ها
    contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    marker_centers = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 900 < area < 1600:  # مربع‌هایی با اندازه حدود 31×31
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    marker_centers.append((cx, cy))

    if len(marker_centers) < 4:
        print(f"⚠️ فقط {len(marker_centers)} مارکر یافت شد. تصویر نادیده گرفته شد.")
        return None

    # انتخاب نزدیک‌ترین 4 نقطه به نقاط مرجع
    src_points = []

    for ref in REFERENCE_POINTS:
        closest = min(marker_centers, key=lambda p: np.linalg.norm(np.array(p) - ref))
        src_points.append(closest)

    src_points = np.float32(src_points)

    # محاسبه ماتریس تبدیل و اعمال warp
    dst_points = np.float32([
        [0, 0],
        [WARP_WIDTH - 1, 0],
        [0, WARP_HEIGHT - 1],
        [WARP_WIDTH - 1, WARP_HEIGHT - 1]
    ])

    M = cv2.getPerspectiveTransform(src_points, dst_points)
    warped = cv2.warpPerspective(image, M, (WARP_WIDTH, WARP_HEIGHT))

    return warped
