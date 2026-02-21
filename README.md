# Aplikasi API undangan online

## Intro
Baik 👍 kita mulai dari nol sampai siap pakai:

    ✅ Buat virtual environment
    ✅ Install Django + DRF
    ✅ Struktur clean architecture
    ✅ Buat apps
    ✅ Koneksi ke MySQL

Kita pakai:

    - Django
    - Django REST Framework
    - MySQL

## 1 📦 Install requirements
    ```
    pip install -r requirements.txt
    ```
## 2 🏗 pasang virtual env python
### Cara pasang venv
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
## 3 📝 Proses Build Aplikasi
    1. Buat Project Django
        ```
        django-admin startproject config .
        ```

    2. Buat Struktur Apps Clean Architecture
        - struktur awal
            invitation_be/
            │
            ├── config/
            │   ├── settings.py
            │   ├── urls.py
            │
            └── manage.py
