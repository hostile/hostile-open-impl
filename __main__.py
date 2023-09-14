import sys
import dotenv

MIN_PYTHON_VERSION = (3, 8, 0)

if sys.version_info < MIN_PYTHON_VERSION:
    print('Your python version is too old! Please use Python 3.8.0 or above!')
    sys.exit(-1)

dotenv.load_dotenv()

from hostile_open import app

app.run()
