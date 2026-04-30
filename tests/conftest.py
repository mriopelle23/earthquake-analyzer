import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEST_DB_PATH = os.path.join(BASE_DIR, "instance", "test_earthquakes.sqlite3")

os.environ["DATABASE_PATH"] = TEST_DB_PATH