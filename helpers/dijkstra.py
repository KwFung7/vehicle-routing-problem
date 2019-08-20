#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
from helpers import helper


def find_path(warehouse_list):
    # 1. All nodes already set with unvisited in warehouse list
    # 2. Depot already set distance as zero
    # 3. Initialize unvisited and visited list
    unvisited_list = warehouse_list
    visited_list = []

    # Repeat until all the node is visited
    while len(unvisited_list) > 0:
        # 4. Select closest warehouse from unvisited list, it will be depot for the first time
        current_node = min(unvisited_list, key=lambda item: item.smallest_distance_to_depot)

        # 5. Stop if current node with smallest distance is infinity
        if current_node.smallest_distance_to_depot == float('inf'):
            break

        # 6. Select all unvisited neighbors and calculate the distance to origin
        # Set distance if it is smaller than node smallest distance
        for node in unvisited_list:
            distance_key = helper.convert_name_to_distance_string(current_node.warehouse_number)
            distance = current_node.smallest_distance_to_depot + float(node.mapping[distance_key])
            if distance < node.smallest_distance_to_depot:
                node.smallest_distance_to_depot = distance

        # 7. Mark current node as visited, remove it from unvisited list
        unvisited_list.remove(current_node)
        visited_list.append(current_node)

    return visited_list
