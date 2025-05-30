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
    ```
    mysql -u root -p
    ```
2. Buat database baru
    ```sql
    CREATE DATABASE ats_database
    ```

#### Seed Database
1. Buat file `.env` di root project
2. Jalankan seeder
    ```bash
    python src/scripts/seeder.py
    ```

## Run Application
```bash
flet run
```