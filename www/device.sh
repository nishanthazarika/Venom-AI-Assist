#!/bin/bash

echo "Disconnecting old connections..."
adb disconnect

echo "Setting up connected device..."
adb tcpip 5555

echo "Waiting for device to initialize..."
sleep 3

# Get the IP address of the device dynamically
ip=$(adb shell ip addr show wlan0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)

# Check if IP is empty or not
if [ -z "$ip" ]; then
    echo "Error: Unable to fetch IP address from the device."
    exit 1
fi

echo "Connecting to device with IP $ip..."
adb connect "$ip"

# Restart the ADB server to ensure fresh connection
echo "Restarting the ADB server..."
adb kill-server
adb start-server

# Connect to the device using the IP fetched earlier
echo "Connecting to $ip on port 5555 over Wi-Fi..."
adb connect "$ip:5555"
