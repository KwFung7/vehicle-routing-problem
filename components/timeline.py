#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import config
from components.event import Event


class Timeline:
    event_list = []
    current_time = 0

    def __init__(self, truck_list_inst, warehouse_list_inst, cycle_time):
        self.truck_list_inst = truck_list_inst
        self.truck = truck_list_inst.truck_list[0]
        self.warehouse_list_inst = warehouse_list_inst
        self.path = self.warehouse_list_inst.warehouse_list
        self.cycle_time = cycle_time

    # Add event record to event list
    def record_truck_event(self, timestamp, action, truck_number, point, load_amount):
        event = Event(timestamp, action, truck_number, point, load_amount)
        self.event_list.append(event)
        print('Event - time: {}, action: {}, truck: {}, point: {}, load amount: {}'.format(
            timestamp, action, truck_number, point, load_amount if load_amount <= 0 else '+{}'.format(load_amount)
        ))

    # Calculate arrival time, estimate cycle demand, update truck data and record event
    def handle_arrival_event(self, warehouse, next_warehouse):
        # Update arrival time
        travel_time = float(warehouse.mapping[next_warehouse.warehouse_number])
        self.current_time = self.current_time + travel_time

        # Estimate warehouse demand in whole cycle to determine unload amount
        current_demand = next_warehouse.get_current_demand(self.current_time)
        estimated_cycle_demand = current_demand * self.cycle_time

        # Check all warehouse inventory, any of it below zero will throw error
        self.warehouse_list_inst.update_all_warehouse_inventory(self.current_time)

        # Truck arrival operation
        if next_warehouse.inventory < estimated_cycle_demand:
            # Unload enough amount for each cycle
            required_amount = estimated_cycle_demand - next_warehouse.inventory
            unload_amount = self.truck.unload_product(next_warehouse, required_amount, self.current_time)
        else:
            unload_amount = 0
        self.truck.add_operation_day(travel_time)
        self.truck.increment_arrival_count()
        self.record_truck_event(self.current_time, 'arrival', self.truck.truck_number, next_warehouse.warehouse_number,
                                unload_amount)

    # Only support one truck at this moment
    def start_timeline(self):
        global_config = config.get_global_config()
        standard_unit = int(global_config['STANDARD_UNIT'])
        load_product_time = float(global_config['LOAD_PRODUCT_TIME'])
        simulation_days = int(global_config['SIMULATION_DAYS'])
        self.current_time = 0

        # Repeat the cycle until days 7300
        print('Running vehicle routing simulation...')
        while self.current_time < simulation_days:
            # Start with calculated shortest path
            for index, warehouse in enumerate(self.path):

                # Handling departure event, add load product time before departure
                if self.current_time != 0:
                    self.current_time += load_product_time
                    if warehouse.warehouse_number == 'D1':
                        self.truck.load_product(warehouse)
                self.record_truck_event(self.current_time, 'departure', self.truck.truck_number, warehouse.warehouse_number, 0)

                # Truck should back to depot after finished shortest path or simulation
                if len(self.path) == index + 1 or self.current_time >= simulation_days:
                    next_warehouse = self.path[0]
                else:
                    next_warehouse = self.path[index + 1]

                # Handle all arrival event
                self.handle_arrival_event(warehouse, next_warehouse)

                # Add truck departure record after finished simulation
                if self.current_time >= simulation_days and next_warehouse.warehouse_number == 'D1':
                    self.current_time += load_product_time
                    self.truck.load_product(next_warehouse)
                    self.record_truck_event(self.current_time, 'departure', self.truck.truck_number, next_warehouse.warehouse_number, 0)
                    break

        return self.event_list

    def get_output(self):
        print()

