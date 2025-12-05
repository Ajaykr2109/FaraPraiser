"""Main entry point for FaraPraiser application."""

import sys
from PyQt6.QtWidgets import QApplication
from farapraiser.ui.main_window import MainWindow


def main():
    """Start the FaraPraiser application."""
    app = QApplication(sys.argv)
    app.setApplicationName("FaraPraiser")
    app.setOrganizationName("FaraPraiser")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
