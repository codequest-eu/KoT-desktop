from sender import Sender
from filewatcher import FileWatcher
from parser import Parser
from handler import Handler
import pprint

LOGS_PATH = '/Applications/World of Warcraft/Logs/WoWCombatLog.txt'

def main():

  file_watcher = FileWatcher()
  parser = Parser()
  sender = Sender()

  pp = pprint.PrettyPrinter(indent=4)

  print("\33c")
  print(" _  __                                      __   _____ _")
  print("| |/ /___  ___ _ __   ___ _ __ ___    ___  / _| |_   _(_)_ __ ___   ___") 
  print("| ' // _ \/ _ \ '_ \ / _ \ '__/ __|  / _ \| |_    | | | | '_ ` _ \ / _ \\")
  print("| . \  __/  __/ |_) |  __/ |  \__ \ | (_) |  _|   | | | | | | | | |  __/")
  print("|_|\_\___|\___| .__/ \___|_|  |___/  \___/|_|     |_| |_|_| |_| |_|\___|")
  print("              |_|                                                       \n")
  print("                                Welcome!                                 \n")
  
  while True:
    pair_key = input("Type your pairing key: ")
    try:
      response = sender.pair(pair_key)
      zone_id, boss_ids = map(response.get, ('zone_wow_id', 'boss_wow_ids'))
      break
    except Exception as e:
      print('Error ocurred %s' % e)
  print ("Successfully paired for zone %d [%s]" % (zone_id, ", ".join(map(str,boss_ids))))

  handler = Handler(sender, zone_id, boss_ids)

  print("Watching %s for changes..." % LOGS_PATH)

  for combat_log_entry in file_watcher.watch_logs(LOGS_PATH):
    try:
      parsed_params = parser.parse(combat_log_entry)
      handler.handle(parsed_params)
    except Exception:
      pp.pprint(combat_log_entry)
      continue

if __name__ == '__main__':
  main()