#!/usr/bin/env python3

from iss_tracker import sum_squares, find_closest_time_index

data = [{'time': '2024-047T12:00:00.000Z', 'X': {'t': 4}}, {'time': '2024-047T12:04:00.000Z', 'X': {'t':5}}] 

assert find_closest_time_index(data, 'time') == 1

assert sum_squares(data,'X','t') == 41
