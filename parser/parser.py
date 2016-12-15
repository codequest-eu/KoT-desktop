import requests
from datetime import datetime
from .params import *

class Parser():
  def __init__(self):
    self.code = 123122
    
  def parse(self, entry):
    timestamp, event, *rest = entry
    if event.endswith('_DAMAGE'):
      return self.parse_damage(event, entry)
    else:
      return self.parse_common(entry)

  def parse_common(self, entry):
    return dict(zip(COMMON_PARAMS, entry))

  def parse_damage(self, event, entry):
    if event == 'SWING_DAMAGE':
      PARAMS = COMMON_PARAMS + DAMAGE_PARAMS
    else:
      PARAMS = COMMON_PARAMS + NON_SWING_PARAMS + DAMAGE_PARAMS
    obj = dict(zip(PARAMS, entry))
    obj['source'] = self.parse_guid(obj['source_guid'])
    obj['source'].update(self.parse_name(obj['source_name']))
    obj['dest'] = self.parse_guid(obj['dest_guid'])
    obj['dest'].update(self.parse_name(obj['dest_name']))
    self.convert_to_ints(obj)
    self.convert_to_ints(obj['dest'])
    self.convert_to_ints(obj['source'])
    return obj

  def parse_guid(self, guid):
    s_guid = guid.split('-')
    if s_guid[0] == 'Player':
      return dict(zip(PLAYER_PARAMS, s_guid))
    elif s_guid[0] == 'Item':
      return dict(zip(ITEM_PARAMS, s_guid))
    return dict(zip(CREATURE_PARAMS, s_guid))

  def parse_name(self, name):
    PARAMS = ['name', 'server_name']
    return dict(zip(PARAMS, name.strip("\"").split('-')))

  def convert_to_ints(self, entry):
    for key, value in entry.items():
      if key.endswith("_id") or key == 'zone_uid':
        entry[key] = int(value)