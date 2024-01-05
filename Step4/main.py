from data_loader import load_potential_map
from mcts_core import search
import matplotlib.pyplot as plt
from mcts_helps import MCTSHelps
def main():
    csv_file = "/home/sc-5/Desktop/shao/step4/potential_energy_data.csv"
    potential_map = load_potential_map(csv_file)
    # x_range = (1, 6)
    # y_range = (4, 8)
    start_state = (5.5, 5.5)
    goal_state = (3.8, 5.55)
    best_action = search(100, potential_map, start_state, goal_state)
    print("Best action:", best_action)

if __name__ == "__main__":
    main()
