#!/usr/bin/python3
import pyautogui
import random
import time
import os


if __name__ == "__main__":

  with open("mouse_m.txt","a") as f:
      p_currentMouseX, p_currentMouseY = pyautogui.position()
      time_p = time.time()
      while True:
          currentMouseX, currentMouseY = pyautogui.position()
          time_now = time.time()

          if currentMouseX != p_currentMouseX and currentMouseY != p_currentMouseY:
            print(currentMouseX, currentMouseY, time_now - time_p)
            f.write(f"{currentMouseX} {currentMouseY} {time_now - time_p}")
            f.write("\n")
            p_currentMouseX = currentMouseX
            p_currentMouseY = currentMouseY
            time_p = time_now

          time.sleep(0.05)