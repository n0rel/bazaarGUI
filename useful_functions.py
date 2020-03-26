from PyQt5 import QtGui
import cv2


def qimage_of_item(item_name: str) -> QtGui.QImage:
    """Get item picture"""

    # If item has 'ENCHANTED' in the name, give the normal picture because
    # im too lazy to get the enchanted pictures
    if 'ENCHANTED' in item_name:
        item_name_split = item_name.split('_')[1:]
        img_src = f"item_icons/{'_'.join(item_name_split)}.png"
    else:
        img_src = f"item_icons/{item_name}.png"

    img = cv2.imread(img_src, cv2.IMREAD_UNCHANGED)
    img = cv2.imread('item_icons/NOT_FOUND.png', cv2.IMREAD_UNCHANGED) if img is None else img

    height, width, bytes = img.shape
    bytes_per_line = 3 * width
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB, img)

    return QtGui.QImage(img.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)