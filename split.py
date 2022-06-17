#!/usr/bin/env python
# -*- coding: utf-8 -*-
import read_file


def topic_inc(member, group, num):
    for topic in group['topic']:
        if topic in member:
            member[topic] += num
        else:
            member[topic] = num


def get_folds(id_val, members, event_records, groups):
    folds_num = 5
    events_val = {}
    events_train = {}
    for id_group in event_records:
        i = 0
        events_val[id_group] = {}
        events_train[id_group] = {}
        for id_event in event_records[id_group]:
            if i == id_val:
                i = (i + 1) % folds_num
                events_val[id_group][id_event] = event_records[id_group][id_event]
                continue
            events_train[id_group][id_event] = event_records[id_group][id_event]
            i = (i + 1) % folds_num
    return events_val, events_train


def members_update_by_train(members, groups, events_train):
    for id_group in events_train:
        for id_event in events_train[id_group]:
            for id_member in events_train[id_group][id_event]['yes']:
                if id_member not in members:
                    members[id_member] = {}
                    # members[member]['topic'] = []
                topic_inc(members[id_member], groups[id_group], 1)
            for id_member in events_train[id_group][id_event]['no']:
                if id_member not in members:
                    members[id_member] = {}
                topic_inc(members[id_member], groups[id_group], -1)
    return members


'''
Event_records = read_file.get_events()
Val_id = 0
Members = read_file.get_members()
Groups = read_file.get_groups()
# Members,  = get_folds(Val_id, Members, Event_records, Groups)
# print(splits)
'''