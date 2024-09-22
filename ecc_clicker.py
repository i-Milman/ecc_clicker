import pyautogui
import numpy as np
import cv2
import keyboard

def find_color(region, target_color, stop_key='ctrl', delay=100):
    # Установка области поиска
    x, y, width, height = region

    # Определение диапазона цвета в формате BGR
    target_color_bgr = np.array([target_color[2], target_color[1], target_color[0]])  # Конвертация RGB в BGR
    lower_bound = target_color_bgr - 10
    upper_bound = target_color_bgr + 10

    while True:
        # Управление циклом
        if keyboard.is_pressed(stop_key):
            print("Программа остановлена.")
            break
        cv2.waitKey(delay)

        # Получение изображения в указанной части экрана
        screenshot = pyautogui.screenshot(region=region)

        # Преобразование изображения в массив NumPy
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Создание маски для поиска цвета
        mask = cv2.inRange(img, lower_bound, upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Если цвет найден, кликаем по первому найденному объекту
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] > 200:
                cX = int(M["m10"] / M["m00"]) + x
                cY = int(M["m01"] / M["m00"]) + y
                pyautogui.moveTo(cX, cY)
                print(f"Мышь на цвете в ({cX}, {cY})")
            else:
                find_center(region)
        else:
            find_center(region)
        # pyautogui.click()


def find_center(region):
    x, y, width, height = region
    center_x = x + width // 2
    center_y = y + height // 2
    # pyautogui.click(center_x, center_y)
    pyautogui.moveTo(center_x, center_y)
    print(f"Цвет не найден, мышь в центре области ({center_x}, {center_y})")


if __name__ == "__main__":
    # Укажите область поиска: (x, y, ширина, высота)
    region = (420, 320, 600, 500)  # Область 320x320 пикселей, начиная с (335, 220)
    # Укажите целевой цвет: (R, G, B)
    target_color = (147, 88, 49)  # Коричневый цвет
    # target_color = (147, 147, 147)  # Серый цвет
    # target_color = (255, 172, 51)  # Жёлтый цвет

    find_color(region, target_color)
