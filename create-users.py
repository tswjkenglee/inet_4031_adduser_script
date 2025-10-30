#!/usr/bin/python3

# INET4031
# Tswjkeng Lee
# 10.30.2025
# 10.30.2025

# os is used to run the system commands
import os
# re is used to match text patterns
import re
# sys is used to read the input data from the terminal or a file
import sys

def main():
    for line in sys.stdin:

        #This checks if the line starts with a "#"
	#If "#" is detected, it skips over it.
        match = re.match("^#",line)

	#Splits each line into parts using ":" as a seperator
        fields = line.strip().split(':')

	#Skips the line if it starts with "#" or doesn't have 5 parts
	#Prevents the program from crashing on missing parts or bad/short lines
        if match or len(fields) != 5:
            continue

	#Gets the username and password from the input
	#Geco stores the full name and other user info for /etc/passwd
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

	#Split the last field by commas to get a list of groups
        groups = fields[4].split(',')

	#Shows what user account is being created
        print("==> Creating account for %s..." % (username))

	#Make a system command that adds the user account
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)

	#Commented out for dry-runs to avoid adding real users
	#Uncommented would actually create the account
        #print cmd
        os.system(cmd)

	#Show that the script will se a password for the new user
        print("==> Setting the password for %s..." % (username))

	#Make a system command that sets the user's password
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

	#Commented out for dry-runs to avoid setting a real password
	#Uncommented would actually set the password
        #print cmd
        os.system(cmd)

        for group in groups:
	    # Skip if the group is "-". otherwise add the user to the group
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                #print cmd
                os.system(cmd)


if __name__ == '__main__':
    main()
