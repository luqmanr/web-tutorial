# Materi Belajar Vue.js untuk Pemula

Materi ini disusun bertahap: **JavaScript → HTML → DOM → Interaksi JS & DOM → Vue.js 3 → Bootstrap**. Konsepnya dibangun satu per satu supaya kamu paham *kenapa* Vue.js itu ada, bukan sekadar *cara pakainya*.

---

## Bagian 1: Konsep Dasar JavaScript

Vue.js dibangun di atas JavaScript, jadi wajib paham konsep dasarnya dulu.

### 1.1 Variabel

```javascript
let nama = "Budi";      // bisa diubah
const umur = 25;        // tidak bisa diubah

nama = "Andi";          // ✅ boleh
// umur = 30;           // ❌ error, karena const

```

### 1.2 Tipe Data

```javascript
let teks = "Halo";          // string
let angka = 10;             // number
let benar = true;           // boolean
let kosong = null;          // null (kosong sengaja)

```

### 1.3 Function

```javascript
// Cara 1: deklarasi biasa
function sapa(nama) {
  return "Halo, " + nama;
}

// Cara 2: arrow function (standar penulisan di Vue 3)
const sapa2 = (nama) => {
  return `Halo, ${nama}`;
};

console.log(sapa("Budi"));   // "Halo, Budi"
console.log(sapa2("Andi"));  // "Halo, Andi"

```

> **Catatan:** `${nama}` di dalam tanda backtick (```) disebut **template literal** — cara modern menggabungkan string.

### 1.4 Array

```javascript
let buah = ["Apel", "Mangga", "Jeruk"];

console.log(buah[0]);        // "Apel"
buah.push("Pisang");          // tambah di akhir
console.log(buah.length);     // 4

// Loop array
buah.forEach((item) => {
  console.log(item);
});

```

### 1.5 Object

```javascript
let mahasiswa = {
  nama: "Sinta",
  jurusan: "Informatika",
  semester: 4
};

console.log(mahasiswa.nama);     // "Sinta"
mahasiswa.semester = 5;          // ubah nilai

```

---

## Bagian 2: HTML Dasar

HTML adalah kerangka halaman web. Struktur minimalnya:

```html
<!DOCTYPE html>
<html>
<head>
  <title>Halaman Pertamaku</title>
</head>
<body>
  <h1>Selamat Datang</h1>
  <p id="pesan">Ini paragraf.</p>
  <button class="tombol">Klik Aku</button>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
</body>
</html>

```

**Poin penting:**

* `id` → penanda **unik** untuk satu elemen (satu halaman hanya boleh satu `id` sama)
* `class` → penanda yang bisa dipakai berulang, biasanya untuk styling

---

## Bagian 3: Apa Itu DOM?

**DOM (Document Object Model)** adalah representasi halaman HTML dalam bentuk "pohon" yang bisa dibaca dan dimanipulasi oleh JavaScript.

Saat browser membaca HTML-mu, dia mengubahnya jadi struktur seperti ini:

```
document
└── html
    ├── head
    │   └── title
    └── body
        ├── h1
        ├── p (id="pesan")
        └── button

```

**Analogi sederhana:** HTML itu seperti *cetakan kue* mentah, DOM itu *kuenya* yang sudah jadi di browser — dan JavaScript bisa memotong, menambah, atau menghias kue itu kapan saja.

---

## Bagian 4: Interaksi JavaScript dengan DOM (Cara Manual)

JavaScript bisa **mengubah halaman tanpa reload**.

### 4.1 Mengambil dan mengubah elemen

```html
<p id="pesan">Teks awal</p>

<script>
  // 1. Ambil elemen dari DOM
  let elemen = document.getElementById("pesan");

  // 2. Ubah isinya
  elemen.innerText = "Teks sudah berubah!";
</script>

```

### 4.2 Menangani event (klik, ketik, dll)

```html
<button id="tombol">Klik Aku</button>
<p id="hasil">Belum diklik</p>

<script>
  let tombol = document.getElementById("tombol");
  let hasil = document.getElementById("hasil");
  let hitung = 0;

  tombol.addEventListener("click", function () {
    hitung++;
    hasil.innerText = "Diklik " + hitung + " kali";
  });
</script>

```

### 4.3 Membuat daftar dari data

```html
<ul id="daftar"></ul>

<script>
  let buah = ["Apel", "Mangga", "Jeruk"];
  let daftar = document.getElementById("daftar");

  buah.forEach(function (item) {
    let li = document.createElement("li");  // bikin elemen <li> baru
    li.innerText = item;
    daftar.appendChild(li);                  // masukkan ke <ul>
  });
</script>

```

### 😩 Masalahnya dengan cara manual

1. Harus **cari manual** setiap elemen (`getElementById`)
2. Harus **update manual** setiap perubahan data
3. Kode cepat berantakan ketika aplikasi membesar karena data dan tampilan tidak terhubung otomatis

👉 **Itulah masalah yang diselesaikan Vue.js 3.**

---

## Bagian 5: Vue.js 3 — Reactive State (`ref`)

### 5.1 Konsep Inti Vue 3

> **Vue menghubungkan STATE (Data) dengan TAMPILAN secara otomatis.**
> Di Vue 3, kita membuat state menggunakan fungsi `ref()`. Ketika `ref` berubah, tampilan di layar langsung ikut berubah.

```
┌─────────────┐     otomatis     ┌──────────┐
│ State (ref) │ ───────────────▶ │ TAMPILAN │
│   (Data)    │ ◀─────────────── │  (DOM)   │
└─────────────┘    interaksi     └──────────┘

```

### 5.2 Program Pertama Vue 3 (Composition API)

```html
<!DOCTYPE html>
<html>
<head>
  <!-- Import Vue 3 via CDN -->
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body>
  <div id="app">
    <h1>{{ pesan }}</h1>
    <p>Halo, {{ nama }}!</p>
    <input v-model="nama" placeholder="Tulis namamu">
  </div>

  <script>
    const { createApp, ref } = Vue;

    createApp({
      setup() {
        // Membuat reactive state dengan ref()
        const pesan = ref("Belajar Vue.js 3");
        const nama = ref("");

        // Data yang dikembalikan siap dipakai di HTML
        return { pesan, nama };
      }
    }).mount("#app");
  </script>
</body>
</html>

```

**Penjelasan Komponen Utama Vue 3:**

| Fungsi / Syntax | Fungsi di Vue 3 |
| --- | --- |
| `createApp({...})` | Membuat instance aplikasi Vue 3 |
| `setup()` | Tempat utama menulis semua logika, state, dan fungsi (Composition API) |
| `ref("...")` | Membungkus variabel biasa menjadi **reactive state** |
| `{{ pesan }}` | Menampilkan isi variabel di HTML |
| `v-model="nama"` | **Two-way binding**: Mengikat input HTML secara langsung dengan `ref("nama")` |

---

### 5.3 Directive Vue 3

Directive adalah atribut khusus berawalan `v-` untuk mengontrol elemen HTML:

#### a) `v-on` / `@` — Event Handling & Mengubah State

```html
<div id="app">
  <p>Jumlah klik: {{ hitung }}</p>
  <button @click="hitung++">Tambah</button>
  <button @click="reset">Reset</button>
</div>

<script>
  const { createApp, ref } = Vue;

  createApp({
    setup() {
      const hitung = ref(0);

      const reset = () => {
        // Di dalam script JS, wajib gunakan .value untuk mengakses/mengubah ref!
        hitung.value = 0;
      };

      return { hitung, reset };
    }
  }).mount("#app");
</script>

```

> ⚠️ **Aturan Emas `ref()`:**
> * Di dalam **JavaScript**: Wajib pakai `.value` (contoh: `hitung.value = 0`).
> * Di dalam **HTML Template**: Langsung panggil namanya (contoh: `{{ hitung }}`).
> 
> 

#### b) `v-if` / `v-else` — Kondisional

```html
<p v-if="nilai >= 75">Lulus 🎉</p>
<p v-else>Tidak lulus, coba lagi</p>

```

#### c) `v-for` — Looping List

```html
<div id="app">
  <ul>
    <li v-for="item in buah" :key="item">{{ item }}</li>
  </ul>
</div>

<script>
  const { createApp, ref } = Vue;

  createApp({
    setup() {
      const buah = ref(["Apel", "Mangga", "Jeruk"]);
      return { buah };
    }
  }).mount("#app");
</script>

```

#### d) `v-bind` / `:` — Binding Atribut

```html
<img :src="urlGambar" :alt="deskripsi">
<div :class="{ active: isAktif }">Kotak</div>

```

---

### 5.4 `computed()` — State Turunan Otomatis

`computed()` digunakan untuk nilai yang bergantung pada `ref` lain. Nilainya akan dihitung ulang secara otomatis *hanya* jika `ref` terkait berubah.

```html
<div id="app">
  <input v-model.number="harga" type="number">
  <input v-model.number="jumlah" type="number">
  <p>Total: Rp {{ total }}</p>
</div>

<script>
  const { createApp, ref, computed } = Vue;

  createApp({
    setup() {
      const harga = ref(10000);
      const jumlah = ref(2);

      // Otomatis terhitung ulang bila harga / jumlah berubah
      const total = computed(() => harga.value * jumlah.value);

      return { harga, jumlah, total };
    }
  }).mount("#app");
</script>

```

---

### 5.5 Mini Project: To-Do List (Vue 3 Style)

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body>
  <div id="app">
    <h1>To-Do List</h1>
    <input v-model="tugasBaru" @keyup.enter="tambahTugas" placeholder="Tulis tugas, tekan Enter">
    <button @click="tambahTugas">Tambah</button>

    <ul>
      <li v-for="(tugas, index) in daftarTugas" :key="index">
        <span :style="{ textDecoration: tugas.selesai ? 'line-through' : 'none' }">
          {{ tugas.teks }}
        </span>
        <button @click="tandaiSelesai(index)">✓</button>
        <button @click="hapusTugas(index)">✕</button>
      </li>
    </ul>

    <p v-if="daftarTugas.length === 0">Belum ada tugas 🎉</p>
    <p>Sisa tugas: {{ sisaTugas }}</p>
  </div>

  <script>
    const { createApp, ref, computed } = Vue;

    createApp({
      setup() {
        const tugasBaru = ref("");
        const daftarTugas = ref([
          { teks: "Belajar Vue 3", selesai: false },
          { teks: "Buat proyek", selesai: false }
        ]);

        const sisaTugas = computed(() => {
          return daftarTugas.value.filter(t => !t.selesai).length;
        });

        const tambahTugas = () => {
          if (tugasBaru.value.trim() === "") return;
          daftarTugas.value.push({ teks: tugasBaru.value, selesai: false });
          tugasBaru.value = "";
        };

        const tandaiSelesai = (index) => {
          daftarTugas.value[index].selesai = !daftarTugas.value[index].selesai;
        };

        const hapusTugas = (index) => {
          daftarTugas.value.splice(index, 1);
        };

        return {
          tugasBaru,
          daftarTugas,
          sisaTugas,
          tambahTugas,
          tandaiSelesai,
          hapusTugas
        };
      }
    }).mount("#app");
  </script>
</body>
</html>

```

---

## Bagian 6: Bootstrap + Vue 3 Integration

### 6.1 Cara Pakai via CDN

```html
<head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

```

### 6.2 Proyek Rapi: To-Do List UI Bootstrap (Vue 3)

```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body class="bg-light">
  <div id="app" class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">

        <div class="card shadow">
          <div class="card-body">

            <h1 class="card-title text-center mb-4">📋 To-Do List Vue 3</h1>

            <div class="input-group mb-3">
              <input v-model="tugasBaru" @keyup.enter="tambahTugas"
                     class="form-control" placeholder="Tulis tugas baru...">
              <button @click="tambahTugas" class="btn btn-primary">Tambah</button>
            </div>

            <div v-if="daftarTugas.length === 0" class="alert alert-info text-center">
              Belum ada tugas. Selamat bersantai! 🎉
            </div>

            <ul class="list-group">
              <li v-for="(tugas, index) in daftarTugas" :key="index"
                  class="list-group-item d-flex justify-content-between align-items-center">

                <span :class="{ 'text-decoration-line-through text-muted': tugas.selesai }"
                      @click="tandaiSelesai(index)" style="cursor: pointer">
                  {{ tugas.teks }}
                </span>

                <span class="badge" :class="tugas.selesai ? 'bg-success' : 'bg-warning'">
                  {{ tugas.selesai ? 'Selesai' : 'Belum' }}
                </span>

                <button @click="hapusTugas(index)" class="btn btn-sm btn-outline-danger">✕</button>
              </li>
            </ul>

            <div class="mt-3 text-center text-muted">
              Sisa tugas: <strong>{{ sisaTugas }}</strong>
            </div>

          </div>
        </div>

      </div>
    </div>
  </div>

  <script>
    const { createApp, ref, computed } = Vue;

    createApp({
      setup() {
        const tugasBaru = ref("");
        const daftarTugas = ref([
          { teks: "Belajar Vue 3", selesai: false },
          { teks: "Buat proyek", selesai: false }
        ]);

        const sisaTugas = computed(() => {
          return daftarTugas.value.filter(t => !t.selesai).length;
        });

        const tambahTugas = () => {
          if (tugasBaru.value.trim() === "") return;
          daftarTugas.value.push({ teks: tugasBaru.value, selesai: false });
          tugasBaru.value = "";
        };

        const tandaiSelesai = (index) => {
          daftarTugas.value[index].selesai = !daftarTugas.value[index].selesai;
        };

        const hapusTugas = (index) => {
          daftarTugas.value.splice(index, 1);
        };

        return {
          tugasBaru,
          daftarTugas,
          sisaTugas,
          tambahTugas,
          tandaiSelesai,
          hapusTugas
        };
      }
    }).mount("#app");
  </script>
</body>
</html>

```

---

## Ringkasan Perjalanan

| Tahap | Yang Dipelajari | Manfaat |
| --- | --- | --- |
| **JavaScript** | Variabel, function, array, object | Fondasi logika program |
| **HTML & DOM** | Elemen HTML dan manipulasi DOM | Memahami cara kerja browser |
| **Vue 3 State (`ref`)** | `setup()`, `ref()`, `.value` | Data berubah → UI otomatis terbarui |
| **Vue Directives** | `v-model`, `@click`, `v-if`, `v-for` | Interaksi data dan elemen HTML yang efisien |
| **Vue Computed** | `computed()` | Perhitungan otomatis tanpa event listener manual |
| **Bootstrap** | Grid, Card, Badge, Alert | UI rapi tanpa harus menulis CSS rumit |
