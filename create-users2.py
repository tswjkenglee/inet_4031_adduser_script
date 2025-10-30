#!/usr/bin/python3

# INET4031
# Author: Tswjkeng Lee
# Date: 10.30.2025
# Create user with a Y/N dry-run prompt

import os   # lets us run system commands
import re   # lets us check if a line starts with '#'
import sys  # lets us read lines from standard input

def main():
    # Ask the user if this is a dry-run (no real changes)
    sys.stdout.write("Run in Dry-run mode? Y/N: ")
    sys.stdout.flush()

    # Read the answer from the keyboard (not from the input file)
    with open("/dev/tty") as tty:
        answer = tty.readline().strip().upper()

    # Dry-run is True if the user types Y
    dry_run = (answer == "Y")

    # Read each line from the input file that we redirect in, like:
    # ./create-users2.py < create-users.input
    for line in sys.stdin:
        # Skip empty lines
        if line.strip() == "":
            if dry_run:
                print(">> SKIP: empty line")
            continue

        # Check if the line starts with '#'
        is_comment = re.match("^#", line)

        # Split the line into parts using ':'
        parts = line.strip().split(':')

        # We expect exactly 5 parts:
        # username : password : last : first : groups
        if is_comment or len(parts) != 5:
            if dry_run:
                if is_comment:
                    print(">> SKIP: commented line -> " + line.strip())
                else:
                    print(">> ERROR: line does not have 5 fields -> " + line.strip())
            # In real run, we stay quiet and just skip
            continue

        # Get each field
        username = parts[0]
        password = parts[1]
        last     = parts[2]
        first    = parts[3]
        groups   = parts[4].split(',')  # example: group01,group02 or "-"

        # Build the GECOS field like: "First Last,,,"
        gecos = first + " " + last + ",,,"

        # 1) Add the user (no password yet)
        print("==> Creating account for " + username + "...")
        cmd_adduser = "/usr/sbin/adduser --disabled-password --gecos '" + gecos + "' " + username
        if dry_run:
            print("[DRY-RUN] Would run: " + cmd_adduser)
        else:
            os.system(cmd_adduser)

        # 2) Set the password (non-interactive)
        print("==> Setting the password for " + username + "...")
        cmd_setpass = "/bin/echo -ne '" + password + "\\n" + password + "' | /usr/bin/sudo /usr/bin/passwd " + username
        if dry_run:
            print("[DRY-RUN] Would run: " + cmd_setpass)
        else:
            os.system(cmd_setpass)

        # 3) Add the user to groups (skip '-' which means no groups)
        for g in groups:
            if g != "-":
                print("==> Assigning " + username + " to the " + g + " group...")
                cmd_group = "/usr/sbin/adduser " + username + " " + g
                if dry_run:
                    print("[DRY-RUN] Would run: " + cmd_group)
                else:
                    os.system(cmd_group)
            else:
                if dry_run:
                    print(">> SKIP: '-' means no group for " + username)

if __name__ == "__main__":
    main()
