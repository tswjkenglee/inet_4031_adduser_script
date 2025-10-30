# INET-4031 Add User Script

## Program Description:
This script helps add users and groups to a Linux system.
Instead of typing manually, this Python script reads from a text file and runs the same commands automatically.

It can:
- Create new user accounts
- Set passwords for each user
- Add users to one or more groups
- Skip users marked with # or with missing data

## How-to-use:

1. Open a terminal on your Linux system.
2. Clone this repository onto your machine:
   - git clone https://github.com/<your-username>/inet_4031_adduser_script.git
3. Move into the folder after cloning:
   - cd inet_4031_adduser_script
4. Prepare a file named create-users.input in the same folder.
5. Each line should follow this format:
   - username:password:last:first:groups
6. Make the script executable:
   - chmod +x create-users2.py

7. Run the program in Dry Run Mode (safe test):
   - ./create-users2.py < create-users.input
7a. Type Y when asked if you want to run a dry run.
    The program will show what it would do, but make no real changes.

8. Run the program for Real Mode (actually adds users):
   - sudo ./create-users2.py < create-users.input
8a. Type N when asked for Dry Run Mode.
   - The script will create users, set passwords, and add groups.

9. Check the results:
  - grep user0 /etc/passwd
  - grep user0 /etc/group

These commands confirm that the users and groups were added.
