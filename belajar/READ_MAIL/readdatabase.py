# given sebuah email address, return rekno & jumlah dari database.csv
def get_rekno_jumlah(email):
    f = open("database.csv", "r").read()
    f = f.split("\n")
    for rows in f:
        cols = rows.split(",")
        dbemail = cols[0]
        if dbemail == email:
            rekno = cols[2]
            jumlah = cols[3]
            return rekno, jumlah
        else:
            rekno = 0
            jumlah = 0
    return rekno, jumlah

if __name__ == '__main__':
    foundrek, foundjum = get_rekno_jumlah('luqman.rahardjo@gmail.com')
    print("found:", foundrek, foundjum)