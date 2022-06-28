<p align="center">
<img src="https://user-images.githubusercontent.com/48435702/176270041-869570c9-98ae-4c88-964b-f05483794240.png" width="200px" height="200px"/>
<h1 align="center">SUPPORTED BY THE COMPUTER ENGINEERING DEPARTMENT OF BURSA ULUDAĞ UNIVERSITY</h1>
</p>


-------------

**IMPORTANT**: The boot_logger and junk_cleaner folders should be renamed and the directories should be hidden by putting a dot (.) at the beginning of the folder names. The folders were not kept hidden so that the files could be reviewed.

-------------

Requirements:
+ Python
+ Ubuntu 18.04 (Tested)

Preliminary:
-------------
First of all, the /Cleaner directory must be created in the root directory and all files must be moved into this directory. The directory hierarchy should be as follows:
```bash
.
├── .boot_logger
│   └── boot_log_creater.py
├── .junk_cleaner
│   ├── exclude.txt
│   ├── include.txt
│   └── junk_cleaner.py
├── readme.txt
└── services
    ├── boot_logger.sh
    └── junk_cleaner.sh

```
> The **cleaner_boot_logger.service** and **cleaner_junk_cleaner.service** files should be moved to /etc/systemd/system.

Running Scripts as a Service
=============
Scripts must be set as a service in order to perform cleaning operations at the startup of the system. The cleaning process uses the previous boot date and time information and the current boot date and time information each time the computer is turned on. All files that have been modified (newly created files are also created as modified, Linux OS) in this time interval are deleted from the specified directories.

> Scripts with .sh extension are run by services and python scripts are run by them.

Boot Logger (boot_log_creater.py):
-------------
A log generator script has been created to get the correct date and time information of the previous system boot. Information could also be obtained using the system logs from the terminal, but the system logs are reset every month and additionally, if there is a problem with shutdown or restart, they are not properly logged.

Things to do for the log generator script to run as a service:
```
$ sudo chmod 744 /Cleaner/services/boot_logger.sh
$ sudo chmod 664 /etc/systemd/system/cleaner_boot_logger.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable cleaner_boot_logger.service
```
Restart the computer after the processes are complete.
If the processes were completed without any problems, the boot_logs directory should have been created in the /Cleaner directory. In this directory, a folder for the current year will be created and also the boot_logs.txt file will be created in current year folder. Every time the computer is turned on, the current boot date and time is entered at the end of the boot_logs.txt file.

Junk Cleaner (junk_cleaner.py):
-------------
Cleanup operations work for directories written in **include.txt** and **exclude.txt**. Deletion process works for directories written in **include.txt**. The files and folders in **exclude.txt** are not deleted, the directories are skipped. Any directory not included in **include.txt** will not be deleted.

Things to do for the cleaning script to run as a service:
```
$ sudo chmod 744 /Cleaner/services/junk_cleaner.sh
$ sudo chmod 664 /etc/systemd/system/cleaner_junk_cleaner.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable cleaner_junk_cleaner.service
```
Restart the computer after the processes are complete.
If the operations are completed without any problems, a test file can be created in any directory written in **include.text** and the computer can be restarted to check if it has been deleted. A backup system has also been created for deleted files.

Backup Operations:
-------------
Before deleting operations, a backup folder is created by the script in the **/Cleaner/.backups** directory. The maximum number of backups is set as 5. When a new backup is created after the 5th backup is created, the first backup created before is deleted and the backup number is kept as 5.
> Manual entry should not be made to the **last_backup_time.txt** file in **Cleaner/.backups**. The file is created and edited automatically.



Disabling Services
-------------
Things to do to disable services:
```
$ sudo systemctl disable cleaner_junk_cleaner.service
$ sudo systemctl disable cleaner_boot_logger.service
```
> To enable it again, enable keyword must be written instead of disable keyword.

Activating Root Account
------------
A password can be set for sudo operations by activating the root account on the system. In this way, sudo commands can be performed with the sudo password determined differently from the account password, and the authorization level of the student account is not changed. In all processes that require root authority, the password determined as below must be used.

- Ubuntu should boot in recovery mode instead of normal boot.
- https://www.maketecheasier.com/assets/uploads/2019/03/ubuntu-recovery-root.jpg
- Select the root option as above
- With the following code on the command line, the password of the root account is re-set
- **passwd root**
- **new root password is entered twice after entering command**
- Reboot ubuntu.
- Open terminal and run **su** command
- The password determined in the previous step is entered as the password.
- Run **sudo gedit /etc/sudoers**
- The data in the opened file is deleted and the following texts are added instead


```
#
# This file MUST be edited with the 'visudo' command as root.
#
# Please consider adding local content in /etc/sudoers.d/ instead of
# directly modifying this file.
#
# See the man page for details on how to write a sudoers file.
#
Defaults env_reset
Defaults mail_badpass
Defaults secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
Defaults rootpw
ogrenci ALL=(ALL) ALL
%sudousers ALL=(ALL) ALL
Defaults:%sudousers !rootpw
# Host alias specification

# User alias specification

# Cmnd alias specification

# User privilege specification
root ALL=(ALL:ALL) ALL

# Members of the admin group may gain root privileges
%admin ALL=(ALL) ALL

# Allow members of group sudo to execute any command
%sudo ALL=(ALL:ALL) ALL

# See sudoers(5) for more information on "#include" directives:

#includedir /etc/sudoers.d
```

- ***The text above has been prepared for computers in the computer lab of Uludag University Computer Engineering***


Setting a directory that cannot be changed (delete, create etc.) by students in any way.
-------------
```
sudo chattr +i /home/ogrenci/Şablonlar
```
> Directory access can be opened by typing -i instead of +i.

Debug Operations For Visual Studio Code
-------------
While working on the script, if the directory where the scripts are located is the root directory or a directory that requires root permission, debugging can be done by adding the following information into a launch.json file (created using the Visual Studio Code editor).
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Sudo Debug",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "sudo": true
        }
    ]
}
```
> **"sudo": true** provides root permission. For the debug process to start, the sudo password must be entered from the terminal screen in Visual Studio Code.

Jupyter-Notebook Operations:
-------------
- In addition to opening the application in the home directory with the **jupyter-notebook** command on the terminal, the jupyter-notebook application can also be opened in the desired directory by entering the directory parameter such as **jupyter-notebook */home/ogrenci/Desktop***.
- Even if any directory parameter is entered by the students, it is always ensured that the application works in the specified directory. This directory is designated as **/home/ogrenci/JupyterNotebook**.

> In addition, the jupyer-notebook command deletes all files in the specified **/home/ogrenci/JupyterNotebook** directory every time the application is opened. In this way, a student who opens the application later will not be able to access the previous files.

Two different arrangements must be made in order for these processes to take place.

1. Open the **jupyter-notebook** file located in the **/home/ogrenci/anaconda3/bin** directory with any text editor.
2. The contents of the file are updated as follows.
```
#!/home/ogrenci/anaconda3/bin/python

# -*- coding: utf-8 -*-
import re
import sys
import os

from notebook.notebookapp import main

if __name__ == '__main__':
    if not os.path.exists("/home/ogrenci/JupyterNotebook"):
        os.mkdir("/home/ogrenci/JupyterNotebook")
    if os.path.exists("/home/ogrenci/JupyterNotebook"):
        os.chdir("/home/ogrenci/JupyterNotebook")
        all_files = os.listdir()
        for f in all_files:
          os.system("rm -r " + str(f))

    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```
> With this change, every time the application is opened, the **/home/ogrenci/JupyterNotebook** directory is created if it does not exist, and all files in it are deleted.
3. Open the **Filemanager.py** file located in the **/anaconda3/lib/python3.7/site-packages/notebook/services/contents/** directory with any text editor.
> If the **python3.7** folder is not in the **lib** directory, the desired directory must be navigated from the folder with a different python version name.
4. The content of the ***def info_string(self):*** function, located approximately on line 581 of the file, is updated as follows
```
def info_string(self):
  if os.path.exists("/home/ogrenci/JupyterNotebook"):
    self.root_dir = "/home/ogrenci/JupyterNotebook"
    
  return _("Serving notebooks from local directory: %s") % self.root_dir
```
> With this change, the application is guaranteed to open in the **/home/ogrenci/Jupyter Notebook** directory.
> Even if the directory is specified as **jupyter-notebook /home/ogrenci/Desktop** when opening the application, the application will open in the **JupyerNotebook** directory.


Opening Terminal in Desktop Directory Instead of Home Directory
-------------
- When the terminal application is opened using a shortcut or by clicking on the application's icon, it operates in the ***/home/ogrenci*** directory.
- Students usually create their files after opening the terminal, without specifying a directory, as **touch <filename>** in the directory where the terminal was opened.
- Since the script that performs the cleaning process does not work for the ***/home/ogrenci*** directory, the files created here remain undeleted.
- To avoid this problem to some extent, the default boot directory of the terminal has been replaced with ***/home/ogrenci/*** -> ***/home/ogrenci/Desktop***.
> Since each new file created with terminal commands (such as touch etc.) will be found in the Desktop directory, it will be detected and deleted by the script that performs the cleaning process.
  
In order for this to happen, the secret file **.bashrc** in the ***/home/ogrenci/*** directory is opened with a text editor.
Go to the last line of the file and add the following commands
```
if [ "$(pwd)" == "/home/ogrenci" ]; then
cd /home/ogrenci/Masaüstü
fi
```
> This process does not change the directory of terminals opened with **Open terminal here** from the right-click menu in any directory. It is only valid for terminals opened in the home directory.
  
