import unittest
from pathlib import Path

import jpype


class JVMSetupTest(unittest.TestCase):
    def test_jvm_can_be_loaded(self):
        jvm_path = Path(jpype.getDefaultJVMPath())
        self.assertTrue(jvm_path.is_file(), f"JVM library not found: {jvm_path}")

        if not jpype.isJVMStarted():
            jpype.startJVM(str(jvm_path), convertStrings=True)

        self.assertTrue(jpype.isJVMStarted())


if __name__ == "__main__":
    unittest.main()
