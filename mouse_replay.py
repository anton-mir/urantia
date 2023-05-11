#!/usr/bin/python3
import pyautogui
import time

# to track mouse use pyautogui.mouseInfo()


if __name__ == "__main__":

    lines_from_file = open(
        "mouse_m.txt",
        "r",
    ).readlines()
    target_left_x = 360 # left
    target_left_y = 640
    target_center_x = 840 # center
    target_center_y = 640
    target_right_x = 1330 # right
    target_right_y = 640
    click = False
    for line in lines_from_file:
        mouseX, mouseY, m_delay = line.split()
        mouseX = int(mouseX)
        mouseY = int(mouseY)
        time.sleep(float(m_delay))
        pyautogui.moveTo(mouseX, mouseY)
        x_approve = (
            (mouseX >= target_center_x - 5 and mouseX <= target_center_x + 5)
            or (
                mouseX >= target_right_x - 5
                and mouseX <= target_right_x + 5
            )
            or (
                mouseX >= target_left_x - 5
                and mouseX <= target_left_x + 5
            )
        )
        y_approve = (
            (mouseY >= target_center_y - 5 and mouseY <= target_center_y + 5)
            or (
                mouseY >= target_right_y - 5
                and mouseY <= target_right_y + 5
            )
            or (
                mouseY >= target_left_y - 5
                and mouseY <= target_left_y + 5
            )
        )
        print(mouseX, mouseY, x_approve, y_approve, click)
        if x_approve and y_approve:
            if click == False:
                pyautogui.click()
                print("CLICK!")
                click = True
        elif not x_approve and not y_approve:
            click = False
