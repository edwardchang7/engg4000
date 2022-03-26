import os
import shutil
import unittest


class TestConverter(unittest.TestCase):
    def test_batch_convert(self):
        # Delete if converted_compositions already exists
        if os.path.isdir("src/backend/mxl_to_abc/converted_compositions"):
            shutil.rmtree("src/backend/mxl_to_abc/converted_compositions")

        os.system("python src/backend/mxl_to_abc/converter.py")

        # Check that converted_compositions was recreated
        self.assertTrue(os.path.isdir("src/backend/mxl_to_abc/converted_compositions"))
