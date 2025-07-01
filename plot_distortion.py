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


def read_distortion_data(file_path):
    encoding, raw = detect_encoding(file_path)
    lines = raw.decode(encoding).splitlines()
    data_pattern = re.compile(r'\s*([\d\.\-]+)\s+([\d\.\-]+)\s+([\d\.\-]+)\s+([\d\.\-]+)\s+([\d\.\-]+)\s+([\d\.\-]+) ?%?')
    y_angle = []
    distortion = []
    for line in lines:
        match = data_pattern.match(line)
        if match:
            y_angle.append(float(match.group(1)))
            distortion.append(float(match.group(6)))
    return np.array(y_angle), np.array(distortion)


def plot_distortion(y_angle, distortion, file_name):
    plt.figure(figsize=__config__.distortion_pic_size)
    plt.plot(distortion, y_angle, color=__config__.colors[1], linewidth=2.5, label='Distortion')
    plt.ylabel('Y Angle (deg)', fontsize=__config__.ylabel_size)
    plt.xlabel('Distortion (%)', fontsize=__config__.xlabel_size)
    plt.title('Distortion vs Y Angle', fontsize=__config__.title_size)
    plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.xticks(fontsize=__config__.xticks_size)
    plt.yticks(fontsize=__config__.yticks_size)
    ax = plt.gca()
    ax.tick_params(width=2, length=8)
    for spine in ax.spines.values():
        spine.set_linewidth(2)
    plt.legend(fontsize=__config__.legend_size)
    plt.savefig(f'{file_name}.png', dpi=300)
    #plt.show()
    plt.close()


def main():
    file_path = '新煒/Distortion.txt'
    file_name = '新煒/distortion'
    y_angle, distortion = read_distortion_data(file_path)
    plot_distortion(y_angle, distortion, file_name)


if __name__ == '__main__':
    main() 