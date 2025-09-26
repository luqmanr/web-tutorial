# steps to setup
1. harus punya akun email
2. enable app password (harus enable 2 factor auth di google account)
3. setelah punya app password, buat `config.py`, yang isinya `EMAIL_PASSWORD='app password dari google'`
4. `EMAIL_ACCOUNT='account@gmail.com'`
5. `IMAP_SERVER='imap.google.com'`
6. coba cek `readmail.py` untuk contoh pemakaian
