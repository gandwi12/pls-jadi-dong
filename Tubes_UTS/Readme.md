# Food Delivery System

Sistem delivery makanan berbasis Flask dengan frontend interaktif menggunakan Jinja2, HTML, CSS, dan JavaScript.

## Fitur

- **Homepage**: Halaman utama dengan hero section dan fitur unggulan
- **Menu**: Menampilkan daftar menu dari berbagai restoran dengan tombol "Tambah ke Keranjang"
- **Keranjang (Order)**: Menampilkan item yang ditambahkan, form pengiriman, dan tombol untuk submit pesanan
- **Pembayaran**: Form pemilihan metode pembayaran
- **Restoran**: Daftar restoran dengan link ke menu masing-masing
- **Profil Pengguna**: Halaman profil dengan data pengguna

## Teknologi

- **Backend**: Flask 3.0.0, Python
- **Database**: MySQL (dengan mysqlclient)
- **Frontend**: HTML5, CSS3 (Responsive), Vanilla JavaScript (ES6)
- **Tools**: Flask-SQLAlchemy, Flask-Migrate, python-dotenv

## Instalasi

### 1. Clone repository
```bash
git clone https://github.com/gandwi12/Tubes-EAI.git
cd Tubes-EAI/Tubes_UTS
```

### 2. Buat virtual environment (optional tapi recommended)
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

## Menjalankan Aplikasi

### Cara 1: Jalankan dari folder Tubes_UTS
```powershell
cd c:\Users\admin\Downloads\Uts EAI\Tubes-EAI\Tubes_UTS
python api_gateway/app.py
```

### Cara 2: Menggunakan Flask CLI
```powershell
cd c:\Users\admin\Downloads\Uts EAI\Tubes-EAI\Tubes_UTS
$env:FLASK_APP = 'api_gateway.app'
python -m flask run --host=127.0.0.1 --port=5000
```

Setelah aplikasi berjalan, buka browser dan akses: **http://127.0.0.1:5000**

## Struktur Folder

```
Tubes_UTS/
├── api_gateway/
│   └── app.py              # Flask app utama dengan routes
├── menu/
│   ├── app.py
│   ├── config.py
│   └── models.py
├── order/
│   ├── app.py
│   ├── config.py
│   └── models.py
├── payment/
│   ├── app.py
│   ├── config.py
│   └── models.py
├── restoran/
│   ├── app.py
│   ├── config.py
│   └── models.py
├── User/
│   ├── app.py
│   ├── config.py
│   └── models.py
├── static/
│   ├── style.css           # Styling responsif
│   └── app.js              # Interaktivitas (cart, form handling)
├── templates/
│   ├── base.html           # Template dasar (base layout)
│   ├── index.html          # Halaman utama
│   ├── menu.html           # Halaman menu
│   ├── order.html          # Halaman keranjang & form pengiriman
│   ├── payment.html        # Halaman pembayaran
│   ├── restoran.html       # Halaman daftar restoran
│   └── user.html           # Halaman profil pengguna
├── requirements.txt        # Python dependencies
└── Readme.md               # File ini
```

## Cara Menggunakan Frontend

### 1. **Homepage** (`/`)
- Klik tombol "Lihat Menu" untuk melihat daftar makanan
- Klik "Temukan Restoran" untuk melihat daftar restoran

### 2. **Menu** (`/menu`)
- Lihat daftar makanan dengan harga dan deskripsi
- Klik tombol "Tambah" untuk menambahkan item ke keranjang
- Counter keranjang di navbar akan berubah secara real-time

### 3. **Keranjang & Order** (`/order`)
- Lihat daftar item yang sudah ditambahkan
- Gunakan tombol **+** dan **-** untuk mengubah jumlah item
- Klik "Hapus" untuk menghapus item dari keranjang
- Isi form nama, alamat, dan catatan
- Klik "Buat Pesanan" untuk submit order (item keranjang akan dihapus setelah submit)

### 4. **Pembayaran** (`/payment`)
- Pilih metode pembayaran:
  - **Cash on Delivery (COD)**
  - **Transfer Bank**
  - **E-Wallet**
- Total pembayaran ditampilkan otomatis
- Klik "Bayar" untuk selesaikan transaksi

### 5. **Restoran** (`/restoran`)
- Lihat daftar restoran yang tersedia
- Klik "Lihat Menu" untuk melihat menu dari restoran tertentu

### 6. **Profil Pengguna** (`/user`)
- Lihat informasi profil pengguna
- Klik "Edit Profil" untuk mengubah data (perlu di-implementasikan di backend jika diperlukan)

## Fitur Interaktif (JavaScript)

### Keranjang (Cart)
- **localStorage**: Data keranjang disimpan di browser, persisten setelah refresh page
- **Add to Cart**: Klik "Tambah" di menu untuk menambahkan item
- **Update Quantity**: Gunakan **+/-** di halaman order untuk ubah jumlah
- **Remove Item**: Klik "Hapus" untuk delete item dari keranjang
- **Real-time Counter**: Badge "Cart" di navbar menunjukkan jumlah item

### Form Handling
- **Order Form**: Submit ke `/order` (POST) dengan data cart, nama, alamat, catatan
- **Payment Form**: Submit ke `/payment` (POST) dengan metode pembayaran yang dipilih
- **Validation**: Input name dan address wajib diisi sebelum submit

## Customization

### Mengubah Nama Brand
Edit `templates/base.html` bagian `.brand`:
```html
<a class="brand" href="/">FoodDelivery</a>  <!-- Ubah teks ini -->
```

### Menambah Item Menu
Edit `api_gateway/app.py` di `SAMPLE_ITEMS`:
```python
SAMPLE_ITEMS = [
    {'id': 5, 'name': 'Bakso Sapi', 'price': '22000', 'description': 'Bakso daging sapi premium', 'image_url': '/static/img/bakso.jpg'},
    # ... tambah item lainnya
]
```

### Styling
Edit `static/style.css` untuk customize warna, font, layout, dll.

## Development

### Debug Mode
Flask app berjalan di debug mode secara default (`debug=True` di `api_gateway/app.py`). Browser akan auto-reload saat ada perubahan di code.

### Test Endpoints
Gunakan tools seperti Postman atau curl untuk test API:
```bash
# Test POST /order
curl -X POST http://127.0.0.1:5000/order \
  -H "Content-Type: application/json" \
  -d '{"cart":[{"id":1,"name":"Nasi Goreng","price":"25000","qty":2}],"name":"Joni","address":"Jl Merdeka"}'

# Test POST /payment
curl -X POST http://127.0.0.1:5000/payment \
  -H "Content-Type: application/json" \
  -d '{"method":"cod"}'
```

## Troubleshooting

### Port 5000 sudah digunakan
Ubah port di `api_gateway/app.py`:
```python
app.run(host='127.0.0.1', port=5001, debug=True)  # Gunakan port 5001 atau port lain
```

### Module not found: mysqlclient error
Pastikan sudah install MySQL driver yang tepat untuk sistem Anda, atau gunakan SQLite untuk development:
```python
# Di api_gateway/app.py, ubah config jika perlu SQLite:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fooddelivery.db'
```

### Template not found error
Pastikan struktur folder benar:
- `api_gateway/app.py` berada di subfolder `api_gateway/`
- `templates/` dan `static/` berada di parent folder (Tubes_UTS)
- Flask app di-initialize dengan `template_folder='../templates'` dan `static_folder='../static'`

## Next Steps (Backend Integration)

Untuk integrasi lengkap dengan backend:

1. **Database Models**: Gunakan SQLAlchemy untuk define User, Restaurant, Menu, Order, Payment models
2. **Authentication**: Implementasikan login/register dengan Flask-Login atau JWT
3. **API Routes**: Extend routes untuk CRUD operations
4. **Payment Gateway**: Integrasi dengan Midtrans, Stripe, atau provider lain
5. **Email Notifications**: Kirim email konfirmasi order dan status delivery
6. **Real-time Updates**: Gunakan WebSocket atau polling untuk tracking pesanan

## License

MIT

## Author

Tubes EAI - Food Delivery System  
Repository: https://github.com/gandwi12/Tubes-EAI
