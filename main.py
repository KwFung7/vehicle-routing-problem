#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import config
import csv
import sys
from components.Truck import Truck
from components.TruckList import TruckList
from components.Warehouse import Warehouse
from components.WarehouseList import WarehouseList


def initializeTrucks():
    global_config = config.get_global_config()
    standard_unit = int(global_config['STANDARD_UNIT'])
    truck_list = TruckList()

    # Using only one truck at this moment
    truck = Truck(1, standard_unit, 0, standard_unit)
    truck_list.purchase_new_truck(truck)
    return truck_list


def initializeWarehouses():
    global_config = config.get_global_config()
    standard_unit = int(global_config['STANDARD_UNIT'])
    warehouse_list = WarehouseList()

    with open(global_config['DATASET_PATH'], newline='') as dataset:
        # Return csv dataset
        datadict = csv.DictReader(dataset)

        # Retrieve warehouse data in dataset and append it to warehouse list
        for row in datadict:
            maximum_warehouse_size = int(row['maximum_warehouse_size'])\
                if len(row['maximum_warehouse_size']) != 0 else sys.maxsize
            warehouse = Warehouse(
                row['depot_warehouse_name'],
                standard_unit,
                0,
                standard_unit,
                float(row['demand']),
                float(row['demand_growth_rate']),
                maximum_warehouse_size,
                int(row['possible_truck_size'])
            )
            warehouse_list.append_warehouse_record(warehouse)
    return warehouse_list


def main():
    # Initialize warehouses and trucks
    truck_list = initializeTrucks()
    warehouse_list = initializeWarehouses()

    truck_list.get_total_truck_purchase_cost()
    truck_list.get_total_truck_operating_cost()

    warehouse_list.get_total_warehouse_purchase_cost()


if __name__ == '__main__':
    main()
