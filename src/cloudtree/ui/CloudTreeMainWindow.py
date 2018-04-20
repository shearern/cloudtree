from PySide.QtCore import *
from PySide.QtGui import *

from ..catalog import CatalogScanner, CatalogModel

from .SbcCatalogMainWindow_UI import Ui_SbcCatalogMainWindow

class SbcCatalogMainWindow(QMainWindow, Ui_SbcCatalogMainWindow):

    def __init__(self):
        super(SbcCatalogMainWindow, self).__init__(parent=None)

        self.setupUi(self)

        self.catalog_scanner = CatalogScanner()
        self.catalog_scanner.activity.connect(self.catalog_scanner_activity_update)
        self.catalog_scanner_idle_countdown = None
        self.catalog_model = CatalogModel(self.catalog_scanner)
        self.catalog_table_view.setModel(self.catalog_model)

        self._initial_column_widths_set = False
        self.catalog_model.dataChanged.connect(self._set_initial_recording_table_widths)

        self.search_box.textChanged.connect(self.catalog_model.set_search_term)

        # Startup Tasks
        QTimer.singleShot(0, self.start_worker_threads)

        # Timer to do a pulse extend on activity icons
        self.activity_idle_countdown_timer = QTimer()
        self.connect(self.activity_idle_countdown_timer, SIGNAL("timeout()"), self.activity_idle_countdown)
        self.activity_idle_countdown_timer.start(0.1 * 1000)    # 1000 msec = 1 second


    def start_worker_threads(self):
        self.catalog_scanner.start_worker_thread()


    def _set_initial_recording_table_widths(self, topLeft, bottomRight):
        if not self._initial_column_widths_set:
            self.catalog_table_view.resizeColumnsToContents()
            self._initial_column_widths_set = True


    def catalog_scanner_activity_update(self, status):
        if status == 'idle':
            self.catalog_scanner_idle_countdown = 0.75
        elif status == 'checking':
            self.catalog_scanner_idle_countdown = None
            self.catalog_scanner_activity_icon.setPixmap(QPixmap(":/status_ind/assets/compiled/catalog_scanner_checking.png"))
        elif status == 'working':
            self.catalog_scanner_idle_countdown = None
            self.catalog_scanner_activity_icon.setPixmap(QPixmap(":/status_ind/assets/compiled/catalog_scanner_working.png"))
        else:
            self.catalog_scanner_idle_countdown = None
            self.catalog_scanner_activity_icon.setPixmap(QPixmap(":/status_ind/assets/compiled/catalog_scanner_error.png"))
            # TODO: Add error message to tooltip?


    def activity_idle_countdown(self):
        '''Maintain activity timeout timers

        This acts as a basic pulse extender for activity indicators so that the status icons
        are visible for a short time before going back to idle.
        '''
        timer_freq = 0.1
        if self.catalog_scanner_idle_countdown is not None:
            self.catalog_scanner_idle_countdown -= timer_freq
            if self.catalog_scanner_idle_countdown <= 0:
                self.catalog_scanner_activity_icon.setPixmap(QPixmap(":/status_ind/assets/compiled/catalog_scanner_icon.png"))
                self.catalog_scanner_idle_countdown = None
