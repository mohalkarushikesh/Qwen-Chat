import os
import unittest

from app.main import app


class AppConfigTests(unittest.TestCase):
    def test_template_folder_exists(self):
        self.assertTrue(os.path.isdir(app.template_folder))
        self.assertTrue(os.path.exists(os.path.join(app.template_folder, "index.html")))


if __name__ == "__main__":
    unittest.main()
