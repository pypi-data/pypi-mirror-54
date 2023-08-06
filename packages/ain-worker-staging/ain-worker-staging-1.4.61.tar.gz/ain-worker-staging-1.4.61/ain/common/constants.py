import os 
import dotenv

# Common
ROOT_PATH = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])
CLI_ENVS = dotenv.dotenv_values(ROOT_PATH + "/env.development")
VERSION = CLI_ENVS["VERSION"]
TRACKER_ADDR = "https://" + CLI_ENVS["SERVER_ADDR"] + "/tracker/"
CLI_NAME = CLI_ENVS["CLI_NAME"]


# Worker
SHARED_PATH = ROOT_PATH + "/share"
WORKER_ENV_PATH = SHARED_PATH + "/worker.env"
if (CLI_NAME == "ain-worker"):
    IMAGE = "ainblockchain/ain-worker:latest"
else:
    IMAGE = "ainblockchain/ain-worker-staging:latest"

WORKER_ENVS = dotenv.dotenv_values(WORKER_ENV_PATH)
HOST_TTYD_PATH = SHARED_PATH + "/ain_worker_ttyd.sock"
WORKER_SERVER_PATH = "http+unix://" + SHARED_PATH.replace("/", '%2F') + "%2Fain_worker.sock"