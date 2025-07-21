# layout.py

top_blocks = [
    ((86, 629), (302, 629)),
    ((371, 629), (587, 629)),
    ((656, 629), (871, 629)),
    ((940, 629), (1156, 629)),
    ((1222, 629), (1440, 629)),
    ((1509, 629), (1725, 629)),
]

block_height = 327
block_spacing = 9
blocks_per_column = 5
padding_top_bottom = 19
padding_left = 10

num_rows = 10
num_cols = 5
row_height = 17
row_spacing = 13

col_widths = [38, 26, 26, 26, 26]
col_spacings = [0, 6, 11, 13, 11]

def get_all_cells():
    """
    خروجی: لیست دیکشنری شامل مختصات دقیق تمام گزینه‌ها برای هر سوال
    فقط گزینه‌ها (A تا D) را برمی‌گرداند (ستون 0 = شماره سوال نادیده گرفته می‌شود)
    """
    cells = []
    question_number = 1

    for col_idx, ((x1, y1), (x2, _)) in enumerate(top_blocks):
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
                    x1_cell = int(x_cursor)
                    y1_cell = int(y_cell)
                    x2_cell = x1_cell + cell_w
                    y2_cell = y1_cell + row_height

                    if col >= 1:
                        cell_info = {
                            "question": question_number,
                            "option": col,  # A=1, B=2, C=3, D=4
                            "x1": x1_cell,
                            "y1": y1_cell,
                            "x2": x2_cell,
                            "y2": y2_cell
                        }
                        cells.append(cell_info)

                    x_cursor += cell_w

                question_number += 1

    return cells
