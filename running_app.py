#!/usr/bin/python3
import re
import subprocess

def findThisProcess(process_name):
  ps = subprocess.Popen("ps -A | grep "+process_name, shell=True, stdout=subprocess.PIPE)
  output = str(ps.stdout.read())
  ps.stdout.close()
  ps.wait()

  return output

def isThisRunning(process_name):
  output = findThisProcess(process_name)

  if re.search(process_name, output) is None:
    return False
  else:
    return True


if __name__ == "__main__":
    if isThisRunning('process') == False:
            print("Exist")
            exit()
    else:
            print("Not exist")
