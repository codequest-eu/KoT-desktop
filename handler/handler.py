import requests

class Handler:
  instance_id = -1
  def __init__(self, sender, zone_uid, bosses):
    self.sender = sender
    self.zone_uid = zone_uid
    self.bosses = bosses

  def handle(self, params):
    npc = self.get_npc(params)
    import pdb; pdb.set_trace()
    if not npc:
      return
    if self.instance_id == -1:
      if npc['zone_uid'] != self.zone_uid:
        return
      self.start_session(npc['instance_id'])
    if npc['instance_id'] != self.instance_id:
      return
    self.handle_event(params)

  def handle_event(self, params):
    if params['type'].endswith('_DAMAGE'):
      self.handle_damage(params)
    elif params['type'] == 'UNIT_DIED':
      self.handle_death(params)
    else:
      return

  def start_session(self, instance_id):
    print('Stared session with instance id: %s' % instance_id)
    self.instance_id = instance_id
    self.sender.start_session(instance_id)

  def get_npc(self, params):
    if ('dest' in params) and params['dest']['type'] == 'Creature':
      return params['dest']
    elif ('source' in params) and params['source']['type'] == 'Creature':
      return params['source']
    else:
      return

  def handle_damage(self, params):
    if params['source']['type'] != 'Player':
      return
    if params['dest']['npc_id'] not in self.bosses:
      return
    print('Handling boss... %d' % params['dest']['npc_id'])
    return self.sender.send_params(self.format_params(params))

  def handle_death(self, params):
    if params['dest']['npc_id'] not in self.bosses:
      return
    print('Handling boss death... %d' % params['dest']['npc_id'])
    return self.sender.send_params(self.format_params(params))
    
  def format_params(self, params):
    return {
      'event_timestamp': params['timestamp'],
      'server_wow_id': params['dest']['server_id'],
      'instance_wow_id': params['dest']['instance_id'],
      'zone_wow_id': params['dest']['zone_uid'],
      'npc_wow_id': params['dest']['npc_id'],
      'wow_event': params['type'],
      'player_wow_id': params['source']['player_uid']
    }