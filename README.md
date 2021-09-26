## Features

- Refresh jumlah followers yang ditampilkan di terminal (Default 1 detik)
- Membuat Bar Chart berisi pergerakan follower setiap waktu yang ditentukan (Default 1 minute)
- Simpan history perubahan followers format .txt (Default 1 minute mengikuti char bar)

## Settings
- Merubah kecepatan refresh followers yang ditampilkan di terminal
Atur detik di variable SLEEPREFRESH di baris 11
```python
SLEEPREFRESH = 0.8 
```
- Merubah berapa menit untuk menampilkan Bar Chart (Contoh 3 menit, maka selama 3 menit sebelumnya akan disimpan/ditampilkan di Bar Chart berapa jumlah penaikan/pengurangan follower)
`$ python3 main.py --update 3`

- Merubah jumlah char bar yang ditampilkan dalam satu frame (Contoh 5, maka setiap frame/gambar hanya berisi maximal 5 char bar)
`$ python3 main.py --showbar 5`

- Mengganti alamat file log perubahan follower (default sesuai username IG)
`$ python3 main.py --output hasil.txt`

## Contoh
1. Jalankan perintah di terminal/cmd
`$ python3 main.py`

2. Masukkan username instagram yang akan dipantau
`Username : @cristiano`

3. Default waktu refresh follower yang ditampilkan pada terminal adalah 1 detik
maka setiap 1 detik akan di print di terminal, contoh output :
>Username : @cristiano
09:41:30 | 348.340.607 (+0)
09:41:32 | 348.340.618 (+11)
09:41:34 | 348.340.623 (+5)
09:41:36 | 348.340.628 (+5)

4. Bar Chart akan di tambahkan setiap waktu yang ditentukan (Default 1 menit) dan disimpan dalam format .jpg dengan lokasi gambar yaitu username.jpg

5. Setiap log perubahan pada Bar Chart akan disimpan (Default username.txt)

[![Visits Badge](https://badges.pufler.dev/visits/RTechnoS/instagram_static?style=for-the-badge&color=blue)](https://github.com/RTechnoS/RTechnoS)
