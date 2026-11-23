import unittest
import sys
from pathlib import Path

# Add src to pythonpath
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

def verify():
    print("=== Running Complete Regression Test Suite ===")
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    if not res.wasSuccessful():
        print("Verification FAILED.")
        sys.exit(1)
    print("=== All Regression Tests PASSED Successfully ===")

if __name__ == "__main__":
    verify()
