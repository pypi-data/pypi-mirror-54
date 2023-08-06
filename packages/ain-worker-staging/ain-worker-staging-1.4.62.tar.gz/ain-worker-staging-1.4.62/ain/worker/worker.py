import subprocess
import dotenv
import requests_unixsocket
import os
import ain.common.constants as constants
from ain.worker.manager.ttyd import Ttyd
from ain.worker.manager.docker import Docker
import re

# Singleton pattern Class
class Worker():

  Instance = None

  def __init__(self):
    self.session = requests_unixsocket.Session()

  @staticmethod
  def getInstance():
    if Worker.Instance == None:
      Worker.Instance = Worker()
    return Worker.Instance

  def workerNameCheck(self, name):
    if re.match("^[a-zA-Z0-9_-]*$", name) and len(name) >= 5:
      return True
    else:
      return False

  def start(self, name, max_instance_count, price, mnemonic, description, server_ip, gpu):
    
    if (os.path.exists(constants.HOST_TTYD_PATH)):
      print("[!] You have to input 'sudo ain worker stop.'")
      return
    
    # check options
    if (price < 0): 
      print("[!] price must be greater then zero.")
      return

    if self.workerNameCheck(name) == False:
      print("The worker name ("+ name +") must be at least 5 characters long\n \
             and can be any combination of numbers, alphabets, '-' and '_' ")
      return

    optionsDict = {
      "NAME": name,
      "MAX_INSTANCE_COUNT": str(max_instance_count),
      "PRICE": str(price),
      "MNEMONIC": mnemonic,
      "DESCRIPTION": description,
      "SERVER_IP": server_ip,
      "GPU_BOOL": str(gpu)
    }

    for option in optionsDict:
      if optionsDict[option] == "":
        print('[-] "' + option + '" - empty')
        return
      dotenv.set_key(constants.WORKER_ENV_PATH, option, optionsDict[option])

    # open provider's ttys socket 
    ttydResult = Ttyd.createSocket(constants.HOST_TTYD_PATH)
    # open docker container for ain worker server
    if ttydResult: 
      Docker.createContainer(constants.IMAGE, optionsDict["GPU_BOOL"])

  def info(self): 
    try:
      response = self.session.get(constants.WORKER_SERVER_PATH + "/info")
      return response.json()['id']
    except Exception as e:
      print("[-] worker server error - info")
      return -1
    
  def status(self):
    # Option
    for option in constants.WORKER_ENVS:
      print("[Worker Option]")
      print(option + ": " + constants.WORKER_ENVS[option])
    
    # Worker Instance
    try:
      ids = self.info()
      if (ids == -1): return
      print("[+] Status: Running")
      print("Instance Count: " + str(len(ids)))
      if (len(ids) != 0):
        option = " ".join(ids)
        subprocess.run(["docker", "stats" , option])
    except Exception as e:
      print(e)
      return

  def stop(self):
    # send terminate message to Worker.
    try:
      response = self.session.get(constants.WORKER_SERVER_PATH + "/terminate")
    except Exception as e:
      print("[-] worker server error - terminate")

    # clean socket and Worker docker Container.
    Docker.removeContainer("ain_worker")
    Ttyd.removeSocket(constants.HOST_TTYD_PATH)
    Ttyd.removeSocket(constants.SHARED_PATH + "/ain_worker.sock")

  def log(self):
    basePath = constants.SHARED_PATH + "/log/"
    logFileName = sorted(os.listdir(basePath))[:-1]

    if (len(logFileName) == 0):
      print("[+] does not exist")
      return
    
    targetFile = logFileName[-1]
    
    print("[?] Do you want to see recent log?(y/n)")
    answer = input()
    if (answer == "n"):
      for i in range(len(logFileName)):
        print(str(i) + " - " + logFileName[i])
      print("[?] input number")
      number = int(input())
      targetFile = logFileName[number]
    
    try:
      path = os.path.join(basePath, targetFile)
      if (answer):
        subprocess.run(["tail", "-f" , path])
      else:
        subprocess.run(["cat", path])
    except Exception as e:
      print("[-] subprocess(log) error")
      print(e)
