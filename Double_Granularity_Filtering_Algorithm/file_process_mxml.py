#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
import cmath

file = open("Data/CR.mxml", "r")


def find_trace_name(line):
    index = line.find("id=")
    name = ""
    for i in range(index + 4, len(line)):
        if line[i] == "\"":
            break
        name += line[i]
    return name


def find_event_name(line):
    index = line.find("<WorkflowModelElement>")
    name = ""
    for i in range(index + 22, len(line)):
        if line[i] == "<":
            break
        name += line[i]
    return name


def find_next_event():
    global file
    while 1:
        line = file.readline()
        line = line[:-1]
        if line == "\t\t</ProcessInstance>":
            break
        elif line == "\t\t\t<AuditTrailEntry>":
            while 1:
                line1 = file.readline()
                line1 = line1[:-1]
                if "<WorkflowModelElement>" in line1 and "</WorkflowModelElement>" in line1:
                    event_name = find_event_name(line1)
                    return event_name
    return -1


def file_process():
    global file
    log = {}
    line = file.readline()
    line = line[:-1]
    while line:
        if "\t\t<ProcessInstance id=" in line:
            trace_name = find_trace_name(line)
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
