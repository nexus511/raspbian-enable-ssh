# enable_ssh.py

Simple helper script to add the ssh file to the vfat partition on a raspbian
image. This will enable sshd during boot and allow you to access the
raspberry pi without having to use a monitor and keyboard on the device.

I rarely use the raspberry pi on any kind of display but I really often
forget to enable sshd before I boot the device for the first time. By just
enabling it on the image I have downloaded, this is not automagically
enabled on all of my devices and I just have to connect to the device and
pick a secure password.

## Requirements

The script requires a few packages being installed:

- mtools
- util-linux
- dosfstools
- python3

To make sure those tools are installed, you can use the following command on
ubuntu/debian:

```
sudo apt install util-linux mtools dosfstools python3
```

## Usage

To just enable ssh, use the --enable-ssh parameter. Just call

```
python3 enable_ssh.py --enable-ssh 2020-05-27-raspios-buster-lite-armhf.img
```

if 2020-05-27-raspios-buster-lite-armhf.img is your desired image file. It
will automatically add a file named `ssh` to the root of the boot partition.
You don't need root to perform this operation, as the image is not mounted
but the fat-filesystem is modified instead.

You can also use the script to write a wpa_supplicant.conf file to the
partitions to make sure that the device also connects to a network
automatically, if you don't like to use ethernet or are using a pi zero or a
pi A+.

You can add one or multiple wifis using the --add-wifi parameter:

```
python3 enable_ssh.py --add-wifi MySsid:MyPsk 2020-05-27-raspios-buster-lite-armhf.img
```

MySsid is the SSID and MyPsk the PSK of the connection. If you want to use
special characters, you can URL-encode the SSID and PSK. This can be done
using urllib. You can use this command line:

```
python3 -c 'from urllib.parse import quote; print(quote("This:Password!"));'
```
