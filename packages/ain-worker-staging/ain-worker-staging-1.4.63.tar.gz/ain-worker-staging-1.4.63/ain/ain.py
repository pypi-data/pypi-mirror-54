import click
from ain.worker.worker import Worker
import ain.common.constants as constants
import ain.common.util as util

@click.group()
def call():
	# check CLI version
	if util.cliVersionCheck() == False:
		click.echo('[!] You have to input "sudo pip3 install --upgrade ' + constants.CLI_NAME + '".')
		return

@call.command()
@click.argument("command", type=click.Choice(['start', 'stop', 'status', 'log', 'init', 'version', 'restart']))
@click.option("--name", "-n", "name", default=constants.WORKER_ENVS["NAME"], help="Ain Worker Name", type=str)
@click.option("--max-instance-count", "-m", "max_instance_count", default=constants.WORKER_ENVS["MAX_INSTANCE_COUNT"], help="Maximum number of Instances", type=int)
@click.option("--price", "-p", "price", default=constants.WORKER_ENVS["PRICE"], help="ain/h Price", type=float)
@click.option("--mnemonic", "-m", "mnemonic", default=constants.WORKER_ENVS["MNEMONIC"], help="mnemonic", type=str)
@click.option("--description", "-d", "description", default=constants.WORKER_ENVS["DESCRIPTION"], help="Description", type=str)
@click.option("--server-ip", "-s", "server_ip", default=constants.WORKER_ENVS["SERVER_IP"], help="Server IP", type=str)
@click.option("--gpu", "-g", "gpu", default=constants.WORKER_ENVS["GPU_BOOL"], help="Use GPU (true or false)", type=str)
def worker(command, name, max_instance_count, price, mnemonic, description, server_ip, gpu):
	workerInstance = Worker.getInstance()

	if (command == "start"):
		print("[?] Do you want to start? (y/n)")
		if (input().lower() == 'y'):
			workerInstance.start(name, max_instance_count, price, mnemonic, description, server_ip, gpu)
	elif(command == "restart"):
		info = workerInstance.info()
		if (info != -1):
			print("[+] Instance count:" + str(len(info)))
		print("[?] Do you want to restart? (y/n)")
		if (input().lower() == 'y'):
			workerInstance.stop()
			workerInstance.start(name, max_instance_count, price, mnemonic, description, server_ip, gpu)
	elif (command == "stop"):
		info = workerInstance.info()
		if (info != -1):
			print("[+] Instance count:" + str(len(info)))
		print("[?] Do you want to stop? (y/n)")
		if (input().lower() == 'y'):
			workerInstance.stop()
	elif (command == "log"):
		workerInstance.log()
	elif (command == "init"):
		workerInstance.init()
	elif (command == "status"):
		workerInstance.status()
	elif (command == "version"):
		click.echo(constants.VERSION)
		
if __name__ == '__main__':
	call()
