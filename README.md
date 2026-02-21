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
        - Buat folder apps:
            ```
            mkdir apps
            cd apps
            ```
        - Buat apps utama:
            ```
            python ../manage.py startapp accounts
            python ../manage.py startapp invitations
            python ../manage.py startapp rsvp
            
            jalankan 1 per 1
            ```
        - Kembali ke root
            ```
            cd..
            ```
        - Struktur saat ini
            invitation_be/
            │
            ├── apps/
            │   ├── accounts/
            │   ├── invitations/
            │   ├── rsvp/
            │
            ├── config/
            ├── manage.py
            └── venv/

