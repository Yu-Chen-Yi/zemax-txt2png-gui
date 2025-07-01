import numpy as np
import matplotlib.pyplot as plt
import re
import chardet
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import __config__

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw = f.read()
        result = chardet.detect(raw)
        return result['encoding'], raw


def read_mtf_data(file_path):
    encoding, raw = detect_encoding(file_path)
    lines = raw.decode(encoding).splitlines()
    field_pattern_y = re.compile(r'^Field: (([\d\.]+) mm|Diffraction limit)')
    field_pattern_r = re.compile(r'^Field: (([\d\.]+), ([\d\.]+) mm|Diffraction limit)')
    data_pattern = re.compile(r'\s*([\-\d\.]+)\s+([\d\.]+)\s+([\d\.]+)')
    fields = []
    current_field = None
    current_data = []
    for line in lines:
        field_match = field_pattern_y.match(line)
        if field_match is None:
            field_match = field_pattern_r.match(line)
            xy_field = True
        else:
            xy_field = False
        if field_match:
            if not xy_field:
                if current_field is not None:
                    fields.append({
                        'field': current_field,
                        'data': np.array(current_data, dtype=float)
                    })
                    current_data = []
                if field_match.group(2) is not None:
                    current_field = float(field_match.group(2))
                else:
                    current_field = 'Diffraction limit'
            else:
                if current_field is not None:
                    fields.append({
                        'field': current_field,
                        'data': np.array(current_data, dtype=float)
                    })
                    current_data = []
                if field_match.group(2) is not None:
                    current_field = (float(field_match.group(2)), float(field_match.group(3)))
                else:
                    current_field = 'Diffraction limit'
        elif current_field is not None:
            data_match = data_pattern.match(line)
            if data_match:
                current_data.append([
                    float(data_match.group(1)),
                    float(data_match.group(2)),
                    float(data_match.group(3))
                ])
    if current_field is not None and current_data:
        fields.append({
            'field': current_field,
            'data': np.array(current_data, dtype=float)
        })
    return fields


def plot_mtf(fields, file_name):
    plt.figure(figsize=(8, 6))
    for i, field in enumerate(fields):
        data = field['data']
        focal_shift = data[:, 0]
        tangential = data[:, 1]
        sagittal = data[:, 2]
        if field['field'] == 'Diffraction limit':
            plt.plot(focal_shift, tangential, 
                     color=__config__.colors[i], 
                     linestyle='-', 
                     label=f'Diff. limit')
        else:
            if isinstance(field['field'], tuple):
                plt.plot(focal_shift, tangential, 
                        color=__config__.colors[i], 
                        linestyle='-', 
                        label=f'T_{field["field"][0]:.3f}, {field["field"][1]:.3f} mm')
                plt.plot(focal_shift, sagittal, 
                        color=__config__.colors[i], 
                        linestyle='--', 
                        label=f'S_{field["field"][0]:.3f}, {field["field"][1]:.3f} mm')
            else:
                plt.plot(focal_shift, tangential, 
                        color=__config__.colors[i], 
                        linestyle='-', 
                        label=f'T_{field["field"]:.3f} mm')
                plt.plot(focal_shift, sagittal, 
                        color=__config__.colors[i], 
                        linestyle='--', 
                        label=f'S_{field["field"]:.3f} mm')
    plt.xlabel('Cycles per mm (lp/mm)', fontsize=__config__.xlabel_size)
    plt.ylabel('MTF', fontsize=__config__.ylabel_size)
    plt.xlim(np.min(focal_shift), np.max(focal_shift))
    plt.ylim(0, 1)
    plt.title('MTF vs lp/mm (Tangential & Sagittal)', fontsize=__config__.title_size)
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
    # file_folder = 'mtf_vs_lp'
    # for file in os.listdir(file_folder):
    #     if not file.endswith('.txt'):
    #         continue
    #     file_path = os.path.join(file_folder, file)
    #     fields = read_mtf_data(file_path)
    #     # 存檔檔名去掉.txt
    #     save_name = os.path.splitext(file)[0]
    #     plot_mtf(fields=fields, file_name=save_name)
    #     plt.close()
    file_path = '新煒/MTF vs Frequency.txt'
    filename = '新煒/MTF vs Frequency'
    fields = read_mtf_data(file_path)
    plot_mtf(fields=fields, file_name=filename)
    plt.close()

if __name__ == '__main__':
    main()