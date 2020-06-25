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

The script just takes the image file as a parameter. Just call

```
python3 enable_ssh.py 2020-05-27-raspios-buster-lite-armhf.img
```

if 2020-05-27-raspios-buster-lite-armhf.img is your desired image file. It
will automatically add a file named `ssh` to the root of the boot partition.
You don't need root to perform this operation, as the image is not mounted
but the fat-filesystem is modified instead.

