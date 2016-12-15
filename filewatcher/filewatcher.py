from . import watch

class FileWatcher():
  def watch_logs(self, path):
    for line in watch.watch(path):
      yield self.tokenize(line)
      
  def tokenize(self, row):
    timestamp, rest = row.split('  ')
    return [timestamp] + rest.split(',')