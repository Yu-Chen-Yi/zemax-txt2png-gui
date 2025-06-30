import numpy as np
import matplotlib.pyplot as plt
import re
import chardet
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import __config__   

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        return result['encoding'], raw


def read_ri_data(file_path):
    encoding, raw = detect_encoding(file_path)
    lines = raw.decode(encoding).splitlines()
    data_pattern = re.compile(r'\s*([\d\.\-]+)\s+([\d\.\-]+)')
    y_field = []
    rel_illum = []
    data_start = False
    for line in lines:
        # 找到資料表頭後才開始抓資料
        if 'Y Field' in line and 'Rel. Ill' in line:
            data_start = True
            continue
        if data_start:
            match = data_pattern.match(line)
            if match and len(match.groups()) >= 2:
                try:
                    y_field.append(float(match.group(1)))
                    rel_illum.append(float(match.group(2)))
                except ValueError:
                    continue
    return np.array(y_field), np.array(rel_illum)


def plot_ri(y_field, rel_illum, file_name):
    plt.figure(figsize=__config__.pic_size)
    plt.plot(y_field, rel_illum, color=__config__.colors[1], linewidth=2.5, marker='o', label='Relative Illumination')
    plt.xlabel('Y Field (mm)', fontsize=__config__.xlabel_size)
    plt.ylabel('Relative Illumination', fontsize=__config__.ylabel_size)
    plt.title('Relative Illumination vs Y Field', fontsize=__config__.title_size)
    plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.xticks(fontsize=__config__.xticks_size)
    plt.yticks(fontsize=__config__.yticks_size)
    ax = plt.gca()
    ax.tick_params(width=2, length=8)
    for spine in ax.spines.values():
        spine.set_linewidth(2)
    plt.legend(fontsize=__config__.legend_size)
    plt.savefig(file_name, dpi=300)
    #plt.show()
    plt.close()


def main():
    file_path = '新煒/RI.txt'
    file_name = '新煒/RI'
    y_field, rel_illum = read_ri_data(file_path)
    plot_ri(y_field, rel_illum, file_name)


if __name__ == '__main__':
    main() 