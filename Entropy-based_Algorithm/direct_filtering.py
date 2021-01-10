#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
import cmath


# l是dict{}
def activities(log):
    result = []
    for trace in dict.values(log):
        for event in trace:
            if event not in result:
                result.append(event)
    return result


# x是list[]
def h1(x):
    result = 0
    for i in range(len(x)):
        if x[i] != 0:
            result = result - x[i] * math.log2(x[i])
    return result


# a在l中出现次数，l是list[]
def occurrences_time(a, log):
    result = 0
    for k in range(len(log)):
        for i in range(len(log[k]) - len(a) + 1):
            j = 0
            while j < len(a):
                if log[k][i + j] == a[j]:
                    j = j + 1
                else:
                    break
            if j >= len(a):
                result = result + 1
    return result


# l是dict{}，a是event
def dfr(a, log):
    result = []
    l_temp = []
    acts = []
    for trace in dict.values(log):
        trace_temp = []
        for i in range(len(trace)):
            trace_temp.append(trace[i])
            if trace[i] not in acts:
                acts.append(trace[i])
        trace_temp.append(']')
        l_temp.append(trace_temp)
    acts.append(']')

    for event in acts:
        trace1 = [a, event]
        trace2 = [a]
        result.append(occurrences_time(trace1, l_temp) / occurrences_time(trace2, l_temp))

    return result


# l是dict{}，a是event
def dpr(a, log):
    result = []
    l_temp = []
    acts = ['[']
    for trace in dict.values(log):
        trace_temp = ['[']
        for i in range(len(trace)):
            trace_temp.append(trace[i])
            if trace[i] not in acts:
                acts.append(trace[i])
        l_temp.append(trace_temp)

    for event in acts:
        trace1 = [event, a]
        trace2 = [a]
        result.append(occurrences_time(trace1, l_temp) / occurrences_time(trace2, l_temp))

    return result


# l是dict{}
def h2(a, log):
    return h1(dfr(a, log)) + h1(dpr(a, log))


# l是dict{}
def arg_max(acts, log):
    max_h = 0
    result = ''
    for a in acts:
        if h2(a, log) > max_h:
            result = a
    return result


def l_temp_update(acts, a, l_temp):
    acts_temp = []
    for event in acts:
        if event != a:
            acts_temp.append(event)

    result = {}
    for key, values in dict.items(l_temp):
        trace = []
        for i in range(len(values)):
            if values[i] in acts_temp:
                trace.append(values[i])
        result[key] = trace

    return result


def direct_filtering(log):
    l_temp = {}
    for key, values in dict.items(log):
        l_temp[key] = values
    # l是字典{}，其中values是列表[]，key是字符串
    q = [l_temp]

    acts = activities(l_temp)
    while len(acts) > 2:
        a = arg_max(acts, l_temp)
        l_temp = l_temp_update(acts, a, l_temp)
        q.append(l_temp)
        acts = activities(l_temp)

    return q
