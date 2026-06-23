import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# 获取 exe 真实路径
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(os.path.abspath(sys.executable))
    CONFIG_FILE = os.path.join(APP_DIR, "config.json")
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(APP_DIR, "config.json")


def load_config():
    if os.path.exists(CONFIG_FILE):
        import json
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"username": "", "octane_target": ""}


def save_config(config):
    import json
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def safe_clean_folder(path, log_func):
    if not os.path.exists(path):
        log_func(f"  文件夹不存在，跳过：{path}")
        return
    count_file = count_dir = 0
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
                count_file += 1
            else:
                shutil.rmtree(item_path)
                count_dir += 1
        except Exception as e:
            log_func(f"  跳过（无权限）：{item} - {e}")
    log_func(f"  已删除 {count_file} 个文件，{count_dir} 个文件夹")


def safe_copy_folder(src, dst, log_func):
    if not os.path.exists(src):
        log_func(f"  源文件夹不存在：{src}")
        return False
    try:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        log_func(f"  复制完成：{src} → {dst}")
        return True
    except Exception as e:
        log_func(f"  复制失败：{e}")
        return False


# 颜色定义
BG = "#2d2d2d"
FG = "#e0e0e0"
FRAME_BG = "#3d3d3d"
ENTRY_BG = "#4d4d4d"
BTN_BG = "#0066cc"
BTN_HOVER = "#0088ff"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("OC插件 快速激活工具")
        self.root.geometry("480x520")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.config = load_config()
        self.setup_ui()

    def create_button(self, parent, text, command, bg=BTN_BG, fg="white"):
        btn = tk.Button(parent, text=text, command=command,
                        bg=bg, fg=fg, font=("Microsoft YaHei", 11, "bold"),
                        relief="flat", cursor="hand2", padx=10, pady=8)
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def create_label(self, parent, text, font=None):
        return tk.Label(parent, text=text, bg=FRAME_BG, fg=FG,
                        font=font or ("Microsoft YaHei", 10))

    def setup_ui(self):
        # 标题
        tk.Label(self.root, text="OC插件 快速激活工具",
                 font=("Microsoft YaHei", 15, "bold"),
                 bg=BG, fg="white", pady=(15, 10)).pack()

        # 配置区
        cfg = tk.LabelFrame(self.root, text=" 配置 ", bg=FRAME_BG, fg=FG,
                            font=("Microsoft YaHei", 10, "bold"),
                            padx=10, pady=10)
        cfg.pack(fill="x", padx=15, pady=(0, 10))

        # 用户名
        self.create_label(cfg, "用户名：").grid(row=0, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar(value=self.config.get("username", ""))
        self.username_entry = tk.Entry(cfg, textvariable=self.username_var,
                                        width=25, bg=ENTRY_BG, fg=FG,
                                        insertbackground=FG,
                                        relief="flat", bd=2)
        self.username_entry.grid(row=0, column=1, sticky="w", padx=(8, 0), pady=5)

        # octane 路径
        self.create_label(cfg, "octane 复制目标：").grid(row=1, column=0, sticky="w", pady=5)
        self.oct_var = tk.StringVar(value=self.config.get("octane_target", ""))
        self.oct_entry = tk.Entry(cfg, textvariable=self.oct_var,
                                   width=25, bg=ENTRY_BG, fg=FG,
                                   insertbackground=FG,
                                   relief="flat", bd=2)
        self.oct_entry.grid(row=1, column=1, sticky="w", padx=(8, 5), pady=5)

        sel_btn = tk.Button(cfg, text="选择", command=self.on_select_oct,
                            bg=FRAME_BG, fg=FG, relief="flat",
                            font=("Microsoft YaHei", 9))
        sel_btn.grid(row=1, column=2, pady=5)

        save_btn = tk.Button(cfg, text="保存配置", command=self.on_save_config,
                             bg=BTN_BG, fg="white", relief="flat",
                             font=("Microsoft YaHei", 10), padx=10)
        save_btn.grid(row=2, column=0, columnspan=3, pady=(10, 0))

        # 路径预览
        preview = tk.LabelFrame(self.root, text=" 路径预览 ", bg=FRAME_BG, fg=FG,
                                font=("Microsoft YaHei", 10, "bold"),
                                padx=8, pady=8)
        preview.pack(fill="x", padx=15, pady=(0, 10))

        self.preview_text = tk.Text(preview, height=4, wrap="word",
                                    font=("Consolas", 9),
                                    bg=BG, fg=FG, insertbackground=FG,
                                    relief="flat", bd=0)
        self.preview_text.pack(fill="x")
        self.refresh_preview()

        # 实时刷新
        self.username_entry.bind("<KeyRelease>", lambda e: self.refresh_preview())
        self.oct_entry.bind("<KeyRelease>", lambda e: self.refresh_preview())

        # 功能按钮
        btn_frame = tk.LabelFrame(self.root, text=" 功能操作 ", bg=FRAME_BG, fg=FG,
                                  font=("Microsoft YaHei", 10, "bold"),
                                  padx=15, pady=15)
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.create_button(btn_frame, "🗑  清空 OctaneRender 缓存",
                           self.on_clean_all, bg="#cc4444").pack(pady=5, fill="x")

        self.create_button(btn_frame, "📋  复制资源到目标路径",
                           self.on_copy_all).pack(pady=5, fill="x")

        # 日志区
        log_frame = tk.LabelFrame(self.root, text=" 操作日志 ", bg=FRAME_BG, fg=FG,
                                  font=("Microsoft YaHei", 10, "bold"),
                                  padx=8, pady=8)
        log_frame.pack(fill="both", expand=True, padx=15, pady=(0, 12))

        self.log_text = tk.Text(log_frame, height=6, wrap="word",
                                font=("Consolas", 9),
                                bg=BG, fg=FG, insertbackground=FG,
                                relief="flat", bd=0)
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # 底部信息
        tk.Label(self.root, text=f"程序目录：{APP_DIR}",
                 font=("Microsoft YaHei", 8),
                 bg=BG, fg="#888").pack(pady=(0, 5))

    def refresh_preview(self):
        username = self.username_var.get().strip()
        oct_target = self.oct_var.get().strip()

        lines = [
            ("清空 Local  ", f"C:\\Users\\{username}\\AppData\\Local\\OctaneRender"
             if username else "(请填写用户名)"),
            ("清空 Roaming", f"C:\\Users\\{username}\\AppData\\Roaming\\OctaneRender"
             if username else "(请填写用户名)"),
            ("复制 AppData", f"{os.path.join(APP_DIR, 'AppData')}  →  C:\\Users\\{username if username else '(请填写用户名)'}\\AppData"),
            ("复制 octane  ", f"{os.path.join(APP_DIR, 'octane')}  →  {oct_target if oct_target else '(请填写目标路径)'}"),
        ]
        text = "\n".join(f"{label}：{path}" for label, path in lines)
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", text)
        self.preview_text.config(state="disabled")

    def log(self, msg):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.root.update_idletasks()

    def get_username(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("错误", "请先填写用户名！")
            return None
        return username

    def on_save_config(self):
        self.config["username"] = self.username_var.get().strip()
        self.config["octane_target"] = self.oct_var.get().strip()
        save_config(self.config)
        messagebox.showinfo("成功", "配置已保存！")

    def on_select_oct(self):
        path = filedialog.askdirectory(title="选择 octane 复制目标文件夹")
        if path:
            self.oct_var.set(path)
            self.config["octane_target"] = path
            save_config(self.config)
            self.refresh_preview()

    def on_clean_all(self):
        username = self.get_username()
        if not username:
            return
        paths = [
            f"C:\\Users\\{username}\\AppData\\Local\\OctaneRender",
            f"C:\\Users\\{username}\\AppData\\Roaming\\OctaneRender",
        ]
        if not messagebox.askyesno(
                "确认清空",
                f"将清空以下两个目录的所有内容：\n\n{paths[0]}\n{paths[1]}\n\n此操作不可撤销！"):
            return
        for p in paths:
            self.log(f"[清理] {p}")
            safe_clean_folder(p, self.log)
        self.log("✅ 全部清理完成\n")
        messagebox.showinfo("完成", "OctaneRender 缓存已全部清空！")

    def on_copy_all(self):
        username = self.get_username()
        if not username:
            return
        oct_target = self.oct_var.get().strip()
        if not oct_target:
            messagebox.showerror("错误", "请先填写或选择 octane 复制目标路径！")
            return

        src_appdata = os.path.join(APP_DIR, "AppData")
        dst_appdata = f"C:\\Users\\{username}\\AppData"

        if not messagebox.askyesno("确认复制", f"将复制以下内容到目标路径：\n\n"
                                   f"AppData：{src_appdata}  →  {dst_appdata}\n"
                                   f"octane ：{os.path.join(APP_DIR, 'octane')}  →  {oct_target}\n\n"
                                   f"继续吗？"):
            return

        # 复制 AppData
        if os.path.exists(src_appdata):
            self.log(f"[复制 AppData] {src_appdata} → {dst_appdata}")
            try:
                if not os.path.exists(dst_appdata):
                    os.makedirs(dst_appdata, exist_ok=True)
                for item in os.listdir(src_appdata):
                    s = os.path.join(src_appdata, item)
                    d = os.path.join(dst_appdata, item)
                    if os.path.isfile(s):
                        shutil.copy2(s, d)
                        self.log(f"  已复制文件：{item}")
                    else:
                        if os.path.exists(d):
                            shutil.rmtree(d)
                        shutil.copytree(s, d)
                        self.log(f"  已复制文件夹：{item}")
                self.log("  ✅ AppData 复制完成")
            except Exception as e:
                self.log(f"  ❌ 失败：{e}")
        else:
            self.log(f"  ⚠ AppData 文件夹不存在，跳过")

        # 复制 octane
        src_oct = os.path.join(APP_DIR, "octane")
        dst_oct = os.path.join(oct_target, "octane")
        if os.path.exists(src_oct):
            self.log(f"[复制 octane] {src_oct} → {dst_oct}")
            safe_copy_folder(src_oct, dst_oct, self.log)
        else:
            self.log(f"  ⚠ octane 文件夹不存在，跳过")

        self.log("✅ 全部复制完成\n")
        messagebox.showinfo("完成", "资源复制完成！")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
