# -*- coding: utf-8 -*-

"""Console script for vault2env."""
import argparse
import sys

from vault2env.vault2env import generate_env


def main():
    """Console script for vault2env."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', metavar="URL", help="Vault Address (https://vault.myco.com)", required=True)
    parser.add_argument('-t', metavar="Token", help="Vault Token - Token with enough access to read the KV-2 pairs for the .env", required=True)
    parser.add_argument('-p', metavar="Path", help="Path that contains the list of KV-2 pairs to generate the .env with", required=True)
    parser.add_argument('-o', metavar="Output File", help="Output filename", default=".env")
    args = parser.parse_args()

    generate_env(args.a, args.t, args.p, args.o)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
