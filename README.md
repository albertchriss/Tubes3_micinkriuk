# Tubes Strategi Algoritma 3

## Setup

1. Buat virtual environment

   ```bash
   python -m venv venv
   ```

2. Aktifkan virtual environment
    - Windows

      ```bash
      venv\Scripts\activate
      ```

    - Linux/MacOS

      ```bash
      source venv/bin/activate
      ```

3. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

## Database Setup

#### Buat MySQL Database

1. Buka MySQL Command Line Client

    ```bash
    mysql -u root -p
    ```

2. Buat database baru

    ```sql
    CREATE DATABASE ats_database
    ```

3. Keluar dari MySQL

    ```sql
    exit;
    ```

4. Ganti ke folder `data`

    ```bash
    cd data
    ```

5. Load database dari asisten

    ```sql
    mysql -u root -p ats_database < tubes3_seeding.sql
    ```

#### Seed Database

1. Buat file `.env` di root project

    ```bash
    cp .env.example .env
    ```

2. Edit `DATABASE_URL`

3. Jalankan seeder

    ```bash
    python src/scripts/seeder.py
    ```

## Run Application

```bash
flet run
```
