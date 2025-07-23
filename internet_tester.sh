#!/bin/bash
echo -e "\e[1;33m🌐 Internet Tester 🌐\e[0m"
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        printf "\e[1;36m [%c] Testing ping...\e[0m" "$spinstr"
        local temp=${spinstr#?}
        spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"
    done
    printf "\e[1;36m [Done] Test completed!     \e[0m\n"
}
echo -e "\e[1;34mStarting ping test...\e[0m"
(ping -c 4 8.8.8.8 > ping_result.txt) & spinner $!
avg_ping=$(grep "rtt min/avg/max" ping_result.txt | awk -F '/' '{print $5}' | awk '{print $1}')
rm ping_result.txt
if [ -n "$avg_ping" ]; then
    echo -e "\e[1;32mPing to 8.8.8.8: $avg_ping ms\e[0m"
else
    echo -e "\e[1;31mError: No internet connection or ping failed!\e[0m"
    exit 1
fi
