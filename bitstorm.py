#!/usr/bin/env python

from sys import argv, exit, stdout
from copy import copy

def usage():
    print("[-] %s {input_file} {extension} {start} {end} ({output_dir} {update_interva})", argv[0])


print("BitStorm 1.0 Starting...\n")

try:
    input_file = argv[1]
    extension = argv[2]
except:
    usage()
    exit(1)


try:
    start_at = int(argv[3])
    end_at = int(argv[4])
except:
    usage()
    print("[-] Start and End should be ints")
    exit(1)

try:
    output_dir = argv[5]
except:
    output_dir = "output"

try:
    update_interval = int(argv[6])
except:
    update_interval = 100

print("[+] Input File: %s" % input_file)
print("[+] File Extension: %s" % extension)
print("[+] Doing Byte Range %d~%d" % (start_at, end_at))
print("[+] Output Directory: %s" % output_dir)
print("[+] Update interval: %d" % update_interval)

seed_file = open(input_file, 'r')
seed = seed_file.read()
seed_file.close()

print("[+] Length: %2d." % len(seed))
if end_at > len(seed):
    print("[-] Can't end at %d, ending at %d")
    end_at = len(seed)

for i in range(start_at, end_at):
    if (i % update_interval) == 0:
        stdout.write("\n[+] Generating Mutants %d-%d" % (i, i+update_interval))
    else:
        stdout.write(".")
    stdout.flush()
    mutant = list(copy(seed))
    mutated_file = None
    try:
        mutated_file = open("%s/mutation_%d.%s" % (output_dir, i, extension), 'w')
    except IOError:
        print("[-] Can't write to %s/mutation_%d.%s" % (output_dir, 1, extension))
        exit(1)
    byte = ~ord(mutant[i])

    deadlock_detect = 0
    while byte < 0 or byte > 0xff:
        if byte < 0:
            byte = 0xff + byte
        elif byte > 0xff:
            byte = 0xff - byte
        deadlock_detect = deadlock_detect + 1
        if deadlock_detect > 5:
            print("[!] Deadlock, exiting.")
            print("    Byte: %x" % byte)
            print("    Offset: %d" % i)
            exit(1)
    mutant[i] = chr(byte)
    mutated_file.write(''.join(mutant))
    mutated_file.close()

print("\n[+] Done, happy fuzzing!")
