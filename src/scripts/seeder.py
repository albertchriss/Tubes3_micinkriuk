import sys
sys.path.append("src")

from models.model import *
from core.database import create_tables
from core.service import *
from pathlib import Path
from faker import Faker
import random

fake = Faker()
fake.seed_instance(69)  # Seed Faker for reproducibility

def seed_cv_to_db(path: Path, application_role: str):
    """
    Fungsi untuk memasukkan data sebuah CV ke dalam database.
    """
    applicants = get_all_applicants()
    chosen_applicant = random.choice(applicants)
    insert_application(
        applicant_id=chosen_applicant.applicant_id, # type: ignore
        application_role=application_role,
        cv_path=path.absolute().as_posix()
    )

    
def seed_applicants(num_applicants: int):
    """
    Fungsi untuk membuat sejumlah data pelamar palsu dan memasukkannya ke dalam database.
    """
    global first_names, last_names, date_of_births, addresses, phone_numbers

    first_names = [fake.unique.first_name() for _ in range(num_applicants)]
    last_names = [fake.last_name() for _ in range(num_applicants)]
    date_of_births = [fake.date_of_birth(minimum_age=18, maximum_age=50) for _ in range(num_applicants)]
    addresses = [fake.address() for _ in range(num_applicants)]
    phone_numbers = [fake.unique.phone_number() for _ in range(num_applicants)]
    for i in range(num_applicants):
        insert_applicant(
            first_name=first_names[i],
            last_name=last_names[i],
            date_of_birth=date_of_births[i],
            address=addresses[i],
            phone_number=phone_numbers[i]
        )


def process_cv_files():
    """
    Melakukan iterasi pada folder data,
    mengambil 20 file PDF pertama secara leksikografis dari setiap kategori,
    dan memprosesnya.
    """

    # --- Mendapatkan direktori data ---
    data_dir = Path("data")
    if not data_dir.is_dir():
        print(f"Error: Direktori data utama '{data_dir}' tidak ditemukan.")
        return
    
    # --- Iterasi pada setiap subdirektori dalam direktori data ---
    try:
        categories = sorted([d for d in data_dir.iterdir() if d.is_dir()])
    except Exception as e:
        print(f"Tidak dapat membaca direktori kategori: {e}")
        return
    
    print(f"Menemukan {len(categories)} kategori di direktori data. Memulai pemrosesan...")
    for category in categories:
        print(f"Memproses kategori: {category.name}")
        try:
            # --- Mengambil semua file PDF dalam kategori ---
            pdf_files = sorted(category.glob("*.pdf"))

            for pdf_file in pdf_files[:20]:
                seed_cv_to_db(pdf_file, category.name)

            # hapus file pdf yang tidak dipilih
            for pdf_file in pdf_files[20:]:
                try:
                    pdf_file.unlink()  # Hapus file yang tidak dipilih
                except Exception as e:
                    print(f"Error saat menghapus file '{pdf_file}': {e}")
                
        except Exception as e:
            print(f"Error saat memproses kategori '{category.name}': {e}")

if __name__ == "__main__":
    create_tables()
    seed_applicants(200) 
    process_cv_files()
    print("Seeding completed successfully.")