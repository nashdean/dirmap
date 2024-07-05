import pytest
from unittest.mock import patch, MagicMock
import sys
from dirmapper.main import main

def test_main(monkeypatch):
    """
    Test the main function with valid arguments.

    This test simulates command-line arguments and patches the external dependencies to verify that the main function
    behaves correctly without invoking actual functionality. It checks that the DirectoryStructureGenerator is called
    with the expected arguments, the generate method is called, and the success message is logged without any exceptions.
    """

    # Simulate command-line arguments
    test_args = [
        "main.py",
        "test_root_directory",
        "test_output_file",
        "--ignore_file", ".test-ignore",
        "--no_gitignore",
        "--sort", "asc",
        "--style", "tree",
        "--format", "plain",
        "--ignore", "test_ignore_pattern"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Patch the external dependencies
    with patch('dirmapper.main.read_ignore_patterns', return_value=['ignore_pattern']):
        with patch('dirmapper.main.PathIgnorer') as mock_path_ignorer:
            with patch('dirmapper.main.STYLE_MAP', {'tree': MagicMock(return_value=MagicMock())}):
                with patch('dirmapper.main.FORMATTER_MAP', {'plain': MagicMock(return_value=MagicMock())}):
                    with patch('dirmapper.main.parse_sort_argument', return_value=('asc', False)):
                        with patch('dirmapper.main.DirectoryStructureGenerator') as mock_generator:
                            mock_instance = MagicMock()
                            mock_generator.return_value = mock_instance
                            with patch('dirmapper.main.logger.info') as mock_logger_info:
                                with patch('dirmapper.main.log_exception') as mock_log_exception:
                                    with patch('dirmapper.main.get_package_version', return_value="1.0.0"):
                                        # Call the main function
                                        main()

                                        # Assert that DirectoryStructureGenerator was called with the correct arguments
                                        mock_generator.assert_called_once_with(
                                            'test_root_directory',
                                            'test_output_file',
                                            mock_path_ignorer.return_value,
                                            sorting_strategy=mock_generator.call_args[1]['sorting_strategy'],
                                            case_sensitive=False,
                                            style=mock_generator.call_args[1]['style'],
                                            formatter=mock_generator.call_args[1]['formatter']
                                        )
                                        # Assert that generate method was called
                                        mock_instance.generate.assert_called_once()
                                        # Assert that logger.info was called
                                        mock_logger_info.assert_called_once_with("Directory structure saved to test_output_file")
                                        # Assert that no exceptions were logged
                                        mock_log_exception.assert_not_called()

def test_main_with_exception(monkeypatch):
    """
    Test the main function to ensure it handles exceptions correctly.

    This test simulates minimal command-line arguments and patches the external dependencies to raise an exception.
    It verifies that the exception is logged correctly using the log_exception function.
    """
    
    # Simulate command-line arguments
    test_args = [
        "main.py",
        "test_root_directory",
        "test_output_file"
    ]
    monkeypatch.setattr(sys, 'argv', test_args)

    # Patch the external dependencies to raise an exception
    with patch('dirmapper.main.read_ignore_patterns', side_effect=Exception("Test exception")):
        with patch('dirmapper.main.log_exception') as mock_log_exception:
            with patch('dirmapper.main.get_package_version', return_value="1.0.0"):
                # Call the main function
                main()

                # Assert that log_exception was called with the correct exception
                mock_log_exception.assert_called_once()
                assert mock_log_exception.call_args[0][0].args[0] == "Test exception"