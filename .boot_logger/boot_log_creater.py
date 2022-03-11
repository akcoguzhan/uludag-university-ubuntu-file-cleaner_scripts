#!/usr/bin/python3
import os 
import subprocess
from datetime import datetime

def os_commmand_with_return(command, decode="utf-8"):
    cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return cmd.stdout.read().decode(decode)

def main():
    # açılışın tarih ve saat bilgisi
    boot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # açılış yılı
    current_year = os_commmand_with_return('date +%Y').strip()


    # yıllara göre log işlemi yapılması için
    # /Cleaner/boot_logs/2021/boot_logs.txt
    # şeklinde kayıtlar oluşturulur
    # ilgili yıl içersineki tüm kayıtlar aynı belge içerisine kaydedilir
    os.chdir('/Cleaner')

    if not os.path.exists('boot_logs'):
        os.mkdir('boot_logs')

    os.chdir('boot_logs')

    log_by_years = [f.path for f in os.scandir() if f.is_dir()]

    if str('./' + current_year) not in log_by_years:
        os.mkdir(current_year)

    os.chdir(current_year)
        
    
    f = open('boot_logs.txt', 'a')

    # yeni yılın ilk kaydı oluşturulmada önce dosyanın boyutu kontrol edilir
    # eğer dosya yeni oluşturulmuş ise boyutu 0 olacaktır. bu sayede yeni yıl
    # kontrolü yapılmış olur. 
    if os.path.getsize('boot_logs.txt') == 0:
        # önceki yıl kayıtlarının sonuncusunu dosyanın başına ekleriz
        # bu sayede junk_cleaner.py içerisinde değişiklik yapmaya gerek kalmadan
        # script yeni yıla uygun hale getirilmiş olur
        try:
            previous_year_last_boot_log = open('/Cleaner/boot_logs/' + str(int(current_year) - 1) + '/boot_logs.txt')
            previous_year_last_boot_record = str(previous_year_last_boot_log.readlines()[-1]).strip()
            previous_year_last_boot_log.close()
            f.write(previous_year_last_boot_record + '\n')
        except:
            pass


    f.write(boot_time + '\n')
    f.close()

if __name__ == "__main__":
    main()
