#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import config
import csv
import time
from components.truck import Truck
from components.truck_list import TruckList
from components.warehouse import Warehouse
from components.warehouse_list import WarehouseList
from components.timeline import Timeline
from helpers import helper
from helpers.reinforcement import Reinforcement


def initialize_trucks():
    global_config = config.get_global_config()
    standard_unit = int(global_config['STANDARD_UNIT'])
    truck_list = TruckList()

    # Using only one truck at this moment
    truck = Truck(1, standard_unit*16, 0, standard_unit*16)
    truck_list.purchase_new_truck(truck)
    return truck_list


def initialize_warehouses():
    global_config = config.get_global_config()
    initial_warehouse_size = int(global_config['INITIAL_WAREHOUSE_SIZE'])
    warehouse_list = WarehouseList()

    with open(global_config['DATASET_PATH'], newline='') as dataset:
        # Return csv dataset
        print('Using {}...'.format(global_config['DATASET_PATH']))
        datadict = csv.DictReader(dataset)

        # Retrieve warehouse data in dataset and append it to warehouse list
        for row in datadict:
            maximum_warehouse_size = int(row['maximum_warehouse_size'])\
                if len(row['maximum_warehouse_size']) != 0 else float('inf')

            # Create distance mapping
            mapping = helper.create_distance_mapping(row)

            warehouse = Warehouse(
                row['depot_warehouse_name'],
                float('inf') if row['depot_warehouse_name'] == 'D1' else initial_warehouse_size,
                0,
                0 if row['depot_warehouse_name'] == 'D1' else initial_warehouse_size,
                float(row['demand']),
                float(row['demand_growth_rate']),
                maximum_warehouse_size,
                int(row['possible_truck_size']),
                mapping
            )
            warehouse_list.append_warehouse_record(warehouse)
    return warehouse_list


def main():
    # Initialize warehouses and trucks
    truck_list_inst = initialize_trucks()
    warehouse_list_inst = initialize_warehouses()

    # Get shortest path and cycle time with reinforcement learning
    reinforcement = Reinforcement(warehouse_list_inst.warehouse_list)
    shortest_path = reinforcement.get_shortest_path()
    shortest_cycle_time = reinforcement.get_shortest_cycle_time()
    warehouse_list_inst.set_warehouse_list(shortest_path)

    # Start timeline and record event
    timeline = Timeline(truck_list_inst, warehouse_list_inst, shortest_cycle_time)
    timeline.start_timeline()
    time.sleep(1)

    # TODO: Calculate cost
    # truck_list_inst.get_total_truck_purchase_cost()
    # truck_list_inst.get_total_truck_operating_cost()
    # warehouse_list_inst.get_total_warehouse_purchase_cost()

    timeline.get_solution_output()
    timeline.get_equipment_output()


if __name__ == '__main__':
    main()
