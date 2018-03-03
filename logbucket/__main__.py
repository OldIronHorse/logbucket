import argparse
import yaml
from .logbucket import main

# main
parser = argparse.ArgumentParser(prog='logbucket')
parser.add_argument('-c', '--config', type=str, required=True,
                    help='path to configuration file (YAML)')
args = parser.parse_args()
with open(args.config, 'r') as config_file:
  cfg = yaml.load(config_file)
main(cfg)

