#!/usr/bin/env python3
# encoding: utf-8
#
#    enable_ssh.py - enables ssh on a raspberry pi image
#    Copyright (C) 2020 Falk Garbsch
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import argparse
import subprocess
import json
import tempfile

from io import BytesIO
from urllib.parse import unquote

def main(args):
    cmd = [ "sfdisk", "-J", args.image ]
    parttable = json.loads(subprocess.check_output(cmd))["partitiontable"]
    assert parttable["unit"] == "sectors"

    partitions = parttable["partitions"]
    print("partitions:")
    for partition in partitions:
        print("    type: 0x%02x  start: %10d  size: %10d" %(int(partition["type"], 16), int(partition["start"]), int(partition["size"])))

    partition = partitions[0]
    assert int(partition["type"], 16) == 0x0c
    start = int(partition["start"])
    index = start * 512

    print("\ntranslate sector %d to byte %d (512 bytes per sector)" % (start, index))

    if args.enable_ssh:
        print("  enable ssh\n")
        cmd = [ "mcopy", "-D", "o", "-i", "%s@@%d" % (args.image, index), "-", "::/ssh" ]
        proc = subprocess.Popen(cmd, stdin = subprocess.PIPE)
        proc.communicate()
        proc.wait()

    if args.add_wifi and len(args.add_wifi):
        buffer = BytesIO()
        buffer.write(b"ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n\n")
        for wifi in args.add_wifi:
            ssid, psk = [unquote(x) for x in wifi.split(":")]
            print("  add wifi ssid=%s, psk=%s" % (ssid, psk))
            buffer.write(("network={\n    ssid=\"%s\"\n    psk=\"%s\"\n    key_mgmt=WPA-PSK\n}\n\n" % (ssid, psk)).encode("utf-8"))
        buffer.seek(0)

        print("  write wifi config\n")
        cmd = [ "mcopy", "-D", "o", "-i", "%s@@%d" % (args.image, index), "-", "::/wpa_supplicant.conf" ]
        proc = subprocess.Popen(cmd, stdin = subprocess.PIPE)
        proc.communicate(buffer.read())
        proc.wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enables SSHD and configure Wifi on an raspbian image file.")
    parser.add_argument("image", type=str, help="The image to be patched.")
    parser.add_argument("--enable-ssh", action="store_true", default=False, help="If enabled, SSH will be enabled on the image.")
    parser.add_argument("--add-wifi", type=str, action="append", help="Adds a wifi configuration to the image. Provide <ssid>:<psk> as urlencoded parameter.")
    main(parser.parse_args())

