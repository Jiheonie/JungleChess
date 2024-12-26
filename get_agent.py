from dljungle.encoders.base import get_encoder_by_name
from dljungle.agent import pg
import h5py
import numpy as np
import argparse

from keras.api.models import load_model

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--model', '-m')
  parser.add_argument('output_file')
  args = parser.parse_args()
  output_file = args.output_file

  args = parser.parse_args()
  
  encoder = get_encoder_by_name('oneplane')
  model = load_model(args.model)
  new_agent = pg.PolicyAgent(model, encoder)

  with h5py.File(output_file, 'w') as outf:
    new_agent.serialize(outf)

if __name__ == '__main__':
  main()