#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import config
import csv
from components.truck import Truck
from components.truck_list import TruckList
from components.warehouse import Warehouse
from components.warehouse_list import WarehouseList
from helpers import helper
from helpers.reinforcement import Reinforcement


def initialize_trucks():
    global_config = config.get_global_config()
    standard_unit = int(global_config['STANDARD_UNIT'])
    truck_list = TruckList()

    # Using only one truck at this moment
    truck = Truck(1, standard_unit, 0, standard_unit)
    truck_list.purchase_new_truck(truck)
    return truck_list


def initialize_warehouses():
    global_config = config.get_global_config()
    standard_unit = int(global_config['STANDARD_UNIT'])
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
                standard_unit,
                0,
                standard_unit,
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

    reinforcement = Reinforcement(warehouse_list_inst.warehouse_list)
    shortest_path = reinforcement.get_shortest_path()

    truck_list_inst.get_total_truck_purchase_cost()
    truck_list_inst.get_total_truck_operating_cost()
    warehouse_list_inst.get_total_warehouse_purchase_cost()


if __name__ == '__main__':
    main()
