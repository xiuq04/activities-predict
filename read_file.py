#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def get_events():           # {'id': {'num': '', 'time': '', 'org': [], 'yes': [], 'no': [], 'maybe': []}}
    null = []
    event_files = os.listdir(r"./exp2data/GroupEvent")
    event_records = {}
    for event_filename in event_files:
        name_group = event_filename.split('.')[0]   # get the group name from filename
        event_data = open("./exp2data/GroupEvent/"+event_filename, 'r', encoding='UTF-8')
        i = 0
        group_events = {}   # put all events about one group
        for line in event_data.readlines():
            # delete the '\n' and ' ' at the end of line
            line = line.strip('\n')
            line = line.strip(' ')

            tokens = line.split(' ')
            if i == 0:
                group_event = {}
                id_event = tokens[0]
                group_event['members_num'] = tokens[1]
                group_event['time'] = int(tokens[2])
            elif i == 1:
                group_event['org'] = (tokens if tokens != [''] else [])
            elif i == 2:
                group_event['yes'] = (tokens if tokens != [''] else [])
            elif i == 3:
                group_event['no'] = (tokens if tokens != [''] else [])
            elif i == 4:
                group_event['maybe'] = (tokens if tokens != [''] else [])
                # omit the event with no response
                if len(group_event['yes']) + len(group_event['no']) + len(group_event['maybe']) > 0:
                    group_events[id_event] = group_event
            i = (i + 1) % 5
        event_records[name_group] = group_events
        event_data.close()
    # print(event_records['G0'])
    return event_records


def get_groups():
    groups_data = open("./exp2data/GroupTopic.txt", 'r', encoding='UTF-8')
    i = 0
    groups = {}  # put all events about one group
    for line in groups_data.readlines():
        # delete the '\n' and ' ' at the end of line
        line = line.strip('\n')
        line = line.strip(' ')
        tokens = line.split(' ')
        if i == 0:
            group = {}
            id_group = tokens[0]
            group['org'] = (tokens[1:] if tokens[1:] != ['null'] else [])
        elif i == 1:
            group['topic'] = (tokens if tokens != [''] else [])
            groups[id_group] = group
        i = (i + 1) % 2
    # print(groups)
    groups_data.close()
    return groups


def get_members():
    members_data = open("./exp2data/MemberTopic.txt", 'r', encoding='UTF-8')
    i = 0
    members = {}  # put all events about one group
    for line in members_data.readlines():
        # delete the '\n' and ' ' at the end of line
        line = line.strip('\n')
        line = line.strip(' ')
        tokens = line.split(' ')
        if i == 0:
            member = {}
            id_member = tokens[0]
        elif i == 1:
            for token in tokens:
                if token != '':
                    member[token] = 1
            members[id_member] = member
        i = (i + 1) % 2
    # print(members['M19524'])
    members_data.close()
    members['null'] = {}
    return members


# events = get_events()
# get_groups()
Members = get_members()
