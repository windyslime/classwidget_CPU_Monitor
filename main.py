from .ClassWidgets.base import PluginBase, SettingsBase
import psutil
import os
import json
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox

WIDGET_CODE = 'cpu-multi-core-monitor.ui'
WIDGET_NAME = '多核CPU监测'
WIDGET_WIDTH = 250

class Plugin(PluginBase):
    def __init__(self, cw_contexts, method):
        super().__init__(cw_contexts, method)
        self.method.register_widget(WIDGET_CODE, WIDGET_NAME, WIDGET_WIDTH)
        self.core_count = psutil.cpu_count(logical=False)
        self.logical_cores = psutil.cpu_count()
        self.config_path = os.path.join(cw_contexts['PLUGIN_PATH'], 'config.json')

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {"core_mode": "logical"}

    def format_display(self, per_cpu, mode):
        """根据模式生成显示内容"""
        display_text = "CPU\n"
        config = self.load_config()
        
        if config.get("core_mode") == "physical":

            display_text += f"物理核心: {self.core_count}\n"
            display_text += f"总使用率: {sum(per_cpu)/len(per_cpu):.1f}%"
        else:
  
            for i, percent in enumerate(per_cpu, 1):
                display_text += f"C{i}: {percent}%\n"
            display_text += f"逻辑核心: {self.logical_cores}\n"
            display_text += f"总使用率: {psutil.cpu_percent()}%"
        return display_text

    def update(self, cw_contexts):
        super().update(cw_contexts)
        per_cpu = psutil.cpu_percent(interval=0.5, percpu=True)
        config = self.load_config()
        
        self.method.change_widget_content(
            WIDGET_CODE,
            title=self.format_display(per_cpu, config.get("core_mode")),
            content=""
        )

class Settings(SettingsBase):
    def __init__(self, plugin_path, parent=None):
        super().__init__(plugin_path, parent)
        self.plugin_path = plugin_path
        self.config = self.load_config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        

        layout.addWidget(QLabel("核心显示模式："))
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("逻辑核心", "logical")
        self.mode_combo.addItem("物理核心", "physical")
        current_mode = self.config.get("core_mode", "logical")
        index = self.mode_combo.findData(current_mode)
        self.mode_combo.setCurrentIndex(index)
        layout.addWidget(self.mode_combo)
        

        layout.addWidget(QLabel("\n物理核心模式显示总使用率\n逻辑核心模式显示每个核心详情"))

    def load_config(self):
        config_path = os.path.join(self.plugin_path, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {"core_mode": "logical"}

    def save_settings(self):
        config = {
            "core_mode": self.mode_combo.currentData()
        }
        with open(os.path.join(self.plugin_path, 'config.json'), 'w') as f:
            json.dump(config, f)

# __init__.py 保持不变
