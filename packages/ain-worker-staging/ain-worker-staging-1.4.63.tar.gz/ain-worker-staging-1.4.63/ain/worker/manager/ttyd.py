import subprocess
from subprocess import Popen
import os
from time import sleep

class Ttyd():

  @staticmethod
  def createSocket(socketName):
    try:
      Popen(["ttyd" ,"-i" ,socketName ,"/bin/bash"], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      sleep(1)
      if (os.path.exists(socketName) == False):
        print("[-] failed to create ttyd socket.")
        return False
      
    except Exception as e:
      print("[-] failed to create ttyd socket.")
      print(e)
      return False
      
    print("[+] succeded to create ttyd socket.")
    return True

  @staticmethod
  def removeSocket(socketName):
    try:
      if (os.path.exists(socketName)):
        os.remove(socketName)
        print("[+] succeded to remove ttyd socket. - " + socketName)
    except Exception as e:
      print("[-] failed to remove ttyd socket. - " + socketName)
      print(e)