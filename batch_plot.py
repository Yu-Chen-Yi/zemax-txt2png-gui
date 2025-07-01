import os
import sys
import importlib
import datetime


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
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

INPUT_DIR = 'input_zemax_textfile_folder'
OUTPUT_ROOT = 'output_meta-rosetta_pngfile_folder'

def main():
    # 產生以當前時間命名的輸出資料夾
    now_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = os.path.join(OUTPUT_ROOT, now_str)
    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(INPUT_DIR):
        if not fname.endswith('.txt'):
            continue
        for key, (mod_name, read_func, plot_label) in PLOT_MAP.items():
            if fname.startswith(f'{plot_label}_'):
                label = fname[len(plot_label)+1:-4]  # 去除前綴與.txt
                file_path = os.path.join(INPUT_DIR, fname)
                mod = importlib.import_module(mod_name)
                read = getattr(mod, read_func)
                # 讀取資料
                data = read(file_path)
                # 決定繪圖函數與輸出檔名
                if key == 'Chief ray angle':
                    img_h, r1 = data
                    out_png = os.path.join(output_dir, f'CRA_{label}.png')
                    mod.plot_cra(img_h, r1, out_png[:-4])
                elif key == 'Distortion':
                    y_angle, distortion = data
                    out_png = os.path.join(output_dir, f'Dist_{label}.png')
                    mod.plot_distortion(y_angle, distortion, out_png[:-4])
                elif key == 'MTF vs Field':
                    out_png = os.path.join(output_dir, f'MvField_{label}.png')
                    mod.plot_mtf_vs_field(data, out_png[:-4])
                elif key == 'MTF vs Freq':
                    out_png = os.path.join(output_dir, f'MvFreq_{label}.png')
                    mod.plot_mtf(data, out_png[:-4])
                elif key == 'Through Focus':
                    out_png = os.path.join(output_dir, f'TF_{label}.png')
                    mod.plot_mtf(data, out_png[:-4])
                elif key == 'Relative Illumination':
                    y_field, rel_illum = data
                    out_png = os.path.join(output_dir, f'RI_{label}.png')
                    mod.plot_ri(y_field, rel_illum, out_png)
                print(f'已處理 {fname} -> {out_png}')
                break

if __name__ == '__main__':
    main()