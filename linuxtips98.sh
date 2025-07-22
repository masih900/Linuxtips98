#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import shutil
from datetime import datetime

# رنگ‌ها برای خروجی جذاب‌تر
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def print_banner():
    print(f"{GREEN}=====================================")
    print("      LinuxTips98 - Utility Script    ")
    print(f"      For Termux & Linux - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"====================================={RESET}")

def check_platform():
    """نمایش اطلاعات سیستم"""
    print(f"{YELLOW}[+] System Info:{RESET}")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"User: {os.getlogin()}")
    print(f"Current Directory: {os.getcwd()}")

def list_files():
    """لیست کردن فایل‌ها و دایرکتوری‌ها"""
    print(f"{YELLOW}[+] Listing files in current directory:{RESET}")
    for item in os.listdir():
        item_path = os.path.join(os.getcwd(), item)
        if os.path.isdir(item_path):
            print(f"{GREEN}[DIR] {item}{RESET}")
        else:
            print(f"[FILE] {item}")

def check_disk_usage():
    """چک کردن فضای دیسک"""
    print(f"{YELLOW}[+] Disk Usage:{RESET}")
    total, used, free = shutil.disk_usage("/").total, shutil.disk_usage("/").used, shutil.disk_usage("/").free
    print(f"Total: {total // (2**30)} GB")
    print(f"Used: {used // (2**30)} GB")
    print(f"Free: {free // (2**30)} GB")

def run_command(cmd):
    """اجرای دستورات شل"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"{YELLOW}[+] Command Output:{RESET}")
        print(result.stdout or result.stderr)
    except Exception as e:
        print(f"{RED}[-] Error running command: {e}{RESET}")

def main_menu():
    while True:
        print(f"\n{YELLOW}=== LinuxTips98 Menu ==={RESET}")
        print("1. Show System Info")
        print("2. List Files in Current Directory")
        print("3. Check Disk Usage")
        print("4. Run Custom Shell Command")
        print("5. Exit")
        
        choice = input(f"{GREEN}Enter your choice (1-5): {RESET}")
        
        if choice == "1":
            check_platform()
        elif choice == "2":
            list_files()
        elif choice == "3":
            check_disk_usage()
        elif choice == "4":
            cmd = input(f"{GREEN}Enter shell command to run: {RESET}")
            run_command(cmd)
        elif choice == "5":
            print(f"{RED}Exiting LinuxTips98. Bye!{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}Invalid choice! Try again.{RESET}")

if __name__ == "__main__":
    # چک کردن دسترسی اجرایی در ترموکس/لینوکس
    if not os.access(sys.argv[0], os.X_OK):
        print(f"{RED}[-] Warning: Script is not executable. Run 'chmod +x linuxtips98.sh' to fix.{RESET}")
    
    print_banner()
    main_menu()
