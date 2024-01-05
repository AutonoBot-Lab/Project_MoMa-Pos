import pandas as pd
import numpy as np

def load_potential_map(csv_file):
    df = pd.read_csv(csv_file)
    potential_map = {}
    for x, y, energy in zip(df['X Coordinate'], df['Y Coordinate'], df['Potential Energy']):
        potential_map[(x, y)] = energy
    return potential_map

