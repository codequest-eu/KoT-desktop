import time

def watch(filename):
  file = open(filename, 'r')
  file.seek(0, 2) # Go to the end of the file
  while True:
    line = file.readline()
    if not line:
        time.sleep(0.1) # Sleep briefly
        continue
    stripped_line = line.rstrip("\n").rstrip("\r")
    if not stripped_line:
        continue
    yield line.rstrip("\n").rstrip("\r")