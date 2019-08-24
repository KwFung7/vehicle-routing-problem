#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import config
import math
import csv
import time
import os
from tqdm import tqdm
from components.event import Event
from components.truck import Truck


class Timeline:
    event_list = []
    current_time = 0

    def __init__(self, truck_list_inst, warehouse_list_inst, cycle_time):
        self.truck_list_inst = truck_list_inst
        self.truck_list = self.truck_list_inst.truck_list
        self.warehouse_list_inst = warehouse_list_inst
        self.path = self.warehouse_list_inst.warehouse_list
        self.cycle_time = cycle_time

    # Add event record to event list
    def record_truck_event(self, timestamp, action, truck_number, point, load_amount):
        event = Event(timestamp, action, truck_number, point, load_amount)
        self.event_list.append(event)
        print('Event - time: {}, action: {}, truck: {}, point: {}, load amount: {}'.format(
            timestamp, action, truck_number, point, load_amount
        ))

    # Estimate warehouse demand in whole cycle to determine unload amount
    def get_estimated_cycle_demand(self, next_warehouse):
        current_demand = next_warehouse.get_current_demand(self.current_time)
        estimated_cycle_demand = current_demand * (1 + next_warehouse.demand_growth) * self.cycle_time
        return estimated_cycle_demand

    # Calculate arrival time, estimate cycle demand, update truck data and record event
    def handle_arrival_event(self, warehouse, next_warehouse, p_bar):
        global_config = config.get_global_config()
        simulation_days = int(global_config['SIMULATION_DAYS'])

        # Update arrival time
        travel_time = float(warehouse.mapping[next_warehouse.warehouse_number])
        self.current_time = self.current_time + travel_time
        p_bar.update(travel_time)
        estimated_cycle_demand = self.get_estimated_cycle_demand(next_warehouse)

        # Check all warehouse inventory, any of it below zero will throw error
        if self.current_time < simulation_days:
            self.warehouse_list_inst.update_all_warehouse_inventory(self.current_time)

        # Truck arrival operation
        for truck in self.truck_list:

            if next_warehouse.warehouse_number == 'D1':
                load_amount = truck.load_product(next_warehouse, 0)

            elif next_warehouse.inventory > estimated_cycle_demand and truck.products_inventory == 0:
                # Logic for relay warehouse
                required_amount = next_warehouse.inventory - estimated_cycle_demand
                load_amount = truck.load_product(next_warehouse, required_amount)
            elif next_warehouse.inventory < estimated_cycle_demand and truck.truck_size == next_warehouse.truck_size_limit:
                # Unload enough amount for each cycle
                required_amount = estimated_cycle_demand - next_warehouse.inventory
                load_amount = truck.unload_product(next_warehouse, required_amount, self.current_time)
            else:
                load_amount = 0

            truck.add_operation_day(travel_time)
            truck.increment_arrival_count()
            self.record_truck_event(self.current_time, 'arrival', truck.truck_number, next_warehouse.warehouse_number, load_amount)

    # Check next warehouse size limit for truck,
    # add new truck if all existing trucks are not compatible
    def check_next_warehouse_size_limit(self, warehouse, next_warehouse):
        min_truck = self.truck_list_inst.get_min_truck()
        estimated_cycle_demand = self.get_estimated_cycle_demand(next_warehouse)
        compatible_truck_list = [truck for truck in self.truck_list if truck.truck_size == next_warehouse.truck_size_limit]
        compatible_truck_total_inventory = sum(truck.products_inventory for truck in compatible_truck_list)

        if compatible_truck_total_inventory <= estimated_cycle_demand:
            for i in range(math.ceil(estimated_cycle_demand / next_warehouse.truck_size_limit)):
                new_truck = Truck(
                    len(self.truck_list) + 1,
                    next_warehouse.truck_size_limit,
                    self.current_time,
                    next_warehouse.truck_size_limit
                )
                self.truck_list_inst.purchase_new_truck(new_truck)
                self.truck_list = self.truck_list_inst.truck_list
                self.record_truck_event(self.current_time, 'departure', new_truck.truck_number, warehouse.warehouse_number, 0)

    # Simulate vehicle routing timeline
    def start_timeline(self):
        global_config = config.get_global_config()
        load_product_time = float(global_config['LOAD_PRODUCT_TIME'])
        simulation_days = int(global_config['SIMULATION_DAYS'])
        self.current_time = 0

        # Repeat the cycle until days 7300
        print('Running vehicle routing simulation...')
        time.sleep(1)
        p_bar = tqdm(total=simulation_days + 3)
        while self.current_time < simulation_days:
            # Start with calculated shortest path
            for index, warehouse in enumerate(self.path):

                # Handling departure event, add load product time before departure
                if self.current_time != 0:
                    self.current_time += load_product_time
                    p_bar.update(load_product_time)
                for truck in self.truck_list:
                    self.record_truck_event(self.current_time, 'departure', truck.truck_number, warehouse.warehouse_number, 0)

                # Truck should back to depot after finished shortest path or simulation
                if len(self.path) == index + 1 or self.current_time >= simulation_days:
                    next_warehouse = self.path[0]
                else:
                    next_warehouse = self.path[index + 1]

                # Check next warehouse size limit for truck
                self.check_next_warehouse_size_limit(warehouse, next_warehouse)

                # Handle all arrival event
                self.handle_arrival_event(warehouse, next_warehouse, p_bar)

                # Add truck departure record after finished simulation
                if self.current_time >= simulation_days and next_warehouse.warehouse_number == 'D1':
                    self.current_time += load_product_time
                    p_bar.update(load_product_time)
                    for truck in self.truck_list:
                        self.record_truck_event(self.current_time, 'departure', truck.truck_number, next_warehouse.warehouse_number, 0)
                    break

        return self.event_list

    # Get solution csv output
    def get_solution_output(self):
        global_config = config.get_global_config()
        solution_output = global_config['SOLUTION_OUTPUT']
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, '../../solution/' + solution_output)
        print('\nGenerating solution csv output...')
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for event in self.event_list:
                writer.writerow([
                    event.timestamp,
                    event.action,
                    event.truck_number,
                    event.point, event.load_amount
                ])
        print('Finish {} output generation at {}'.format(solution_output, path))

    # Get equipment csv output
    def get_equipment_output(self):
        global_config = config.get_global_config()
        equipment_output = global_config['EQUIPMENT_OUTPUT']
        initial_warehouse_size = global_config['INITIAL_WAREHOUSE_SIZE']
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, '../../solution/' + equipment_output)
        print('\nGenerating equipment csv output...')
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write final truck list
            for truck in self.truck_list:
                writer.writerow([
                    truck.truck_number,
                    truck.truck_size,
                    truck.purchase_date,
                    truck.truck_size
                ])

            # Write final warehouse list, sort the list with name first
            self.path.sort(key=lambda item: int(item.warehouse_number[1:]))
            for warehouse in self.path:
                if warehouse.warehouse_number == 'D1':
                    continue
                writer.writerow([
                    warehouse.warehouse_number,
                    min(initial_warehouse_size, warehouse.size_limit),
                    warehouse.purchase_date,
                    min(initial_warehouse_size, warehouse.size_limit)
                ])
                for i, record in enumerate(warehouse.added_warehouse_size):
                    writer.writerow([
                        warehouse.warehouse_number,
                        record,
                        warehouse.additional_purchase_date[i],
                        0
                    ])
        print('Finish {} output generation at {}'.format(equipment_output, path))

