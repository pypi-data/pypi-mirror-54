# -*- coding: utf-8 -*-
import sys

from requests.exceptions import RequestException
import hvac

"""Main module."""

def generate_env(vault_address, vault_token, path, output_filename):
  client = hvac.Client(url=vault_address, token=vault_token)

  # Attempt to read the secret from the given path
  try:
      result = client.read(path)
  except RequestException:
    print("Issue connecting to the specified Vault address")
    sys.exit(1)

  except hvac.exceptions.Forbidden:
    print("The provided token is not authenticated to access the secrets in Vault")
    sys.exit(2)

  if not result:
    print("No secrets found")
    sys.exit(3)

  secrets = result['data']['data']
  with open(output_filename, 'w+') as filed:
    for key, value in secrets.items():
      new_line = f'{key} = {value}'
      print(f'Adding: {new_line}')
      filed.write(f'{new_line}\n')
