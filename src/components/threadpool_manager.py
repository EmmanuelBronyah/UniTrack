import os
from PySide6.QtCore import QThreadPool

global_threadpool = QThreadPool.globalInstance()

global_threadpool.setMaxThreadCount(os.cpu_count())
