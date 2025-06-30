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


def read_mtf_vs_field(file_path):
    encoding, raw = detect_encoding(file_path)
    lines = raw.decode(encoding).splitlines()
    freq_pattern = re.compile(r'^Data for spatial frequency: ([\d\.]+) cycles per mm')
    data_pattern = re.compile(r'\s*([\d\.\-]+)\s+([\d\.\-]+)\s+([\d\.\-]+)')
    blocks = []
    current_freq = None
    current_data = []
    for line in lines:
        freq_match = freq_pattern.match(line)
        if freq_match:
            if current_freq is not None and current_data:
                blocks.append({
                    'freq': float(current_freq),
                    'data': np.array(current_data, dtype=float)
                })
                current_data = []
            current_freq = freq_match.group(1)
        elif current_freq is not None:
            data_match = data_pattern.match(line)
            if data_match:
                current_data.append([
                    float(data_match.group(1)),
                    float(data_match.group(2)),
                    float(data_match.group(3))
                ])
    if current_freq is not None and current_data:
        blocks.append({
            'freq': float(current_freq),
            'data': np.array(current_data, dtype=float)
        })
    return blocks


def plot_mtf_vs_field(blocks, file_name):
    #colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    
    #plt.style.use('dark_background')
    plt.figure(figsize=__config__.pic_size)
    for i, block in enumerate(blocks):
        data = block['data']
        rel_field = data[:, 0]
        tangential = data[:, 1]
        sagittal = data[:, 2]
        plt.plot(rel_field, tangential, color=__config__.colors[i+1], linestyle='-', label=f'T_{block["freq"]:.2f} lp/mm')
        plt.plot(rel_field, sagittal, color=__config__.colors[i+1], linestyle='--' , label=f'S_{block["freq"]:.2f} lp/mm')
    plt.xlabel('Relative Field', fontsize=__config__.xlabel_size)
    plt.ylabel('MTF', fontsize=__config__.ylabel_size)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title('MTF vs Field (Tangential & Sagittal)', fontsize=__config__.title_size)
    plt.legend(fontsize=__config__.legend_size)
    plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.xticks(fontsize=__config__.xticks_size)
    plt.yticks(fontsize=__config__.yticks_size)
    ax = plt.gca()
    ax.tick_params(width=2, length=8)
    for spine in ax.spines.values():
        spine.set_linewidth(2)
    plt.savefig(f'{file_name}.png', dpi=300)
    #plt.show()
    plt.close()


def main():
    file_path = '新煒/MTF vs Field.txt'
    file_name = '新煒/MTF vs Field'
    blocks = read_mtf_vs_field(file_path)
    plot_mtf_vs_field(blocks, file_name)


if __name__ == '__main__':
    main()