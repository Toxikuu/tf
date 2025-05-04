#!/path/to/python
import os
import re
import socket

import psutil


def fix_length(text):
    pattern = re.compile(r"\x1B\[[0-?9;]*[mK]")
    matches = re.findall(pattern, text)

    total_length = 0
    for match in matches:
        total_length += len(match)
    return total_length


def center_align(text, ansi_lengths):
    terminal_width = os.get_terminal_size().columns + ansi_lengths
    return text.center(terminal_width)


# this function is custom to how my system is set up, so you may want to adjust
# the sources directory or the logic
def get_packages():
    patches = []
    tarballs = []

    directory = "/sources"
    for _, _, files in os.walk(directory):
        for file in files:
            if ".patch" in file:
                patches.append(file)
            if ".t" in file and "z" in file: # potentially less robust than tarexts but much simpler
                tarballs.append(file)

    return f"{len(tarballs)} tarballs, {len(patches)} patches"


def get_cpu():
    cpu_freq = f"{float(psutil.cpu_freq()[2] / 1000)} GHz"
    num_cpus = psutil.cpu_count()

    with open("/proc/cpuinfo") as f:
        cpu_info = f.readlines()

    for line in cpu_info:
        if line.startswith("model name"):
            return f"{line.split(":")[1].split("@")[0].strip()}\
 @ {cpu_freq} ({num_cpus})"


def get_mem():
    m = psutil.virtual_memory()

    total = m.total / 1000**3
    used = m.used / 1000**3
    return f"{used:.2f} / {total:.2f} GB"


def get_names():
    # os.getlogin() wasn't working for me :shrug:
    user = os.environ.get('USER')
    hostname = socket.gethostname()
    return f"\x1b[30m{user}\x1b[36m@\x1b[30m{hostname}\x1b[0m"


def get_distro():
    with open("/etc/os-release") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("PRETTY_NAME"):
            return f"{line.split('\"')[1]}"


def get_colors():
    colors = ""
    for i in range(7):
        colors += f"\x1b[3{i};1m * \x1b[0m"
    return colors


def logo():
    c1 = "\x1b[30m"
    c2 = "\x1b[0m"
    c3 = "\x1b[36m"
    return rf"""
        {c2}#####       
       {c2}#######      
       {c2}##{c1}O{c2}#{c1}O{c2}##      
       {c2}#{c3}#####{c2}#      
     {c2}##{c1}##{c3}###{c1}##{c2}##     
    {c2}#{c1}##########{c2}##    
   {c2}#{c1}############{c2}##   
   {c2}#{c1}############{c2}###  
  {c3}##{c2}#{c1}###########{c2}##{c3}#  
{c3}######{c2}#{c1}#######{c2}#{c3}######
{c3}#######{c2}#{c1}#####{c2}#{c3}#######
   {c3}#####{c2}#######{c3}#####{c2}  
"""


def display():
    sysinfo = f"""\
{get_names()}
{get_colors()}
\x1b[30m{get_distro()}\x1b[0m
\x1b[30m{get_cpu()}\x1b[0m
\x1b[30m{get_mem()}\x1b[0m
\x1b[30m{get_packages()}\x1b[0m
"""

    for line in logo().split("\n"):
        ansi_lengths = fix_length(line)
        print(center_align(line, ansi_lengths))

    for line in sysinfo.split("\n"):
        ansi_lengths = fix_length(line)
        print(center_align(line, ansi_lengths))


if __name__ == "__main__":
    display()
    fix_length("\x1b[30m{get_distro()}\x1b[0m")
