# main.py
from .ClassWidgets.base import PluginBase, SettingsBase
import psutil

WIDGET_CODE = 'cpu-monitor.ui'
WIDGET_NAME = 'CPU监测'
WIDGET_WIDTH = 120

class Plugin(PluginBase):
    def __init__(self, cw_contexts, method):
        super().__init__(cw_contexts, method)
        self.method.register_widget(WIDGET_CODE, WIDGET_NAME, WIDGET_WIDTH)
        self.widget_instance = None

    def execute(self):
        self.widget_instance = self.method.get_widget(WIDGET_CODE)
        
    def update(self, cw_contexts):
        super().update(cw_contexts)
 
        cpu_percent = psutil.cpu_percent()

        self.method.change_widget_content(
            WIDGET_CODE,
            title=f"CPU\n{cpu_percent}%",
            content=""
        )

class Settings(SettingsBase):
    def __init__(self, plugin_path, parent=None):
        super().__init__(plugin_path, parent)
