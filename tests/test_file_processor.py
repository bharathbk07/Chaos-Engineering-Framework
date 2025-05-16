import os
import json
import unittest
from unittest.mock import patch, mock_open
from src.utils.file_processor import process_file_or_folder

class TestFileProcessor(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="This is a test file with enough content to split into chunks.")
    def test_process_file(self, mock_file):
        expected_output = [
            {"content": "This is a test file with enough content to split into", "role": "user"},
            {"content": "chunks.", "role": "user"}
        ]
        result = process_file_or_folder("test_file.txt")
        self.assertEqual(result, expected_output)
        mock_file.assert_called_once_with("test_file.txt", 'r', encoding='utf-8')

    @patch("os.path.isdir", return_value=True)
    @patch("os.walk")
    @patch("builtins.open", new_callable=mock_open, read_data="This is a test file in a directory.")
    def test_process_directory(self, mock_file, mock_walk, mock_isdir):
        mock_walk.return_value = [("test_dir", [], ["test_file.txt"])]
        expected_output = [
            {"content": "This is a test file in a directory.", "role": "user"}
        ]
        result = process_file_or_folder("test_dir")
        self.assertEqual(result, expected_output)
        mock_file.assert_called_once_with("test_dir/test_file.txt", 'r', encoding='utf-8')

    def test_invalid_file(self):
        result = process_file_or_folder("invalid_file.txt")
        self.assertEqual(result, [])

    def test_invalid_directory(self):
        result = process_file_or_folder("invalid_directory")
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()