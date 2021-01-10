#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
import cmath
import csv
import file_process
import log_noise_filtering
import file_process_mxml

if __name__ == '__main__':
    temp_result = file_process_mxml.file_process()
    # temp_result是字典，其中values是列表，key是字符串

    result = log_noise_filtering.log_noise_filtering(temp_result, -1.46, 0.7)
    with open('Result/CR.csv', mode='w', newline='') as result_file:
        writer = csv.writer(result_file, delimiter=',')
        for key, trace in dict.items(result):
            for event in trace:
                writer.writerow([key, event])
        result_file.close()
