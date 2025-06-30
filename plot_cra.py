import matplotlib.pyplot as plt
import numpy as np
import chardet
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import __config__

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        return result['encoding'], raw

def read_cra_data(file_path):
    encoding, raw = detect_encoding(file_path)
    lines = raw.decode(encoding).splitlines()
    img_h = []
    r1 = []
    data_start = False
    for line in lines:
        # 找到表頭
        if 'ImgH' in line and 'R1' in line:
            data_start = True
            continue
        if data_start:
            # 結束於====或空行
            if line.strip().startswith('=') or not line.strip():
                break
            parts = line.split()
            if len(parts) >= 2:
                try:
                    img_h.append(float(parts[0]))
                    r1.append(float(parts[1]))
                except ValueError:
                    continue
    return np.array(img_h), np.array(r1)

if __name__ == '__main__':
    file_path = '新煒/CRA.txt'  # 可更換為其他txt路徑
    img_h, r1 = read_cra_data(file_path)
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
    plt.savefig('cra_plot.png', dpi=300)
    #plt.show()
    plt.close()
