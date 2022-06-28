#!/usr/bin/python3
import os
import subprocess
from datetime import datetime


def os_commmand_with_return(command, decode="utf-8"):
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return cmd.stdout.read().decode(decode)


def main():
    # the date and time information of startup
    boot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # startup year
    current_year = os_commmand_with_return("date +%Y").strip()

    # for logging by years
    # /Cleaner/boot_logs/2021/boot_logs.txt
    # records are created as above
    # all records in the related year are recorded in the same document.
    os.chdir("/Cleaner")

    if not os.path.exists("boot_logs"):
        os.mkdir("boot_logs")

    os.chdir("boot_logs")

    log_by_years = [f.path for f in os.scandir() if f.is_dir()]

    if str("./" + current_year) not in log_by_years:
        os.mkdir(current_year)

    os.chdir(current_year)

    f = open("boot_logs.txt", "a")

    # file size is checked before the first record of the new year is created
    # if the file is newly created, its size will be 0 byte. In this way, the new year control is made.
    if os.path.getsize("boot_logs.txt") == 0:
        # we add the last of the previous year records to the beginning of the file
        # In this way, the script is adapted to the new year
        # without the need to make changes in junk_cleaner.py.
        try:
            previous_year_last_boot_log = open(
                "/Cleaner/boot_logs/" + str(int(current_year) - 1) + "/boot_logs.txt"
            )
            previous_year_last_boot_record = str(
                previous_year_last_boot_log.readlines()[-1]
            ).strip()
            previous_year_last_boot_log.close()
            f.write(previous_year_last_boot_record + "\n")
        except:
            pass

    f.write(boot_time + "\n")
    f.close()


if __name__ == "__main__":
    main()
