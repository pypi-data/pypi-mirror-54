import click
from ain.worker.main import Worker
import requests
import json
import ain.common.constants as constants

@click.group()
def call():
  pass

@call.command()
@click.argument("command", type=click.Choice(['start', 'stop', 'status', 'log', 'init', 'version', 'restart']))
@click.option('--name', default="", help="Ain Worker name")
@click.option('--max-instance-count', default="", help="maximum number of Instances")
@click.option('--price', default="", help="ain/h")
@click.option('--mnemonic', default="", help="mnemonic")
@click.option('--description', default="empty", help="description")
@click.option('--server-ip', default="empty", help="Cloud Server IP")
@click.option('--gpu', default="false", help="gpu")
def worker(command, name, max_instance_count, price, mnemonic, description, server_ip, gpu):

  optionRun = {
    'NAME': name,
    'LIMIT_COUNT': max_instance_count,
    'MNEMONIC': mnemonic,
    'PRICE': price,
    'DESCRIPTION': description,
    'GPU': gpu,
    'SERVER_IP': server_ip
  }

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
      print('[!] you have to input "sudo pip3 install --upgrade ain-worker"')
      return
  except Exception as e:
    print("[-] tracker server error")
    print(e)
    return 

  w = Worker()  
  if (command == "start"):
    w.start(optionRun)
  elif (command == "stop"):
    w.stop()
    exit(1)
  elif (command == "status"):
    w.status()
  elif (command == "log"):
    w.log()
  elif (command == "init"):
    w.init()
  elif (command == "version"):
    print(constants.VERSION)
  elif(command == "restart"):
    w.stop()
    w.start(optionRun)
    
if __name__ == '__main__':
  call()
