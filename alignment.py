import cv2
import numpy as np

REFERENCE_POINTS = np.float32([
    [87, 63],  # top left
    [1696, 63],  # top right
    [87, 2466],  # bottom left
    [1696, 2466]  # bottom right
])

WARP_WIDTH = 1700
WARP_HEIGHT = 2500


def align_form_using_markers(image):
    """
    تلاش برای پیدا کردن 4 مربع گوشه‌ای و اجرای perspective transform
    اگر موفق باشد، تصویر نرمال‌شده را برمی‌گرداند. اگر نه، None.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    clean = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    marker_centers = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 900 < area < 1600:
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    marker_centers.append((cx, cy))

    if len(marker_centers) < 4:
        print(f" فقط {len(marker_centers)} مارکر یافت شد. تصویر نادیده گرفته شد.")
        return None

    src_points = []

    for ref in REFERENCE_POINTS:
        closest = min(marker_centers, key=lambda p: np.linalg.norm(np.array(p) - ref))
        src_points.append(closest)

    src_points = np.float32(src_points)

    dst_points = np.float32([
        [0, 0],
        [WARP_WIDTH - 1, 0],
        [0, WARP_HEIGHT - 1],
        [WARP_WIDTH - 1, WARP_HEIGHT - 1]
    ])

    M = cv2.getPerspectiveTransform(src_points, dst_points)
    warped = cv2.warpPerspective(image, M, (WARP_WIDTH, WARP_HEIGHT))

    return warped
