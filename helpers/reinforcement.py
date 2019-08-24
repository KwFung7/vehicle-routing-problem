#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import random
import config
import time
from tqdm import tqdm
from colorama import Fore


class Reinforcement:
    # 1. All nodes already set with 0 path score for reinforcement learning
    # 2. Initialize unvisited, visited list and shortest path
    unvisited_list = []
    visited_list = []
    shortest_path = []
    shortest_cycle_time = float('inf')

    def __init__(self, warehouse_list):
        self.warehouse_list = warehouse_list

    # Run simulation to update shortest cycle time and shortest path
    def run_simulation(self):
        global_config = config.get_global_config()
        reinforcement_config = config.get_reinforcement_config()

        current_node = self.unvisited_list[0]
        self.unvisited_list.remove(current_node)
        self.visited_list.append(current_node)
        total_cycle_time = 0

        # 4. Repeat until all the node is visited
        while len(self.unvisited_list) > 0:
            # 5. Randomly select next node when random value is larger than threshold,
            # this step increase the randomization in our reinforcement
            if random.random() > float(reinforcement_config['RANDOM_THRESHOLD']):
                selected_node = random.choice(self.unvisited_list)

                # Get node travel time from selected node to current node
                node_travel_time = float(selected_node.mapping[current_node.warehouse_number])
                total_cycle_time = total_cycle_time + node_travel_time + float(global_config['LOAD_PRODUCT_TIME'])
            else:
                # 6. When random value is smaller than threshold,
                # select the next node based on path score and node travel time
                selected_node = max(self.unvisited_list,
                                    key=lambda node: node.path_score[current_node.warehouse_number] / float(
                                        node.mapping[current_node.warehouse_number]))

                # Get node travel time from selected node to current node
                node_travel_time = float(selected_node.mapping[current_node.warehouse_number])
                total_cycle_time = total_cycle_time + node_travel_time + float(global_config['LOAD_PRODUCT_TIME'])

            # 7. Update the list and current node
            self.unvisited_list.remove(selected_node)
            self.visited_list.append(selected_node)
            current_node = selected_node

        # 8. Add travel time for returning to depot
        total_cycle_time += float(self.visited_list[-1].mapping['D1']) + float(global_config['LOAD_PRODUCT_TIME'])

        # 9. Record the shortest cycle time in each repeat cycle
        if total_cycle_time < self.shortest_cycle_time:

            # 10. Reward the preferred path with higher path score
            for index, visited_node in enumerate(self.visited_list):
                if index == 0:
                    visited_node.path_score[visited_node.warehouse_number] += 1
                visited_node.path_score[self.visited_list[index - 1].warehouse_number] += 1

            self.shortest_cycle_time = total_cycle_time
            self.shortest_path = self.visited_list.copy()

        # 11. Reset the list for next round
        self.unvisited_list = self.warehouse_list.copy()
        self.visited_list.clear()

    # Get shortest path with provided warehouse distance
    def get_shortest_path(self):
        reinforcement_config = config.get_reinforcement_config()
        self.unvisited_list = self.warehouse_list.copy()

        # 3. Repeat simulation to investigate shortest path
        print('Running shortest path simulation...')
        for i in tqdm(range(int(reinforcement_config['REPEAT_TIME'])), Fore.BLUE):
            self.run_simulation()

        time.sleep(1)
        print('\nShortest path travel time: {0:.2f} days'.format(self.shortest_cycle_time))
        print('Shortest path: ', end="")
        for node in self.shortest_path:
            print(' 🡲 {}'.format(node.warehouse_number), end="")
        print(' 🡲 D1 \n')
        time.sleep(1)
        return self.shortest_path

    # Must run this function after get_shortest_path to return cycle time
    def get_shortest_cycle_time(self):
        return self.shortest_cycle_time


