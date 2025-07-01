import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QComboBox, QLineEdit, QTabWidget, QMessageBox
)
from PySide6.QtCore import Qt
import importlib
import traceback
import matplotlib.pyplot as plt
import __config__
# 各類型對應的繪圖模組與函數
PLOT_MAP = {
    'Chief ray angle':   ('plot_cra',      'read_cra_data',         'CRA'),
    'Distortion':  ('plot_distortion','read_distortion_data',  'Dist'),
    'MTF vs Field': ('plot_mtf_vs_field', 'read_mtf_vs_field', 'MvField'),
    'MTF vs Freq':  ('plot_mtf_vs_lp',    'read_mtf_data',     'MvFreq'),
    'Through Focus':      ('plot_through_focus','read_mtf_data',     'TF'),
    'Relative Illumination':      ('plot_RI',          'read_ri_data',      'RI'),
}

class SingleFileTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        # 選擇類型
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel('選擇資料類型:'))
        self.type_combo = QComboBox()
        self.type_combo.addItems(list(PLOT_MAP.keys()))
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        # 選擇 txt 檔
        file_layout = QHBoxLayout()
        self.txt_path = QLineEdit()
        self.txt_path.setPlaceholderText('請選擇 txt 檔')
        file_btn = QPushButton('選擇檔案')
        file_btn.clicked.connect(self.select_txt)
        file_layout.addWidget(self.txt_path)
        file_layout.addWidget(file_btn)
        layout.addLayout(file_layout)
        # 選擇輸出 png
        out_layout = QHBoxLayout()
        self.png_path = QLineEdit()
        self.png_path.setPlaceholderText('請選擇輸出 png 路徑')
        out_btn = QPushButton('選擇位置')
        out_btn.clicked.connect(self.select_png)
        out_layout.addWidget(self.png_path)
        out_layout.addWidget(out_btn)
        layout.addLayout(out_layout)
        # 轉換按鈕
        self.run_btn = QPushButton('轉換')
        self.run_btn.clicked.connect(self.run_single)
        layout.addWidget(self.run_btn)
        # 狀態顯示
        self.status = QLabel('')
        layout.addWidget(self.status)
        self.setLayout(layout)

    def select_txt(self):
        path, _ = QFileDialog.getOpenFileName(self, '選擇 txt 檔', '', 'Text Files (*.txt)')
        if path:
            self.txt_path.setText(path)
            # 自動預設 png 路徑
            base = os.path.splitext(path)[0]
            self.png_path.setText(base + '.png')

    def select_png(self):
        path, _ = QFileDialog.getSaveFileName(self, '選擇輸出 png', '', 'PNG Files (*.png)')
        if path:
            if not path.lower().endswith('.png'):
                path += '.png'
            self.png_path.setText(path)

    def run_single(self):
        key = self.type_combo.currentText()
        txt_path = self.txt_path.text().strip()
        png_path = self.png_path.text().strip()
        if not (os.path.isfile(txt_path) and png_path):
            self.status.setText('請正確選擇 txt 檔與輸出 png 路徑')
            QMessageBox.warning(self, '錯誤', '請正確選擇 txt 檔與輸出 png 路徑')
            return
        mod_name, read_func, _ = PLOT_MAP[key]
        try:
            mod = importlib.import_module(mod_name)
            read = getattr(mod, read_func)
            data = read(txt_path)
            # 根據類型呼叫繪圖
            if key == 'Chief ray angle':
                img_h, r1 = data
                mod.plot_cra(img_h, r1, png_path[:-4])
                self.status.setText('轉換成功！')
                QMessageBox.information(self, '完成', f'已輸出：{png_path}')
            elif key == 'Distortion':
                y_angle, distortion = data
                mod.plot_distortion(y_angle, distortion, png_path[:-4])
                self.status.setText('轉換成功！')
                QMessageBox.information(self, '完成', f'已輸出：{png_path}')
            elif key == 'MTF vs Field':
                mod.plot_mtf_vs_field(data, png_path[:-4])
                self.status.setText('轉換成功！')
                QMessageBox.information(self, '完成', f'已輸出：{png_path}')
            elif key == 'MTF vs Freq':
                mod.plot_mtf(data, png_path[:-4])
                self.status.setText('轉換成功！')
                QMessageBox.information(self, '完成', f'已輸出：{png_path}')
            elif key == 'Through Focus':
                mod.plot_mtf(data, png_path[:-4])
                QMessageBox.information(self, '完成', f'已輸出：{png_path}')
            elif key == 'Relative Illumination':
                y_field, rel_illum = data
                mod.plot_ri(y_field, rel_illum, png_path)
                self.status.setText('轉換成功！')
                QMessageBox.information(self, '完成', f'已輸出：{png_path}')
            else:
                QMessageBox.warning(self, '錯誤', '請選擇正確的資料類型')
                self.status.setText('請選擇正確的資料類型')
        except Exception as e:
            self.status.setText('轉換失敗：' + str(e))
            QMessageBox.critical(self, '失敗', f'轉換失敗：{e}')
            print(traceback.format_exc())

class BatchTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        # 選擇資料夾
        in_layout = QHBoxLayout()
        self.in_dir = QLineEdit()
        self.in_dir.setPlaceholderText('請選擇輸入資料夾')
        in_btn = QPushButton('選擇資料夾')
        in_btn.clicked.connect(self.select_in_dir)
        in_layout.addWidget(self.in_dir)
        in_layout.addWidget(in_btn)
        layout.addLayout(in_layout)
        # 選擇輸出資料夾
        out_layout = QHBoxLayout()
        self.out_dir = QLineEdit()
        self.out_dir.setPlaceholderText('請選擇輸出資料夾')
        out_btn = QPushButton('選擇資料夾')
        out_btn.clicked.connect(self.select_out_dir)
        out_layout.addWidget(self.out_dir)
        out_layout.addWidget(out_btn)
        layout.addLayout(out_layout)
        # 批次轉換按鈕
        self.run_btn = QPushButton('批次轉換')
        self.run_btn.clicked.connect(self.run_batch)
        layout.addWidget(self.run_btn)
        # 狀態顯示
        self.status = QLabel('')
        layout.addWidget(self.status)
        self.setLayout(layout)

    def select_in_dir(self):
        path = QFileDialog.getExistingDirectory(self, '選擇輸入資料夾')
        if path:
            self.in_dir.setText(path)

    def select_out_dir(self):
        path = QFileDialog.getExistingDirectory(self, '選擇輸出資料夾')
        if path:
            self.out_dir.setText(path)

    def run_batch(self):
        in_dir = self.in_dir.text().strip()
        out_dir = self.out_dir.text().strip()
        if not (os.path.isdir(in_dir) and os.path.isdir(out_dir)):
            self.status.setText('請正確選擇輸入與輸出資料夾')
            return
        count = 0
        for fname in os.listdir(in_dir):
            if not fname.endswith('.txt'):
                continue
            for key, (mod_name, read_func, plot_label) in PLOT_MAP.items():
                if fname.startswith(f'{plot_label}_'):
                    label = fname[len(plot_label)+1:-4]
                    file_path = os.path.join(in_dir, fname)
                    mod = importlib.import_module(mod_name)
                    read = getattr(mod, read_func)
                    try:
                        data = read(file_path)
                        if key == 'Chief ray angle':
                            img_h, r1 = data
                            plt.figure(figsize=__config__.pic_size)
                            plt.plot(img_h, r1, 'bo-', linewidth=2, markersize=6, label='R1')
                            plt.xlabel('Image Height (mm)', fontsize=__config__.xlabel_size)
                            plt.ylabel('Chief ray angle (deg)', fontsize=__config__.ylabel_size)
                            plt.title('Image Height vs CRA', fontsize=__config__.title_size, fontweight='bold')
                            plt.grid(True, linestyle='--', alpha=0.7)
                            plt.legend(fontsize=__config__.legend_size)
                            plt.xticks(fontsize=__config__.xticks_size)
                            plt.yticks(fontsize=__config__.yticks_size)
                            ax = plt.gca()
                            ax.tick_params(width=2, length=8)
                            for spine in ax.spines.values():
                                spine.set_linewidth(2)
                            plt.tight_layout()
                            out_png = os.path.join(out_dir, f'CRA_{label}.png')
                            plt.savefig(out_png, dpi=300)
                            plt.close()
                        elif key == 'Distortion':
                            y_angle, distortion = data
                            out_png = os.path.join(out_dir, f'Dist_{label}.png')
                            mod.plot_distortion(y_angle, distortion, out_png[:-4])
                        elif key == 'MTF vs Field':
                            out_png = os.path.join(out_dir, f'MvField_{label}.png')
                            mod.plot_mtf_vs_field(data, out_png[:-4])
                        elif key == 'MTF vs Freq':
                            out_png = os.path.join(out_dir, f'MvFreq_{label}.png')
                            mod.plot_mtf(data, out_png[:-4])
                        elif key == 'Through Focus':
                            out_png = os.path.join(out_dir, f'TF_{label}.png')
                            mod.plot_mtf(data, out_png[:-4])
                        elif key == 'Relative Illumination':
                            y_field, rel_illum = data
                            out_png = os.path.join(out_dir, f'RI_{label}.png')
                            mod.plot_ri(y_field, rel_illum, out_png)
                        else:
                            self.status.setText('請選擇正確的資料類型')
                        count += 1
                    except Exception as e:
                        print(f'{fname} 轉換失敗: {e}')
                        print(traceback.format_exc())
                    break
        self.status.setText(f'批次轉換完成，共處理 {count} 個檔案')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Zemax txt 轉 png 批次工具')
        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.addTab(SingleFileTab(), '單檔轉換')
        tabs.addTab(BatchTab(), '批次轉換')
        layout.addWidget(tabs)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(600, 300)
    win.show()
    sys.exit(app.exec()) 