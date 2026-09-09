"""允许 `python -m gateway` 直接运行。"""

import sys

from .main import main

if __name__ == "__main__":
    sys.exit(main())
