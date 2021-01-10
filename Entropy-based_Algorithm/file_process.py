#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
import cmath

file = open("data/test.xes", "r", encoding='UTF-8')


def find_name(line):
    index = line.find("value=")
    name = ""
    for i in range(index + 7, len(line)):
        if line[i] == "\"":
            break
        name += line[i]
    return name


def find_next_event():
    global file
    while 1:
        line = file.readline()
        line = line[:-1]
        if line == "\t</trace>":
            break
        elif line == "\t\t<event>":
            while 1:
                line1 = file.readline()
                line1 = line1[:-1]
                if "key=\"concept:name\"" in line1:
                    event_name = find_name(line1)
                    return event_name
    return -1


def file_process():
    global file
    log = {}
    line = file.readline()
    line = line[:-1]
    while line:
        if line == "\t<trace>":
            while 1:
                line1 = file.readline()
                line1 = line1[:-1]
                if "key=\"concept:name\"" in line1:
                    trace_name = find_name(line1)
                    break
            log[trace_name] = []
            while 1:
                event_name = find_next_event()
                if event_name == -1:
                    break
                else:
                    log[trace_name].append(event_name)
        line = file.readline()
        line = line[:-1]
    file.close()
    return log
