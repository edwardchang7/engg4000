import unittest
import shutil
import os

class TestConverter(unittest.TestCase):
  
  def test_batch_convert(self):

    # check for converted_compositions directory if its there delete it
    if(os.path.isdir("src/backend/mxl_to_abc/converted_compositions")):
      shutil.rmtree("src/backend/mxl_to_abc/converted_compositions")
    
    os.system("python src/backend/mxl_to_abc/converter.py")

    # check if folder of compositions have been recreated
    self.assertTrue(os.path.isdir("src/backend/mxl_to_abc/converted_compositions"))