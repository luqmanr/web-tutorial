import readdatabase

email_content = """
    REKNO: 123456
    NAMA LENGKAP: Luqman R
"""
rekno = email_content.split("REKNO:")[-1].split("\n")[0]
nama_lengkap = email_content.split("NAMA LENGKAP:")[-1].split("\n")[0]
print(rekno)
print(nama_lengkap)

email, jumlah = readdatabase.get_rekno_jumlah(rekno, nama_lengkap)
