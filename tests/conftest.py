import sys
from pathlib import Path
import pytest
from copy import deepcopy

# הוספת תיקיית השורש של הפרויקט ל-PATH כדי שפייתון ימצא את app.py
APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# עכשיו ה-Imports האלה יעבדו!
from app import app
from models import tasks

INITIAL_TASKS = deepcopy(tasks)

@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    tasks.extend(deepcopy(INITIAL_TASKS))
    yield
    tasks.clear()
    tasks.extend(deepcopy(INITIAL_TASKS))

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client