from PIL import Image
import os

def cur2png(cur_path: str, out_png: str = None):
    if out_png is None:
        out_png = os.path.splitext(cur_path)[0] + ".png"
    im = Image.open(cur_path)
    hot_x = im.info.get("hotspot_x", 0)
    hot_y = im.info.get("hotspot_y", 0)
    if hasattr(im, "n_frames") and im.n_frames > 1:
        im.seek(0)
    im.save(out_png, format="PNG")
    print(f"{cur_path} → {out_png}  热点({hot_x},{hot_y})")
    return out_png

if __name__ == "__main__":
    # 当前脚本所在目录
    work_dir = os.path.dirname(__file__)
    for fname in os.listdir(work_dir):
        if fname.lower().endswith(".cur"):
            cur_file = os.path.join(work_dir, fname)
            cur2png(cur_file)
    print("✅ 同目录全部cur转换完成")
