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
                    # 直接複製原繪圖主體
                    import matplotlib.pyplot as plt
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
                    plt.savefig(out_png, dpi=300)
                    plt.close()
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