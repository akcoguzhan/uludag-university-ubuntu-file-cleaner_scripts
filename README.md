<p align="center">
<img src="https://user-images.githubusercontent.com/48435702/176270041-869570c9-98ae-4c88-964b-f05483794240.png" width="200px" height="200px"/>
<h1 align="center">ULUDAĞ ÜNİVERSİTESİ BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ TARAFINDAN DESTEKLENMİŞ BİR ÇALIŞMADIR</h1>
</p>


-------------

**ÖNEMLİ**: boot_logger ve junk_cleaner klasörlerinin yeniden isimlendirilip klasör başlarına . işareti konularak dizinlerin gizlenmesi gerekmektedir.
dosyaların incelenebilmesi için klasörler gizli tutulmadı.

-------------

Gereksinimler:
+ Python
+ Ubuntu 18.04 (Üst sürümlerde kararsızlık olabilir, 18.04 test edildi)

Ön Hazırlık
-------------
Öncelikle root dizini içerisinde Cleaner dizini oluşturulmalı ve tüm dosyalar bu dizin içerisine atılmalıdır. Dizin hiyerarşisi aşağıdaki gibi olmalıdır:
```bash
.
├── .boot_logger
│   └── boot_log_creater.py
├── .junk_cleaner
│   ├── exclude.txt
│   ├── include.txt
│   └── junk_cleaner.py
├── readme.txt
└── services
    ├── boot_logger.sh
    └── junk_cleaner.sh

```
> **cleaner_boot_logger.service** ve **cleaner_junk_cleaner.service** dosyaları /etc/systemd/system dizini içerisine taşınmalıdır.

> .boot_logger ve .junk_cleaner dizinlerinin başında **'.' (nokta)** bulunmaktadır. Dizinler gizli dizinlerdir. Eğer **'.'** kaldırılacak ise scriptler içerisinden de değiştirilmelidir. 

Scriptleri Servis Olarak Çalıştırma
=============
Bilgisayarın her açılışında temizleme işlemlerinin yapılabilmesi için hazırlanmış olarak scriptlerin servis olarak ayarlanması gerekmektedir. Temizleme işlemi bilgisayar her açıldığında bir önceki açılış tarih ve saat bilgisi ile geçerli olan açılışın tarih ve saat bilgisini kullanarak bu zaman aralığında modifikasyona uğramış (yeni oluşturulan dosyalar da modifiye edilmiş olarak oluşuturulur) tüm dosyalar belirlenen dizinler içerisinden silinir.
> Servisler tarafından .sh uzantılı scriptler çalıştırılır ve .sh uzantılı scriptler tarafından da python scriptleri çalıştırılır

Boot Logger (boot_log_creater.py):
-------------
Bir önceki açılışın tarih ve saat bilgisini sağlıklı bir şekilde alabilmek için bir log oluşturucu script oluşturulmuştur. Terminal üzerinden sistem logları kullanılarak da bilgi elde edilebilirdi ancak sistem logları her ay sıfırlanmakta ve ek olarak kapanmada veya yeniden başlatmada bir problem olduğunda düzgün bir şekilde loglanmamaktadır.

Log oluşturucu scriptin bir servis olarak bilgisayarın her açılışında çalışması için yapılması gerekenler:
```
$ sudo chmod 744 /Cleaner/services/boot_logger.sh
$ sudo chmod 664 /etc/systemd/system/cleaner_boot_logger.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable cleaner_boot_logger.service
```
İşlemler tamamlandıktan sonra bilgisayar yeniden başlatılır.
Eğer işlemler sorunsuz bir şekilde tamamlandıysa /Cleaner dizini içerisinde boot_logs dizini oluşmuş olmalı. İçerisinde geçerli yıla ait bir klasör ve onun da içinde boot_logs.txt dosyası olmalıdır. Bilgisayar her açıldığında boot_logs.txt dosyasının sonuna o an ki açılış tarih ve saat bilgisi girilir.

Junk Cleaner (junk_cleaner.py):
-------------
Temizleme işlemleri .junk_cleaner dizini içerisindeki **include.txt** ve **exclude.txt** girilen dizinler için çalışır. **include.txt** içerisindeki dizinlerde silme işlemi gerçekleştirilir. **exclude.txt** içerisindeki dizinlerde ise silme işlemi özellikle yapılmaz. **exlude.txt** içerisine **include.txt** içerisinde bulunan bir dizin içerisindeki başka bir dizinin silinmesi istenmiyor ise ekleme yapılmalıdır. **include.txt** içerisinde bulunmayan herhangi bir dizinde silme işlemi gerçekleşmez. 

Temizleme işlemi yapan scriptin bir servis olarak bilgisayarın her açılışında çalışması için yapılması gerekenler:
```
$ sudo chmod 744 /Cleaner/services/junk_cleaner.sh
$ sudo chmod 664 /etc/systemd/system/cleaner_junk_cleaner.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable cleaner_junk_cleaner.service
```
İşlemler tamamlandıktan sonra bilgisayar yeniden başlatılır.
Eğer işlemler sorunsuz bir şekilde tamamlandıysa **include.txt** içerisinde bulunan herhangi bir dizinde bir dosya oluşturulup bilgisayar yeniden başlatılarak silinip silinmediği kontrol edilebilir. Silinen dosyalar için bir yedek sistemi de oluşturulmuştur.

Yedek İşlemleri:
-------------
Silme işleminden önce script tarafından **/Cleaner/.backups** dizini içerisinde yedek oluştururulur. Maksimumum yedek sayısı 5 olarak belirlenmiştir. 5. yedek de oluştuktan sonra yeni bir yedek oluşturulacağı zaman daha önceden oluşturulmuş olan ilk yedek silinir ve yedek sayısı 5 olarak korunur
> **Cleaner/.backups** içerisinde bulunan **last_backup_time.txt** dosyasına manuel giriş yapılmamalıdır. Dosya otomatik olarak oluşup düzenlenmektedir.




Servisleri Devre Dışı Bırakmak
-------------
Servisleri durdurmak için yapılması gerekenler:
```
$ sudo systemctl disable cleaner_junk_cleaner.service
$ sudo systemctl disable cleaner_boot_logger.service
```
> Tekrar aktif edebilmek için disable yerine enable yazılmalıdır

Root Hesabını Aktif Etme
------------
Sistem üzerinde root hesabını aktif ederek sudo işlemleri için şifre belirlenebilir. Bu sayede hesap şifresinden farklı olarak belirlenen sudo şifresi ile sudo komutları gerçekleştirilebilir. Ve yine bu sayede öğrenci hesaplarının yetkisi değiştirilmemiş olur. Root yetkisi gereken tüm işlemlerde artık aşağıdaki şekilde belirlenen şifre kullanılmak zorunluluğu oluşur. 

- Ubuntu normal boot yerine recovery modda açılır
- https://www.maketecheasier.com/assets/uploads/2019/03/ubuntu-recovery-root.jpg
- Yukarıda olduğu gibi root seçeneği seçilir
- Komut satırında aşağıdaki kod ile birlikte root hesabının şifresi yeniden belirlenmiş olur
- **passwd root**
- **komut girildikten sonra yeni root şifresi iki kez girilir**
- Ubuntu normal şekilde yeniden açılır
- Terminal açılarak **su** komutu çalıştırılır
- Şifre olarak belirlenen şifre girilir
- **sudo gedit /etc/sudoers** komutu çalıştırılır
- Açılan dosya içindeki veriler silinip yerine aşağıdaki yazılar eklenir


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

- ***Yukarıdaki metin bilgisayar laboratuvarındaki bilgisayarlar için hazırlanmıştır***


Öğrenci Tarafından Silinemeyen ve İçerisinde Bir Dosya Oluşturulamayan Dizin Ayarlama:
-------------
home dizini içerisinde bulunan Şablonlar klasörü içerisinde oluşturulan herhangi bir dosya sayesinde herhangi bir dizinde mouse sağ tıkı ile açılan Yeni Doküman (new document) kısa yoldan bir dosya oluşturulabilmektedir. Ancak oluşturulan bu dosya Şablonlar içerisinde bulunan dosyasının bir kopyası olduğundan dosyanın modifikasyon tarihi orijinal dosya ile aynı kalmaktadır (herhangi bir değişiklik yapılmaz ise). Temizleyici tarafındna bu dosyalar belirlenen zaman aralığı dışında kalabileceğinden Şablonlar dizininde dosya oluşturma yetkisi öğrencilerden alınmıştır. 
```
sudo chattr +i /home/ogrenci/Şablonlar
```
komutu ile işlem gerçekleştirilmiştir.
> +i yerine -i yazılarak dizin tekrardan erişime açılabilir.

Debug İşlemleri
-------------
Script üzerinde çalışırken eğer scriptlerin bulunduğu dizin root dizini veya root izni gerektiren bir dizin ise Visual Studio Code editörü kullanılarak oluşturulan bir launch.json dosyası içerisine alttaki bilgiler eklenerek debug yapılabilir.

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
> Root izni ile debug yapmayı **"sudo": true** bilgisi sağlar. Debug işleminin başlayabilmesi için Visual Studio Code içerisinde bulunan terminal ekranından sudo şifresi girilmelidir. 

Jupyter-Notebook İşlemleri
-------------
- Terminal üzerinden **jupyter-notebook** ile uygulamanın home dizininde açılmasının yanı sıra **jupyter-notebook */home/ogrenci/Masaüstü*** gibi dizin parametresi girilerek de jupyter-notebook uygulaması istenilen dizinde de açılabilmektedir. 
- Dosya temizleme işlemlerini yerine getiren script yalnızca daha öncesinde tanımlanan dizinlerde çalıştığı için, herhangi bir öğrencinin jupyter-notebook uygulamasını istediği dizinde açabilmesinin önüne geçilmiştir.
- Öğrenci dizin parametresi girmiş dahi olsa her zaman uygulamanın belirlenen dizinde çalışması sağlanmıştır. Bu dizin **/home/ogrenci/JupyterNotebook** olarak belirlenmiştir.

> Bunun yanı sıra jupyer-notebook uygulaması her açılışında belirlenen **/home/ogrenci/JupyterNotebook** dizini içerisindeki tüm dosyaları silmektedir. Bu sayede uygulamayı sonradan açan bir öğrenci önceki dosyalara erişim sağlayamayacaktır. 

Bu işlemlerin gerçekleşmesi için iki farklı düzenleme yapılması gerekmektedir. 

1. **/home/ogrenci/anaconda3/bin** dizini içerisinde bulunan **jupyter-notebook** dosyası herhangi bir metin düzenleyici ile açılır.
2. Dosyanın içeriği aşağıdaki gibi güncellenir.
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
> Bu değişiklik ile birlikte uygulama her açıldığında **/home/ogrenci/JupyterNotebook** dizininin yoksa oluşturulması ve içerisindeki tüm dosyaların silinmesi sağlanır.
3. **/anaconda3/lib/python3.7/site-packages/notebook/services/contents/** dizini içerisinde bulunan **Filemanager.py** dosyasının herhangi bir metin düzenleyici ile açılır.
> **python3.7** klasörü eğer **lib** dizini içerisinde yoksa farklı bir python sürümü ismine sahip olan klasör içerisinden istenilen dizine gidilmelidir.
4. Dosyanın takriben 581. satırında bulunan ***def info_string(self):*** fonksiyonun içeriği aşağıdaki gibi güncellenir
```
def info_string(self):
  if os.path.exists("/home/ogrenci/JupyterNotebook"):
    self.root_dir = "/home/ogrenci/JupyterNotebook"
    
  return _("Serving notebooks from local directory: %s") % self.root_dir
```
> Bu değişiklik ile birlikte uygulamanın yalnızca **/home/ogrenci/JupyterNotebook** dizininde açılması sağlanmış olur.
> **jupyter-notebook /home/ogrenci/Masaüstü** şeklinde uygulama açılırken dizin belirtilmiş olsa dahi uygulama **JupyerNotebook** dizininde açılacaktır.  


Terminalin Home Dizini Yerine Masaüstü Dizininde Açılması
-------------
- Terminal uygulaması kısayol kullanılarak veya uygulamanın simgesine tıklayarak açıldığında ***/home/ogrenci*** dizininde işlem yapmaktadır.
- Öğrenciler genellikle dosyalarını terminali açtıktan sonra dizin belirtmeden **touch <dosyaadı>** şeklinde terminal hangi dizinde açıldı ise orda oluşturmaktadır.
- Temizleme işlemini yapan script ***/home/ogrenci*** dizini için çalışmadığından dolayı burada oluşturulan dosyalar silinmeden kalmaktadır.
- Bu problemin bir nebze de olsa önüne geçmek için terminalin varsayılan açılış dizini olan ***/home/ogrenci/*** -> ***/home/ogrenci/Masaüstü*** ile değiştirilmiştir.
> Bu sayede touch vb. komutlar ile oluşturulan her yeni dosya Masaüstü dizini içerisinde bulunacağından temizleme işlemini gerçekleştiren script tarafından algılanıp silinecektir.
  
Bu işlemin gerçekleşmesi için ***/home/ogrenci/*** dizini içerisinde bulunan **.bashrc** gizli dosyası metin düzenleyici ile açılır
Dosyanın son satırına gidilerek aşağıdaki komutlar eklenir
```
if [ "$(pwd)" == "/home/ogrenci" ]; then
cd /home/ogrenci/Masaüstü
fi
```
> Bu işlem herhangi bir dizinde sağ tık menüsünden **Terminali burada aç** ile açılan terminallerin dizinini değiştirmemektedir. Yalnızca home dizinde açılan terminaller için geçerli bir işlemdir.
  


