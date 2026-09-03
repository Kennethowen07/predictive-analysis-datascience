# Menyelesaikan Permasalahan Perusahaan Jaya Jaya Maju

## Business Understanding

Jaya Jaya Maju adalah perusahaan multinasional yang berdiri sejak tahun 2000 dengan lebih dari 1000 karyawan. Perusahaan kesulitan mengelola karyawan dan attrition rate-nya menembus 10 persen. Departemen HR ingin tahu faktor apa yang mendorong karyawan keluar, dan butuh dashboard untuk memantaunya.

### Permasalahan bisnis

1. Attrition rate tinggi, yaitu 16.9 persen dari karyawan yang datanya lengkap.
2. HR belum tahu faktor mana yang paling berkaitan dengan keluarnya karyawan.
3. HR belum punya alat monitoring.
4. HR belum bisa mengidentifikasi karyawan berisiko sebelum mereka mengundurkan diri.

### Objektif proyek

1. Eksplorasi data karyawan untuk mencari faktor yang berkaitan dengan attrition.
2. Membangun business dashboard.
3. Membangun model prediksi attrition.
4. Menyusun rekomendasi untuk HR.

### Persiapan

Sumber data.

```
https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/employee/employee_data.csv
```

Dataset berisi 1470 baris dan 35 kolom. Kolom `Attrition` hanya terisi pada 1058 baris. Sisanya 412 baris kosong dan diperlakukan sebagai karyawan yang statusnya belum diketahui.

Setup environment.

```
conda create -n bpds python=3.12
conda activate bpds
pip install -r requirements.txt
```

Menjalankan database dan Metabase.

```
docker run -d --name postgres-hr -e POSTGRES_USER=root -e POSTGRES_PASSWORD=root123 -e POSTGRES_DB=hr_db -p 5433:5432 postgres:16
docker run -d --name metabase -p 3000:3000 metabase/metabase
```

Notebook mengirim data ke PostgreSQL lewat SQLAlchemy, lalu Metabase membaca tabel `employees` dari database itu.

## Business Dashboard

Dashboard dibuat di Metabase dengan nama `HR Attrition Dashboard` dan berisi sepuluh kartu.

Tiga kartu ringkasan menampilkan attrition rate keseluruhan, komposisi karyawan bertahan dan keluar, serta jumlah karyawan yang diprediksi berisiko.

Enam kartu berikutnya memecah attrition rate berdasarkan lembur, posisi, status pernikahan, level jabatan, dan work life balance, ditambah perbandingan rata-rata gaji antara yang bertahan dan yang keluar.

Kartu terakhir berupa tabel berisi dua puluh karyawan dengan probabilitas keluar tertinggi, lengkap dengan posisi, status lembur, dan gaji, supaya HR bisa langsung menindaklanjuti.

Akses dashboard.

```
URL       http://localhost:3000
Email     root@mail.com
Password  root123
```

Berkas `metabase.db.mv.db` ada di folder submission. Untuk membukanya, jalankan container Metabase dengan me-mount berkas itu ke `/metabase.db/metabase.db.mv.db`.

## Menjalankan Sistem Machine Learning

Model yang dipakai Random Forest Classifier dengan `class_weight="balanced"` karena kelasnya timpang. Data dibagi 80 persen latih dan 20 persen uji secara stratified.

Pada threshold bawaan 0.5, recall untuk kelas karyawan keluar hanya 0.39. Artinya lebih dari separuh karyawan berisiko tidak terdeteksi. Bagi HR, kehilangan karyawan jauh lebih mahal daripada mengajak bicara karyawan yang ternyata bertahan, jadi threshold diturunkan ke 0.3.

Performa pada threshold 0.3.

| Metrik | Bertahan | Keluar |
|---|---|---|
| Precision | 0.94 | 0.35 |
| Recall | 0.70 | 0.78 |
| F1-score | 0.80 | 0.48 |

Akurasi keseluruhan 0.71. Model menangkap 28 dari 36 karyawan yang benar-benar keluar pada data uji.

Menjalankan prediksi.

```
python prediction.py data/employee_data.csv
```

Script membaca CSV, melakukan encoding, menyelaraskan kolom dengan kolom saat pelatihan, lalu menyimpan hasilnya ke `prediction_result.csv` berisi `EmployeeId`, `attrition_proba`, dan `attrition_pred`. File masukan boleh tidak punya kolom `Attrition`, jadi script ini bisa dipakai untuk karyawan yang statusnya belum diketahui.

Dari 412 karyawan tanpa label, model menandai 131 orang sebagai berisiko keluar.

## Conclusion

Attrition rate Jaya Jaya Maju ada di 16.9 persen, yaitu 179 dari 1058 karyawan.

Lembur punya selisih terbesar. Karyawan yang lembur keluar pada tingkat 31.9 persen, hampir tiga kali lipat dibanding yang tidak lembur di 10.8 persen.

Posisi sangat menentukan. Sales Representative mencapai 43.1 persen dan Laboratory Technician 26.1 persen, sementara Research Director hanya 3.2 persen.

Karyawan awal karier paling rentan. Level jabatan 1 ada di 27.4 persen. Rata-rata karyawan yang keluar berusia 33.5 tahun dengan gaji 4873, sedangkan yang bertahan berusia 37.8 tahun dengan gaji 6983. Total pengalaman kerja mereka juga lebih pendek, 8.3 tahun berbanding 12.1 tahun.

Kualitas pengalaman kerja juga berpengaruh. Karyawan dengan job involvement terendah keluar pada tingkat 40.0 persen, dibanding 9.5 persen di level tertinggi. Pola yang sama muncul pada work life balance terendah di 32.1 persen dan environment satisfaction terendah di 27.3 persen.

Karyawan tanpa stock option keluar pada tingkat 25.7 persen, sedangkan yang punya stock option level 2 hanya 7.3 persen. Karyawan lajang ada di 26.7 persen dibanding 13.4 persen pada yang menikah.

Temuan ini bersifat asosiatif, bukan sebab akibat. Beberapa faktor juga saling tumpang tindih, misalnya usia, gaji, level jabatan, dan lama pengalaman kerja bergerak bersamaan. Jenis kelamin dan performance rating tidak menunjukkan perbedaan berarti, jadi keduanya tidak dipakai sebagai dasar rekomendasi.

### Rekomendasi Action Items

1. Batasi dan pantau lembur, terutama di Sales dan Research and Development. Lembur punya selisih terbesar sekaligus paling bisa dikendalikan manajemen, tidak seperti usia atau masa kerja.

2. Audit beban kerja dan kompensasi pada posisi Sales Representative dan Laboratory Technician. Keduanya punya attrition rate tertinggi dan umumnya berada di level jabatan awal dengan gaji rendah.

3. Perluas pemberian stock option ke karyawan level 1 dan 2. Selisih antara yang punya dan tidak punya stock option lebih dari tiga kali lipat.

4. Buat program retensi untuk karyawan tahun pertama sampai ketiga, misalnya mentoring, jalur karier yang jelas, dan tinjauan gaji berkala. Kelompok ini yang paling banyak keluar.

5. Pakai skor job involvement, work life balance, dan environment satisfaction sebagai peringatan dini. Karyawan dengan skor 1 perlu segera diajak bicara oleh atasan langsungnya.

6. Gunakan daftar karyawan berisiko di dashboard sebagai antrean tindak lanjut bulanan. Model menandai 131 karyawan, tapi precision-nya 0.35, jadi daftar ini adalah prioritas percakapan retensi, bukan vonis bahwa mereka pasti keluar.
