"""Basic GUI tests."""
import unittest


class TestGUI(unittest.TestCase):
    """Test GUI components."""
    
    def test_import_app(self):
        """Test that we can import the main app."""
        from gui.app import PicXApp
        self.assertIsNotNone(PicXApp)
        
    def test_import_tabs(self):
        """Test that we can import tabs."""
        from gui.tabs.single_image import SingleImageTab
        self.assertIsNotNone(SingleImageTab)
        
    def test_import_widgets(self):
        """Test that we can import widgets."""
        from gui.widgets.file_selector import FileSelector
        from gui.widgets.drop_zone import DropZone
        from gui.widgets.progress_item import ProgressItem
        self.assertIsNotNone(FileSelector)
        self.assertIsNotNone(DropZone)
        self.assertIsNotNone(ProgressItem)
        
    def test_import_utils(self):
        """Test that we can import utilities."""
        from gui.utils.validators import validate_quality, validate_dimensions
        self.assertIsNotNone(validate_quality)
        self.assertIsNotNone(validate_dimensions)


if __name__ == "__main__":
    unittest.main()
