import os
import ain.common.constants as constants
import docker
import subprocess
from subprocess import Popen

class Docker():

  @staticmethod
  def createContainer(image, gpu):
    try:
      print("[+] pull image.")
      client = docker.from_env()
      client.images.pull(image)
      # noneRemoveCommands = 'docker rmi -f $(sudo docker images ainblockchain/ain-worker-staging | grep "<none>" | awk "{print $3}")'
      # Popen(noneRemoveCommands.split(" "), shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

      if gpu:
        runtime = "nvidia"
      else:
        runtime = None
      print("[+] create container.")
      client.containers.run(
        image=image,
        command="yarn start",
        detach=True,
        runtime=runtime,
        name="ain_worker",
        volumes={
          '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'ro'},
          constants.SHARED_PATH:{'bind': "/share", 'mode': "rw"}
        }
      )
        
      print("[+] started ain worker server!")
    except Exception as e:
      print("[-] failed to create container.")
      print(e)
      exit(1)

  @staticmethod
  def removeContainer(name):
    try:
      client = docker.from_env()
      constainer = client.containers.get(name)
      constainer.remove(force=True)
      
    except Exception as e:
      print("failed to remove container. - " + name)
      print(e)