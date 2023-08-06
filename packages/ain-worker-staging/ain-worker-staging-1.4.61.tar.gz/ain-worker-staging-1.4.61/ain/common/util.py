import ain.common.constants as constants
import requests
import json

def cliVersionCheck():
  MESSAGE = {
    "jsonrpc": "2.0",
    "method": "ain_checkCliVersion",
    "params": {
      "version": constants.VERSION
    },
    "id": 1
  }
  headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

  try:
    response = requests.post(constants.TRACKER_ADDR, data=json.dumps(MESSAGE), headers=headers)
    if (response.json()['result']['result'] != 0):
      return False
    return True
  except Exception as e:
    print("[-] tracker server error")
    print(e)
    return False