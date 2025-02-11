import os
import sys
import yaml
from argparse import ArgumentParser
from loguru import logger

import numpy as np
import pandas as pd

from pycaret.anomaly import setup, create_model, assign_model, save_model, load_model

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from constants import DATA_DIR, MODEL_DIR, LOG_DIR

class AnomalyDetectionModel:
    def __init__(self, data):
        self.data = data
        self.model = None
        self.setup_data()

    def setup_data(self):
        self.exp = setup(data=self.data, silent=True, session_id=123)

    def train_model(self, model_type='iforest'):
        self.model = create_model(model_type)
        self.results = assign_model(self.model)

    def save_model(self, model_name):
        save_model(self.model, model_name)

    def load_model(self, model_name):
        self.model = load_model(model_name)

    def predict(self, new_data):
        return assign_model(self.model, data=new_data)

def load_data(data_path):
    return pd.read_csv(data_path)

def train(data_path, model_id):
    print("Training the model...")
    data = load_data(data_path)
    anomaly_detector = AnomalyDetectionModel(data)
    anomaly_detector.train_model(model_type=model_id)
    anomaly_detector.save_model('anomaly_detector_model')


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument('--config_file', type=str, required=True, help='Path to the config file', default='config.yaml')
    args = argparser.parse_args()

    with open(args.config_file, 'r') as f:
        config = yaml.safe_load(f)

    data_path = os.path.join(DATA_DIR, config['data_path'])
    
    

    # train(args.data_path, args.model_id)

