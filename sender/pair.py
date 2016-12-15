import requests

class Pair():
  def __init__(self):
    self.code = 123122
    
  def pair(self, code):
    return self.code

  def _send_request(self, code):
    requests.post("localhost:3000")