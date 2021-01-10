#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import math
import cmath


# 获取日志中所有事件，输入log为字典{}，输出result为列表[]
def activities(log):
    result = []
    for trace in dict.values(log):
        for event in trace:
            if event not in result:
                result.append(event)
    return result


# 获取日志中(e1,e2)的出现次数
def dfd(e1, e2, log):
    result = 0
    for trace in dict.values(log):
        for i in range(len(trace) - 1):
            if trace[i] == e1 and trace[i + 1] == e2:
                result = result + 1
    return result


# 获取dfd矩阵以及所有dfd的和
def get_dfd(acts, log):
    dfds = {}
    sums = 0
    for e1 in acts:
        temp = {}
        for e2 in acts:
            temp[e2] = dfd(e1, e2, log)
            sums = sums + temp[e2]
        dfds[e1] = temp
    return dfds, sums


# 获取ek前面的事件的集合，输出为列表[]
def u_pre(ek, acts, dfds):
    result = []
    for et in acts:
        if dfds[et][ek] > 0 and et not in result:
            result.append(et)
    return result


# 获取ek后面的事件的集合，输出为列表[]
def u_suc(ek, acts, dfds):
    result = []
    for et in acts:
        if dfds[ek][et] > 0 and et not in result:
            result.append(et)
    return result


# 计算ek前面的事件出现次数
def n_pre(ek, dfds, u_pre_set):
    result = 0
    for et in u_pre_set:
        result = result + dfds[et][ek]
    return result


# 计算ek后面的事件出现次数
def n_suc(ek, dfds, u_suc_set):
    result = 0
    for et in u_suc_set:
        result = result + dfds[ek][et]
    return result


# 计算ek前面的事件的密度
def d_pre(ek, acts, dfds):
    u_pre_set = u_pre(ek, acts, dfds)
    if len(u_pre_set) != 0:
        return n_pre(ek, dfds, u_pre_set) / len(u_pre_set)
    else:
        return 0


# 计算ek后面的事件的密度
def d_suc(ek, acts, dfds):
    u_suc_set = u_suc(ek, acts, dfds)
    if len(u_suc_set) != 0:
        return n_suc(ek, dfds, u_suc_set) / len(u_suc_set)
    else:
        return 0


# 计算局部依赖
def dep_local(e1, e2, acts, dfds):
    temp1 = d_suc(e1, acts, dfds)
    temp2 = d_pre(e2, acts, dfds)
    if temp1 != 0 and temp2 != 0:
        return 1 - 1 / ((1 + math.exp((dfds[e1][e2] - temp1) * (4 / temp1))) * 2) - 1 / ((1 + math.exp((dfds[e1][e2] - temp2) * (4 / temp2))) * 2)
    elif temp1 == 0 and temp2 != 0:
        return 1 - 1 / ((1 + math.exp((dfds[e1][e2] - temp2) * (4 / temp2))) * 2)
    elif temp1 != 0 and temp2 != 0:
        return 1 - 1 / ((1 + math.exp((dfds[e1][e2] - temp1) * (4 / temp1))) * 2)
    else:
        return 1


# 计算全局依赖
def dep_global(e1, e2, acts, dfds, sums):
    theta = 0
    for ex in acts:
        for ey in acts:
            if ey != ex:
                if dfds[ex][ey] / sums < 0.02:
                    theta = max(theta, dfds[ex][ey])
    if theta != 0:
        return 1 / (1 + math.exp(1 - dfds[e1][e2] / theta))
    else:
        return 1


# 计算混合依赖
def dep_mixed(e1, e2, acts, dfds, sums):
    return 0.5 * dep_local(e1, e2, acts, dfds) + 0.5 * dep_global(e1, e2, acts, dfds, sums)


# 计算混合依赖矩阵
# 输入：log为日志，acts为日志中所有事件
# 输出：matrix是字典{}，其value是字典{}。对于事件(a,b)，其混合依赖值为matrix[a][b]
def a_mdm(log, acts, dfds, sums):
    matrix = {}
    for e1 in acts:
        temp = {}
        for e2 in acts:
            mixed = dep_mixed(e1, e2, acts, dfds, sums)
            temp[e2] = mixed
        matrix[e1] = temp
    return matrix


def log_noise_filtering(log, punish_para, abandon_threshold):
    log_filter = {}
    acts = activities(log)
    dfds, sums = get_dfd(acts, log)
    matrix = a_mdm(log, acts, dfds, sums)
    '''
    for key, trace in dict.items(log):
        e_start = trace[0]
        e_end = trace[len(trace) - 1]
        trace_filter = [e_start]
        abandon_para = 1
        for i in range(len(trace) - 1):
            j = i + 1
            ei = trace[i]
            ej = trace[j]
            while matrix[ei][ej] < 0.5:
                j = j + 1
                ej = trace[j]
                abandon_para = abandon_para * punish_para * (1 + 2 * (1 / punish_para - 1) * dep_mixed(ei, ej, log, acts))
                if abandon_para < abandon_threshold:
                    continue
            trace_filter.append(ej)
            i = j
        log_filter[key] = trace_filter
    '''
    for key, trace in dict.items(log):
        e_start = trace[0]
        trace_filter = [e_start]
        abandon_para = 1
        i = 0
        while i < len(trace) - 1:
            j = i + 1
            ei = trace[i]
            ej = trace[j]
            while matrix[ei][ej] < 0.5 and j < len(trace) - 1:
                abandon_para = abandon_para * punish_para * (
                            1 + 2 * (1 / punish_para - 1) * matrix[ei][ej])
                if abandon_para < abandon_threshold:
                    break
                j = j + 1
                ej = trace[j]
            if matrix[ei][ej] < 0.5 and j == len(trace) - 1:
                abandon_para = abandon_para * punish_para * (
                        1 + 2 * (1 / punish_para - 1) * matrix[ei][ej])
            if abandon_para < abandon_threshold:
                break
            if matrix[ei][ej] >= 0.5:
                trace_filter.append(ej)
            i = j
        if abandon_para >= abandon_threshold:
            log_filter[key] = trace_filter
    return log_filter

