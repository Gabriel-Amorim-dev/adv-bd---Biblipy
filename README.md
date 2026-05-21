# 📚 Biblipy
 
A library management system built with **Django** and **PostgreSQL**, featuring an intuitive admin interface, PDF report generation, and Excel data export.
 
---
 
## 🚀 Features
 
- 📖 Book and library catalog management
- 🖼️ Cover image support for books
- 📄 PDF report generation
- 📊 Excel data export
- 🎨 Modern admin panel powered by Jazzmin
- 🔐 Environment-based configuration for secure deployments
---
 
## 🛠️ Tech Stack
 
| Technology | Purpose |
|---|---|
| Python / Django 6 | Web framework |
| PostgreSQL | Database |
| Jazzmin | Admin UI theme |
| ReportLab | PDF generation |
| OpenPyXL / Pandas | Excel export |
| Pillow | Image handling |
| python-dotenv | Environment variables |
 
---
 
## ⚙️ Prerequisites
 
- Python 3.11+
- PostgreSQL
- pip
---
 
## 📦 Installation
 
**1. Clone the repository**
 
```bash
git clone https://github.com/Gabriel-Amorim-dev/adv-bd---Biblipy.git
cd adv-bd---Biblipy
```
 
**2. Create and activate a virtual environment**
 
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```
 
**3. Install dependencies**
 
```bash
pip install -r requirements.txt
```
 
**4. Configure environment variables**
 
Copy the example file and fill in your values:
 
```bash
cp .env-example .env
```
 
Then edit `.env`:
 
```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=biblipy (or a name of your choice)
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```
 
**5. Apply migrations**
 
```bash
python manage.py migrate
```
 
**6. Create a superuser**
 
```bash
python manage.py createsuperuser
```
 
**7. Run the development server**
 
```bash
python manage.py runserver
```
 
Access the app at `http://localhost:8000` and the admin panel at `http://localhost:8000/admin`.
 
---
 
## 🗂️ Project Structure
 
```
adv-bd---Biblipy/
├── library/          # Main Django application
├── .env-example      # Environment variable template
├── .gitignore
└── requirements.txt
```
 
---
 
## 📋 Environment Variables
 
| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode (`True` / `False`) |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `DB_HOST` | Database host (e.g. `localhost`) |
| `DB_PORT` | Database port (default: `5432`) |
 
---
 
## 🤝 Contributing
 
Contributions are welcome! Feel free to open an issue or submit a pull request.
 
---
 
## 👤 Author
 
**Gabriel Amorim**
[GitHub](https://github.com/Gabriel-Amorim-dev)
