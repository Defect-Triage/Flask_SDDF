# import unittest
# import pandas as pd
# from app import process_data, sync_tickets 
# import HtmlTestRunner

# class Testapp(unittest.TestCase):

    
#   def test_process_data(self):
#     title = "test title"
#     platform = "Gen20x.i2"
#     threshold = 0.5

#     result = process_data(title, platform, threshold)

#     # Check if an error occurred
#     if isinstance(result, list) and 'error' in result[0]:
#         expected_error = f"File not found: currentdefects_{platform.lower()}.xlsx"
#         self.assertEqual(result, [{'error': expected_error}], f"Unexpected error: {result}")

#     # Check if duplicates are present (only if no error occurred)
#     else:
#         expected_duplicates = [{'Defect ID': 'DEFECTID1', 'Title': 'test title', 'Score': 3.0}]
#         self.assertEqual(result, expected_duplicates, f"Unexpected result: {result}")


#   def test_sync_tickets(self):
#      result = sync_tickets()
#      self.assertEqual(result, "Database updated successfully")

# if __name__ == '__main__':
#     unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test-reports'))

# import unittest
# import HtmlTestRunner
# from unittest.mock import patch
# from parse import process_data, sync_tickets, main


# class TestAppFunctions(unittest.TestCase):

#     @patch('parse.process_data') 
#     def test_find_duplicates_option(self, mock_process_data):
#         # Arrange
#         args = ["--find-duplicates", "--title", "Defect Title", "--platform", "Platform", "--threshold", "0.5"]

#         # Act
#         with patch('sys.argv', ['parse.py'] + args):
#             main()
    
#         # Assert
#         mock_process_data.assert_called_with("Defect Title", "Platform", 0.5)

#     @patch('parse.sync_tickets')  
#     def test_sync_tickets_option(self, mock_sync_tickets):
#         # Arrange
#         args = ["--sync-tickets"]

#         # Act
#         with patch('sys.argv', ['parse.py'] + args):
#             main()

#         # Assert
#         mock_sync_tickets.assert_called_once()

# if __name__ == '__main__':
#     unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test-reports'))











import unittest
import HtmlTestRunner
from unittest.mock import patch
from parse import process_data, sync_tickets, main


class TestAppFunctions(unittest.TestCase):

    def log_message(self, message):
        """Log a custom message to be displayed in the HTML report."""
        self._results.append({'status': 'info', 'message': message})

    def setUp(self):
        """Set up the test."""
        self._results = []  # List to store custom messages

    @patch('parse.process_data') 
    def test_find_duplicates_option(self, mock_process_data):
        # Arrange
        args = ["--find-duplicates", "--title", "Defect Title", "--platform", "Platform", "--threshold", "0.5"]

        # Act
        with patch('sys.argv', ['parse.py'] + args):
            main()

        # Assert
        mock_process_data.assert_called_with("Defect Title", "Platform", 0.5)
        
        # Log a custom message
        self.log_message('Duplicates found in Platform')

    @patch('parse.sync_tickets')  
    def test_sync_tickets_option(self, mock_sync_tickets):
        # Arrange
        args = ["--sync-tickets"]

        # Act
        with patch('sys.argv', ['parse.py'] + args):
            main()

        # Assert
        mock_sync_tickets.assert_called_once()

        # Log a custom message
        self.log_message('Updated database')

    def tearDown(self):
        """Tear down the test and print custom messages to the HTML report."""
        for result in self._results:
            status = result['status']
            message = result['message']
            if status == 'info':
                self.log_message(message)


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test-reports'))
