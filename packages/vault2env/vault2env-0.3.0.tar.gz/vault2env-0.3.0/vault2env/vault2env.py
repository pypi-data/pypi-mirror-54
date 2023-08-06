# -*- coding: utf-8 -*-

import hvac

"""Main module."""

def generate_env(vault_address, vault_token, path, output_filename):
  client = hvac.Client(url=vault_address, token=vault_token)
  result = client.read(path)
  if not result:
    raise ValueError("No secrets found")
  secrets = result['data']['data']
  with open(output_filename, 'w+') as filed:
    for key, value in secrets.items():
      new_line = f'{key} = {value}'
      print(f'Adding: {new_line}')
      filed.write(f'{new_line}\n')
