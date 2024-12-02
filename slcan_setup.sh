#!/bin/bash
env=${1:-test}

if [ $env == "test" ]; then
    # set virtual for testing
    sudo modprobe vcan
    sudo ip link add dev vcan0 type vcan
    sudo ip link set up vcan0
    
elif [ $env == "prod" ]; then
    # set virtual for real
    sudo modprobe slcan
    tty_name=$(dmesg | grep -Po "ttyACM\d"|tail -n1)
    sudo slcand -o -c -f -S 115200 -s6 "/dev/${tty_name}"
    sudo ip link set up can0
fi
