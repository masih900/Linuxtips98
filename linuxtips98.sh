#!/bin/bash

# File: monitor_resources.sh
# Purpose: Monitor CPU, memory, and disk usage

echo "System Resource Monitor"

# Check if running on Termux or Linux
if [ -d "/data/data/com.termux" ]; then
    # Termux environment
    echo "Detected Termux."
    # CPU usage (using top)
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
    # Memory usage
    MEM_TOTAL=$(free -m | awk '/Mem:/ {print $2}')
    MEM_USED=$(free -m | awk '/Mem:/ {print $3}')
    MEM_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))
    # Disk usage
    DISK_USAGE=$(df -h /data | awk 'NR==2 {print $5}' | tr -d '%')
else
    # Linux environment
    echo "Detected Linux."
    # CPU usage
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
    # Memory usage
    MEM_TOTAL=$(free -m | awk '/Mem:/ {print $2}')
    MEM_USED=$(free -m | awk '/Mem:/ {print $3}')
    MEM_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))
    # Disk usage
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
fi

# Display results
echo "CPU Usage: $CPU_USAGE%"
echo "Memory Usage: $MEM_USED/$MEM_TOTAL MB ($MEM_PERCENT%)"
echo "Disk Usage: $DISK_USAGE%"

# Alerts for high usage
if [ "$CPU_USAGE" -gt 80 ]; then
    echo "WARNING: High CPU usage detected!"
fi
if [ "$MEM_PERCENT" -gt 80 ]; then
    echo "WARNING: High memory usage detected!"
fi
if [ "$DISK_USAGE" -gt 80 ]; then
    echo "WARNING: High disk usage detected!"
fi
