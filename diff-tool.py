#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import copy


class DiffTool:
    def __init__(self):
        self.pattern = re.compile("^[a-zA-Z0-9_]*:[a-zA-Z0-9_]*=")

    def match(self, line):
        return self.pattern.search(line)

    def collect(self, file):
        s = set()
        while True:
            line_raw = file.readline()
            if not line_raw:
                break
            line = line_raw.rstrip()
            if d.match(line):
                s.add(line)
        return s


class MakeDict:
    """
    NAME
    gui value
    ter value
    """
    def __init__(self):
        pattern = re.compile(":")
        self.split = pattern.split
        self.d = dict()

    def add_vars(self, myset, tag):
        for line in myset:
            key_value = self.split(line)
            if len(key_value) > 2:
                raise NotImplementedError
            key = key_value[0]
            if self.d.get(key):
                self.d[key][tag] = key_value[1]
            else:
                temp = {"gui": " < empty >", "ter": " < empty >"} 
                temp[tag] = key_value[1]
                self.d[key] = temp


if __name__ == "__main__":
    gui = open("CMakeCache_gui.txt", "r")
    ter = open("CMakeCache_terminal.txt", "r")
    # gui = open("a.txt", "r")
    # ter = open("b.txt", "r")

    d = DiffTool()
    gui_vars = d.collect(gui)
    ter_vars = d.collect(ter)
    
    # remove dup
    for v in copy.copy(ter_vars):
        if v in gui_vars:
            gui_vars.remove(v)
            ter_vars.remove(v)
    
    # make dict
    s = MakeDict()
    s.add_vars(gui_vars, "gui")
    s.add_vars(ter_vars, "ter")
    
    # wirte file
    res = open("result.txt", "w")
    for k, v in s.d.items():
        res.write("(ter) {}:{}\n".format(k, v["ter"]))
        res.write("(gui) {}:{}\n\n".format(k, v["gui"]))
    res.close()
