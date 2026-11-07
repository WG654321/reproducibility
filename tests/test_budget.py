import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('runner', Path(__file__).resolve().parents[1] / 'scripts/run_experiment.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

class BudgetTests(unittest.TestCase):
    def test_persistent_reservation_and_stop(self):
        with tempfile.TemporaryDirectory() as directory:
            old = runner.ROOT
            runner.ROOT = Path(directory)
            try:
                meter = runner.Meter(10, 10, 0.1)
                meter.reserve('hello', 100)
                self.assertGreater(runner.Meter(10,10,0.1).spent, 0)
                with self.assertRaises(runner.StopExperiment):
                    meter.reserve('x' * 20000, 100)
            finally:
                runner.ROOT = old

if __name__ == '__main__':
    unittest.main()
