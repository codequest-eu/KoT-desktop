import requests

SERVER_ADDR = 'http://c8bb7b4c.ngrok.io'

class Sender:
  instance_id = -1
  code = -1
  def start_session(self, instance_id, start_time):
    if self.instance_id:
      return
    self.instance_id = instance_id

    r = requests.put("%s/game_sessions/%s/start" % (SERVER_ADDR, code), {
      instance_id: instance_id,
      start_time: start_time
    })

  def send_params(self, params):
    if not self.instance_id:
      return

    return params

  def pair(self, code):
    r = requests.put("%s/game_sessions/%s/pair" % (SERVER_ADDR, code))
    r.raise_for_status()
    self.code = code
    return r.json()