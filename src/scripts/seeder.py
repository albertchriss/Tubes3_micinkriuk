import sys
sys.path.append("src")

from models.model import *
from core.database import create_tables


if __name__ == "__main__":
    create_tables()