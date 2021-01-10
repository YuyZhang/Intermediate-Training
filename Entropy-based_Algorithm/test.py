#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
import cmath
import csv
import file_process
from Algorithm import direct_filtering
from Algorithm import direct_filtering_with_laplace_smoothing
from Algorithm import indirect_filtering
from Algorithm import indirect_filtering_with_laplace_smoothing

if __name__ == '__main__':
    temp_result = file_process.file_process()
    # temp_result是字典，其中values是列表，key是字符串
    with open('test.csv', mode='w', newline='') as result1_file:
        writer = csv.writer(result1_file, delimiter=',')
        for key, trace in dict.items(temp_result):
            for event in trace:
                writer.writerow([key, event])
        result1_file.close()
    '''
    result1 = direct_filtering.direct_filtering(temp_result)
    target = result1[int((len(result1) + 2) * 0.25)]
    with open('environmental_permit_1.csv', mode='w', newline='') as result1_file:
        writer = csv.writer(result1_file, delimiter=',')
        for key, trace in dict.items(target):
            for event in trace:
                writer.writerow([key, event])
        result1_file.close()

    result2 = direct_filtering_with_laplace_smoothing.direct_filtering_with_laplace_smoothing(temp_result)
    target = result2[int((len(result2) + 2) * 0.25)]
    with open('environmental_permit_2.csv', mode='w', newline='') as result2_file:
        writer = csv.writer(result2_file, delimiter=',')
        for key, trace in dict.items(target):
            for event in trace:
                writer.writerow([key, event])
        result2_file.close()

    result3 = indirect_filtering.indirect_filtering(temp_result)
    target = result3[int((len(result3) + 2) * 0.25)]
    with open('environmental_permit_3.csv', mode='w', newline='') as result3_file:
        writer = csv.writer(result3_file, delimiter=',')
        for key, trace in dict.items(target):
            for event in trace:
                writer.writerow([key, event])
        result3_file.close()

    result4 = indirect_filtering_with_laplace_smoothing.indirect_filtering_with_laplace_smoothing(temp_result)
    target = result4[int((len(result4) + 2) * 0.25)]
    with open('environmental_permit_4.csv', mode='w', newline='') as result4_file:
        writer = csv.writer(result4_file, delimiter=',')
        for key, trace in dict.items(target):
            for event in trace:
                writer.writerow([key, event])
        result4_file.close()
    '''
