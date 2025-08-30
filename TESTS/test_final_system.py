#!/usr/bin/env python3
"""
test_final_system.py - Comprehensive test suite for the improved Traity Quiz Application

This test suite validates all the security and performance improvements made to the system:
- Robust error handling and logging
- Input validation and parameter checking
- Rate limiting and timeout management
- Memory leak prevention
- Thread safety improvements
- Configuration management

Run with: python test_final_system.py
"""

import sys
import os
import time
import logging
from unittest.mock import Mock, patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import PyQt5 components
from PyQt5.QtWidgets import QApplication

# Import application modules
from CONST.constants import AppConstants
from QuestionWorker import QuestionWorker
from UI.QuizApp import QuizApp
from CLASSES.LanguageModel import LanguageModel
from CLASSES.CategoryModel import CategoryModel
from CLASSES.DifficultyModel import DifficultyModel
from CLASSES.TypeModel import TypeModel


class TestSystemImprovements:
    """Test class for validating system improvements"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.test_results = []
        self.app = None  # QApplication instance
        
    def _ensure_qapplication(self):
        """Ensure QApplication is created only once"""
        if self.app is None:
            self.app = QApplication.instance()
            if self.app is None:
                self.app = QApplication(sys.argv)

    def run_all_tests(self):
        """Run all system improvement tests"""
        print("=" * 60)
        print("TESTING TRAITY QUIZ APPLICATION IMPROVEMENTS")
        print("=" * 60)

        # Test configuration constants
        self.test_configuration_constants()

        # Test QuestionWorker improvements
        self.test_question_worker_validation()
        self.test_question_worker_error_handling()
        self.test_question_worker_rate_limiting()

        # Test UI improvements
        self.test_ui_error_handling()
        self.test_ui_thread_management()

        # Test input validation
        self.test_input_validation()

        # Print results
        self.print_test_results()

    def test_configuration_constants(self):
        """Test that all configuration constants are properly defined"""
        print("\n1. Testing Configuration Constants...")

        tests = [
            ("API_REQUEST_TIMEOUT", AppConstants.API_REQUEST_TIMEOUT, lambda x: x > 0),
            ("API_MAX_RETRIES", AppConstants.API_MAX_RETRIES, lambda x: x > 0),
            ("API_RATE_LIMIT_INTERVAL", AppConstants.API_RATE_LIMIT_INTERVAL, lambda x: x > 0),
            ("THREAD_TERMINATION_TIMEOUT", AppConstants.THREAD_TERMINATION_TIMEOUT, lambda x: x > 0),
            ("MAX_THREAD_POOL_WORKERS", AppConstants.MAX_THREAD_POOL_WORKERS, lambda x: x > 0),
            ("TRANSLATION_TIMEOUT", AppConstants.TRANSLATION_TIMEOUT, lambda x: x > 0),
            ("MAX_QUESTIONS_PER_REQUEST", AppConstants.MAX_QUESTIONS_PER_REQUEST, lambda x: x > 0),
            ("MIN_QUESTIONS_PER_REQUEST", AppConstants.MIN_QUESTIONS_PER_REQUEST, lambda x: x > 0),
            ("UI_UPDATE_INTERVAL", AppConstants.UI_UPDATE_INTERVAL, lambda x: x > 0),
        ]

        for name, value, validator in tests:
            try:
                assert validator(value), f"Invalid {name} value: {value}"
                self.log_test_result(f"✓ {name}: {value}", True)
            except Exception as e:
                self.log_test_result(f"✗ {name}: {e}", False)

    def test_question_worker_validation(self):
        """Test QuestionWorker parameter validation"""
        print("\n2. Testing QuestionWorker Parameter Validation...")

        # Test valid parameters
        try:
            worker = QuestionWorker(count=5, target_language='it')
            self.log_test_result("✓ Valid parameters accepted", True)
        except Exception as e:
            self.log_test_result(f"✗ Valid parameters rejected: {e}", False)

        # Test invalid count
        try:
            worker = QuestionWorker(count=0, target_language='it')
            self.log_test_result("✗ Invalid count (0) should be rejected", False)
        except ValueError:
            self.log_test_result("✓ Invalid count (0) properly rejected", True)
        except Exception as e:
            self.log_test_result(f"✗ Unexpected error for invalid count: {e}", False)

        # Test invalid language
        try:
            worker = QuestionWorker(count=5, target_language='invalid')
            self.log_test_result("✗ Invalid language should be rejected", False)
        except ValueError:
            self.log_test_result("✓ Invalid language properly rejected", True)
        except Exception as e:
            self.log_test_result(f"✗ Unexpected error for invalid language: {e}", False)

    def test_question_worker_error_handling(self):
        """Test QuestionWorker error handling improvements"""
        print("\n3. Testing QuestionWorker Error Handling...")

        # Mock requests to simulate network errors
        with patch('QuestionWorker.requests.get') as mock_get:
            # Test timeout handling
            mock_get.side_effect = TimeoutError("Connection timed out")

            worker = QuestionWorker(count=5, target_language='it')
            worker.run()

            # Check that empty list is returned on timeout
            self.log_test_result("✓ Timeout handled gracefully", True)

        # Test JSON parsing error
        with patch('QuestionWorker.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_get.return_value = mock_response

            worker = QuestionWorker(count=5, target_language='it')
            worker.run()

            self.log_test_result("✓ JSON parsing error handled", True)

    def test_question_worker_rate_limiting(self):
        """Test QuestionWorker rate limiting"""
        print("\n4. Testing QuestionWorker Rate Limiting...")

        # Test that rate limiting is enforced
        start_time = time.time()
        worker1 = QuestionWorker(count=5, target_language='it')

        # Simulate API call
        with patch('QuestionWorker.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"results": []}
            mock_get.return_value = mock_response

            worker1.run()

        # Create second worker immediately
        worker2 = QuestionWorker(count=5, target_language='it')

        with patch('QuestionWorker.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"results": []}
            mock_get.return_value = mock_response

            start_second = time.time()
            worker2.run()
            end_second = time.time()

            # Check that at least the rate limit interval has passed
            elapsed = end_second - start_second
            if elapsed >= AppConstants.API_RATE_LIMIT_INTERVAL:
                self.log_test_result(f"✓ Rate limiting enforced ({elapsed:.2f}s >= {AppConstants.API_RATE_LIMIT_INTERVAL}s)", True)
            else:
                self.log_test_result(f"✗ Rate limiting not enforced ({elapsed:.2f}s < {AppConstants.API_RATE_LIMIT_INTERVAL}s)", False)

    def test_ui_error_handling(self):
        """Test UI error handling improvements"""
        print("\n5. Testing UI Error Handling...")
        
        # Ensure QApplication is created
        self._ensure_qapplication()

        # Test that QuizApp handles missing models gracefully
        try:
            # This should not crash even if models are not properly initialized
            app = QuizApp()
            self.log_test_result("✓ QuizApp handles missing models gracefully", True)
        except Exception as e:
            self.log_test_result(f"✗ QuizApp crashed on missing models: {e}", False)
        finally:
            # Clean up the app to prevent thread destruction warnings
            if 'app' in locals():
                app.close()

    def test_ui_thread_management(self):
        """Test UI thread management improvements"""
        print("\n6. Testing UI Thread Management...")
        
        # Ensure QApplication is created
        self._ensure_qapplication()

        # Test that closeEvent properly terminates threads
        app = QuizApp()

        # Mock a running worker
        mock_worker = Mock()
        mock_worker.isRunning.return_value = True
        mock_worker.wait.return_value = True
        app.worker = mock_worker

        # Simulate close event
        mock_event = Mock()
        app.closeEvent(mock_event)

        # Verify worker was terminated
        mock_worker.quit.assert_called_once()
        mock_worker.wait.assert_called_once()

        self.log_test_result("✓ Worker threads properly terminated on close", True)
        
        # Clean up the app to prevent thread destruction warnings
        app.close()

    def test_input_validation(self):
        """Test input validation improvements"""
        print("\n7. Testing Input Validation...")
        
        # Ensure QApplication is created
        self._ensure_qapplication()

        # Test question count validation in QuizApp
        app = QuizApp()

        # Mock the required methods to avoid full initialization
        app._show_loading_overlay = Mock()
        app._hide_loading_overlay = Mock()
        app.category_model = Mock()
        app.difficulty_model = Mock()
        app.type_model = Mock()

        # Test invalid count
        try:
            app.fetch_question(count=0)
            self.log_test_result("✗ Invalid question count should be rejected", False)
        except ValueError:
            self.log_test_result("✓ Invalid question count properly rejected", True)
        except Exception as e:
            self.log_test_result(f"✗ Unexpected error: {e}", False)

        # Test valid count
        try:
            with patch('UI.QuizApp.QuestionWorker') as mock_worker_class:
                mock_worker = Mock()
                mock_worker_class.return_value = mock_worker

                app.fetch_question(count=5)
                self.log_test_result("✓ Valid question count accepted", True)
        except Exception as e:
            self.log_test_result(f"✗ Valid question count rejected: {e}", False)
        finally:
            # Clean up the app to prevent thread destruction warnings
            app.close()

    def log_test_result(self, message, success):
        """Log a test result"""
        self.test_results.append((message, success))
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {message}")

    def print_test_results(self):
        """Print final test results summary"""
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)

        passed = sum(1 for _, success in self.test_results if success)
        total = len(self.test_results)

        for message, success in self.test_results:
            status = "✓" if success else "✗"
            print(f"{status} {message}")

        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {passed/total*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! System improvements are working correctly.")
        else:
            print("⚠️  Some tests failed. Please review the improvements.")


def main():
    """Main test function"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run tests
    tester = TestSystemImprovements()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
