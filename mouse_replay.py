#!/usr/bin/python3
import pyautogui
import time


if __name__ == "__main__":

    lines_from_file = open(
        "mouse_m.txt",
        "r",
    ).readlines()
    target_one_x = 840
    target_one_y = 640
    target_double1_x = 1320
    target_double1_y = 644
    target_double2_x = 362
    target_double2_y = 644
    click = False
    for line in lines_from_file:
        mouseX, mouseY, m_delay = line.split()
        mouseX = int(mouseX)
        mouseY = int(mouseY)
        time.sleep(float(m_delay))
        pyautogui.moveTo(mouseX, mouseY)
        x_approve = (
            (mouseX >= target_one_x - 5 and mouseX <= target_one_x + 5)
            or (
                mouseX >= target_double1_x - 5
                and mouseX <= target_double1_x + 5
            )
            or (
                mouseX >= target_double2_x - 5
                and mouseX <= target_double2_x + 5
            )
        )
        y_approve = (
            (mouseY >= target_one_y - 5 and mouseY <= target_one_y + 5)
            or (
                mouseY >= target_double1_y - 5
                and mouseY <= target_double1_y + 5
            )
            or (
                mouseY >= target_double2_y - 5
                and mouseY <= target_double2_y + 5
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
