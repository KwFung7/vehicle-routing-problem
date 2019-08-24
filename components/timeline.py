#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import config
from tqdm import tqdm
from components.event import Event


class Timeline:
    event_list = []

    def record_truck_event(self, event):
        self.event_list.append(event)

    # Only support one truck at this moment
    def start_timeline(self, truck, path, cycle_time):
        global_config = config.get_global_config()
        load_product_time = float(global_config['LOAD_PRODUCT_TIME'])
        simulation_days = int(global_config['SIMULATION_DAYS'])

        current_time = 0
        p_bar = tqdm(total=simulation_days + 3)

        # Repeat the cycle until days 7300
        while current_time < simulation_days:
            # Start with calculated shortest path
            for index, warehouse in enumerate(path):

                # Handling departure event, add load product time before departure
                if current_time != 0:
                    current_time += load_product_time
                    p_bar.update(load_product_time)
                event = Event(current_time, 'departure', truck.truck_number, warehouse.warehouse_number, 0)
                self.record_truck_event(event)

                # Truck should back to depot after finished shortest path or simulation
                if len(path) == index + 1 or current_time >= simulation_days:
                    next_warehouse = path[0]
                else:
                    next_warehouse = path[index + 1]

                # Calculate arrival time and record event
                travel_time = float(warehouse.mapping[next_warehouse.warehouse_number])
                current_time = current_time + travel_time
                p_bar.update(travel_time)
                event = Event(current_time, 'arrival', truck.truck_number, next_warehouse.warehouse_number, 0)
                self.record_truck_event(event)

                # Add truck departure record after finished simulation
                if current_time >= simulation_days and next_warehouse.warehouse_number == 'D1':
                    current_time += load_product_time
                    p_bar.update(load_product_time)
                    event = Event(current_time, 'departure', truck.truck_number, next_warehouse.warehouse_number, 0)
                    self.record_truck_event(event)
                    break

        return self.event_list

    def get_output(self):
        print()

