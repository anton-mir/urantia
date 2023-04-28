#!/usr/bin/python3
import pyautogui
import random
import time


def move_to_flag(target_x, target_y):
    currentMouseX, currentMouseY = pyautogui.position()
    counter = 0
    speed = random.randint(2, 5)
    x_approve = currentMouseX>=target_x-5 and currentMouseX<=target_x+5
    y_approve = currentMouseY>=target_y-5 and currentMouseY<=target_y+5
    while (not x_approve) or (not y_approve):
      if counter%20 == 0:
        speed = random.randint(2, 5)

      if currentMouseX > target_x:
        move_x = (-speed)
      elif currentMouseX < target_x:
        move_x = speed
      else:
        move_x = 0

      if currentMouseY > target_y:
        move_y = (-speed)
      elif currentMouseY < target_y:
        move_y = speed
      else:
        move_y = 0

      pyautogui.moveRel(move_x, move_y, duration=0)
      currentMouseX, currentMouseY = pyautogui.position()
      x_approve = currentMouseX>=target_x-5 and currentMouseX<=target_x+5
      y_approve = currentMouseY>=target_y-5 and currentMouseY<=target_y+5
      print(f"{counter}::{currentMouseX}/{target_x}:{currentMouseY}/{target_y} --> move:{move_x}/{move_y} --> approve: {x_approve}/{y_approve}")
      counter+=1
    print("DONE!")
    pyautogui.click()


if __name__ == "__main__":
  while True:
      x_in = random.randint(840, 850)
      y_in = random.randint(635, 645)
      x_out = random.randint(1, 1800)
      y_out = random.randint(1, 1000)
      move_to_flag(x_in, y_in)

      time.sleep(random.randint(100, 1000)/1000)

      for i in range(5,10):
        print(i)
        x_in = random.randint(840, 850)
        y_in = random.randint(635, 645)
        move_to_flag(x_in, y_in)
        time.sleep(0.05)

      time.sleep(random.randint(300, 3000)/1000)
      move_to_flag(x_out, y_out)
      time.sleep(random.randint(300, 3000)/1000)