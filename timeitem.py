#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import read_file as f
import math as m


def get_member_events(events):
    member_events = {}
    for group_events in events.values():
        for event_id, group_event in group_events.items():
            time = group_event['time']
            members = group_event['yes']
            # print(time)
            for member in members:
                member_event = {}
                if member in member_events:
                    member_event = member_events[member]
                member_event[event_id] = time
                member_events[member] = member_event
    return member_events


def get_events_item(events, members, groups):
    events_item = {}
    for group_id, group in groups.items():
        group_item = group['topic'] 
        group_events = events[group_id]
        for event_id, event in group_events.items():
            event_item = {}
            for item in group_item:
                event_item[item] = 1
            event_org = event['org']
            for org_id in event_org:
                if org_id in members:
                    org = members[org_id]
                    for item in group_item:
                        if item in org:  
                            event_item[item] += 1

            events_item[event_id] = event_item
    return events_item       


def get_item_time(members, member_events, events_item, member_id, now_time):
    member = {}
    # member_event = {}
    if member_id in members:
        member = members[member_id]
    if member_id not in member_events:
        return member
    member_event = member_events[member_id]
    for event_id, time in member_event.items():
        if time < now_time:
            # print(time)
            event_item = events_item[event_id]
            # print(event_item)
            for item in event_item:
                # print(1/m.exp(m.log(1+(now_time-time) * 1e-9)))
                if item in member:
                    member[item] += 1/m.exp(m.log(1+(now_time-time) * 1e-9))
                else:
                    member[item] = 1/m.exp(m.log(1+(now_time-time) * 1e-9))               
    return member


def members_update(members, member_events, events_item, member_lists, time):

    for id_member in member_lists:
        members[id_member] = get_item_time(members, member_events, events_item, id_member,
                                           int(time))
    return members


def get_member_habits1(events):
    member_habits = {}
    for group_id, group_events in events.items():
        for event_id, group_event in group_events.items():
            members_yes = group_event['yes']
            members_maybe = group_event['maybe']
            members_no = group_event['no']
            # print(time)
            for member in members_yes:
                member_habit = {}
                if member in member_habits:
                    member_habit = member_habits[member]
                if group_id in member_habit:
                    member_habit[group_id][0] += 1
                else:
                    member_habit[group_id] = [1, 0, 0]
                member_habits[member] = member_habit

            for member in members_maybe:
                member_habit = {}
                if member in member_habits:
                    member_habit = member_habits[member]
                if group_id in member_habit:
                    member_habit[group_id][1] += 1
                else:
                    member_habit[group_id] = [0, 1, 0]
                member_habits[member] = member_habit

            for member in members_no:
                member_habit = {}
                if member in member_habits:
                    member_habit = member_habits[member]
                if group_id in member_habit:
                    member_habit[group_id][2] += 1
                else:
                    member_habit[group_id] = [0, 0, 1]
                member_habits[member] = member_habit               
           
    return member_habits


def get_member_habits2(events):
    member_habits = {}
    for group_id, group_events in events.items():
        for event_id, group_event in group_events.items():
            members_yes = group_event['yes']
            members_maybe = group_event['maybe']
            members_no = group_event['no']
            orgs = group_event['org']
            if orgs == ['null']:
                continue
            # print(time)
            for member in members_yes:
                member_habit = {}
                if member in member_habits:
                    member_habit = member_habits[member]
                for org in orgs:
                    if org in member_habit:                
                        member_habit[org][0] += 1
                    else:
                        member_habit[org] = [1, 0, 0]
                member_habits[member] = member_habit

            for member in members_maybe:
                member_habit = {}
                if member in member_habits:
                    member_habit = member_habits[member]
                for org in orgs:
                    if org in member_habit:                
                        member_habit[org][1] += 1
                    else:
                        member_habit[org] = [0, 1, 0]
                member_habits[member] = member_habit

            for member in members_no:
                member_habit = {}
                if member in member_habits:
                    member_habit = member_habits[member]
                for org in orgs:
                    if org in member_habit:                
                        member_habit[org][2] += 1
                    else:
                        member_habit[org] = [0, 0, 1]
                member_habits[member] = member_habit              
           
    return member_habits


def get_member_habits(key, events):
    if key == 1:
        return get_member_habits1(events)
    elif key == 2:
        return get_member_habits2(events)


def get_member_all_events(events):
    member_all_events = {}
    for group_id, group_events in events.items():
        for event_id, group_event in group_events.items():
            time = group_event['time']
            members_yes = group_event['yes']
            members_maybe = group_event['maybe']
            members_no = group_event['no']
            orgs = group_event['org']
            for member in members_yes:
                event = {}
                event['time'] = time
                event['group_id'] = group_id
                event['org'] = orgs
                event['act'] = 0
                member_all_event = {}
                if member in member_all_events:
                    member_all_event = member_all_events[member]
                member_all_event[event_id] = event
                member_all_events[member] = member_all_event

            for member in members_maybe:
                event = {}
                event['time'] = time
                event['group_id'] = group_id
                event['org'] = orgs
                event['act'] = 1
                member_all_event = {}
                if member in member_all_events:
                    member_all_event = member_all_events[member]
                member_all_event[event_id] = event
                member_all_events[member] = member_all_event

            for member in members_no:
                event = {}
                event['time'] = time
                event['group_id'] = group_id
                event['org'] = orgs
                event['act'] = 2
                member_all_event = {}
                if member in member_all_events:
                    member_all_event = member_all_events[member]
                member_all_event[event_id] = event
                member_all_events[member] = member_all_event

    return member_all_events


def get_member_time_habits(model, member_all_events, member_id, now_time):
    member_time_habits = {}
    member_all_event = {}
    if member_id not in member_all_events:
        return member_time_habits
    member_all_event = member_all_events[member_id]
    for event in member_all_event.values():
        if event['time'] < now_time:
            if model == 1:  # group
                member_time_habit = [0, 0, 0]
                group_id = event['group_id']
                if group_id in member_time_habits:
                    member_time_habit = member_time_habits[group_id]
                # member_time_habit[event['act']] += 1/m.exp(m.log(1+(now_time-event['time']) * 1e-9))
                member_time_habit[event['act']] += 1
                member_time_habits[group_id] = member_time_habit

            if model == 2:  # org
                for org in event['org']:
                    member_time_habit = [0, 0, 0]
                    if org in member_time_habits:
                        member_time_habit = member_time_habits[org]
                    # member_time_habit[event['act']] += 1/m.exp(m.log(1+(now_time-event['time']) * 1e-9))
                    member_time_habit[event['act']] += 1
                    member_time_habits[org] = member_time_habit

    return member_time_habits


'''
Events = f.get_events()
Members = f.get_members()
Groups = f.get_groups()
Member_Events = get_member_events(Events)
print(Member_Events)
Events_Item = get_events_item(Events, Members, Groups)
print(Events_Item)
member = get_item_time(Members, Member_Events, Events_Item, 'M60359', 1304095600000)
member_habits = get_member_habits(2, Events)
print(member_habits['M60359'])
'''

    

