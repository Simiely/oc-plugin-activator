import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# ── 路径 ──
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(os.path.abspath(sys.executable))
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
        log_func(f"  ⚠ 不存在：{path}")
        return
    c1 = c2 = 0
    for item in os.listdir(path):
        p = os.path.join(path, item)
        try:
            if os.path.isfile(p) or os.path.islink(p):
                os.remove(p)
                c1 += 1
            else:
                shutil.rmtree(p)
                c2 += 1
        except Exception as e:
            log_func(f"  ⚠ 跳过：{item} - {e}")
    log_func(f"  已删除 {c1} 个文件、{c2} 个文件夹")


def safe_copy_folder(src, dst, log_func):
    if not os.path.exists(src):
        log_func(f"  ⚠ 源文件夹不存在：{src}")
        return False
    try:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        log_func(f"  ✅ 复制完成")
        return True
    except Exception as e:
        log_func(f"  ❌ {e}")
        return False


def set_dark_titlebar(root):
    """Windows 10/11 深色标题栏"""
    try:
        from ctypes import windll, c_int, byref
        HWND = windll.user32.GetParent(root.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 20, byref(c_int(2)), c_int(4))
    except Exception:
        pass  # 非 Windows 或旧版本忽略


# ── 颜色 ──
BG = "#1e1e1e"
FG = "#d4d4d4"
CARD = "#2d2d2d"
INPUT = "#3c3c3c"
BLUE = "#0078d4"
RED = "#c42b1c"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("OC插件 快速激活工具")
        self.root.geometry("520x560")
        self.root.minsize(460, 480)
        self.root.configure(bg=BG)

        self.config = load_config()
        set_dark_titlebar(root)
        self.build_ui()

    # ── 工具方法 ──
    def lbl(self, parent, text, fg=FG, bg=None, font=None, side=None):
        w = tk.Label(parent, text=text, bg=bg or BG, fg=fg,
                     font=font or ("Microsoft YaHei", 10))
        if side:
            w.pack(side=side)
        return w

    def btn(self, parent, text, cmd, bg=BLUE, fg="white"):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=bg, fg=fg, activebackground="#555", activeforeground=fg,
                      font=("Microsoft YaHei", 11, "bold"),
                      relief="flat", cursor="hand2")
        b.bind("<Enter>", lambda e: b.config(bg="#555"))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        return b

    def log(self, msg):
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.root.update_idletasks()

    def get_user(self):
        u = self.u_var.get().strip()
        if not u:
            messagebox.showerror("错误", "请先填写用户名！")
            return None
        return u

    # ── 构建界面 ──
    def build_ui(self):
        # 让 root 网格可扩展
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        row = 0

        # ── 标题 ──
        self.lbl(self.root, "OC插件 快速激活工具",
                 fg="white", font=("Microsoft YaHei", 15, "bold")
                 ).grid(row=row, column=0, pady=(18, 0)); row += 1

        # ── 配置卡片 ──
        c1 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c1.grid(row=row, column=0, padx=16, pady=12, sticky="ew"); row += 1
        self.lbl(c1, "配置", fg="white", font=("Microsoft YaHei", 10, "bold")
                 ).pack(pady=(8, 0))

        # 用户名行
        r1 = tk.Frame(c1, bg=CARD)
        r1.pack(fill="x", padx=12, pady=(8, 4))
        self.lbl(r1, "用户名：", bg=CARD, side="left")
        self.u_var = tk.StringVar(value=self.config.get("username", ""))
        ue = tk.Entry(r1, textvariable=self.u_var, width=24,
                      bg=INPUT, fg=FG, insertbackground=FG,
                      relief="flat", bd=2)
        ue.pack(side="left", padx=8)
        ue.bind("<KeyRelease>", lambda e: self.refresh())

        # octane 目标行
        r2 = tk.Frame(c1, bg=CARD)
        r2.pack(fill="x", padx=12, pady=(4, 4))
        self.lbl(r2, "octane 目标：", bg=CARD, side="left")
        self.o_var = tk.StringVar(value=self.config.get("octane_target", ""))
        oe = tk.Entry(r2, textvariable=self.o_var, width=18,
                      bg=INPUT, fg=FG, insertbackground=FG,
                      relief="flat", bd=2)
        oe.pack(side="left", padx=8)
        oe.bind("<KeyRelease>", lambda e: self.refresh())
        tk.Button(r2, text="浏览", command=self.pick_oct,
                  bg="#555", fg="white", relief="flat",
                  font=("Microsoft YaHei", 9), padx=6, pady=1).pack(side="left")

        # 保存按钮
        btn_save = tk.Button(c1, text="保存配置", command=self.save_cfg,
                             bg=BLUE, fg="white", relief="flat",
                             font=("Microsoft YaHei", 10), padx=12, pady=2)
        btn_save.pack(pady=(4, 8))

        # ── 路径预览 ──
        c2 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c2.grid(row=row, column=0, padx=16, pady=(0, 10), sticky="ew"); row += 1
        self.lbl(c2, "路径预览", fg="white",
                 font=("Microsoft YaHei", 10, "bold")).pack(pady=(6, 0))
        self.pv = tk.Text(c2, height=4, wrap="word",
                          font=("Consolas", 9),
                          bg=BG, fg=FG, insertbackground=FG,
                          relief="flat", bd=0)
        self.pv.pack(fill="x", padx=8, pady=(4, 8))
        self.refresh()

        # ── 功能按钮 ──
        c3 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c3.grid(row=row, column=0, padx=16, pady=(0, 10), sticky="ew"); row += 1
        self.lbl(c3, "功能操作", fg="white",
                 font=("Microsoft YaHei", 10, "bold")).pack(pady=(6, 0))

        inner = tk.Frame(c3, bg=CARD)
        inner.pack(padx=12, pady=8, fill="x")
        self.btn(inner, "🗑  清空 OctaneRender 缓存",
                 self.do_clean, bg=RED).pack(pady=4, fill="x")
        self.btn(inner, "📋  复制资源到目标路径",
                 self.do_copy).pack(pady=4, fill="x")

        # ── 日志区（可伸缩） ──
        c4 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c4.grid(row=row, column=0, padx=16, pady=(0, 10), sticky="nsew")
        c4.grid_rowconfigure(2, weight=1)
        c4.grid_columnconfigure(0, weight=1)
        row += 1

        self.lbl(c4, "操作日志", fg="white",
                 font=("Microsoft YaHei", 10, "bold")
                 ).grid(row=0, column=0, pady=(6, 0))

        lf = tk.Frame(c4, bg=BG, bd=1, relief="sunken")
        lf.grid(row=1, column=0, padx=8, pady=(4, 8), sticky="nsew")
        lf.grid_rowconfigure(0, weight=1)
        lf.grid_columnconfigure(0, weight=1)

        self.log_box = tk.Text(lf, wrap="word",
                               font=("Consolas", 9),
                               bg=BG, fg=FG, insertbackground=FG,
                               relief="flat", bd=0)
        self.log_box.grid(row=0, column=0, sticky="nsew")
        sb = tk.Scrollbar(lf, command=self.log_box.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.log_box.config(yscrollcommand=sb.set)

        # ── 底部路径提示 ──
        self.lbl(self.root,
                 f"程序目录：{APP_DIR}  |  AppData：{os.path.join(APP_DIR, 'AppData')}",
                 fg="#888", font=("Microsoft YaHei", 8)
                 ).grid(row=row, column=0, pady=(0, 6)); row += 1

    # ── 功能方法 ──
    def refresh(self):
        u = self.u_var.get().strip()
        o = self.o_var.get().strip()

        def path_with(src_label, src_path, dst):
            return f"{src_label}：{src_path}  →  {dst}"

        lines = [
            f"清空 1：C:\\Users\\{u}\\AppData\\Local\\OctaneRender" if u else "清空 1：(待填写用户名)",
            f"清空 2：C:\\Users\\{u}\\AppData\\Roaming\\OctaneRender" if u else "清空 2：(待填写用户名)",
            path_with("AppData", os.path.join(APP_DIR, "AppData"),
                      f"C:\\Users\\{u}\\AppData" if u else "(待填写)"),
            path_with("octane", os.path.join(APP_DIR, "octane"),
                      o if o else "(待填写)"),
        ]
        self.pv.config(state="normal")
        self.pv.delete("1.0", "end")
        self.pv.insert("1.0", "\n".join(lines))
        self.pv.config(state="disabled")

    def save_cfg(self):
        self.config["username"] = self.u_var.get().strip()
        self.config["octane_target"] = self.o_var.get().strip()
        save_config(self.config)

    def pick_oct(self):
        p = filedialog.askdirectory(title="选择 octane 复制目标")
        if p:
            self.o_var.set(p)
            self.config["octane_target"] = p
            save_config(self.config)
            self.refresh()

    def do_clean(self):
        u = self.get_user()
        if not u:
            return
        paths = [
            f"C:\\Users\\{u}\\AppData\\Local\\OctaneRender",
            f"C:\\Users\\{u}\\AppData\\Roaming\\OctaneRender",
        ]
        if not messagebox.askyesno(
                "确认清空",
                f"将清空以下两个目录的所有内容：\n\n{paths[0]}\n{paths[1]}\n\n此操作不可撤销！"):
            return
        for p in paths:
            if os.path.exists(p):
                self.log(f"[清理] {p}")
                safe_clean_folder(p, self.log)
            else:
                self.log(f"[跳过] 不存在：{p}")
        self.log("✅ 全部清理完成\n")

    def do_copy(self):
        u = self.get_user()
        if not u:
            return
        ot = self.o_var.get().strip()
        if not ot:
            messagebox.showerror("错误", "请填写 octane 复制目标路径！")
            return

        src_a = os.path.join(APP_DIR, "AppData")
        src_o = os.path.join(APP_DIR, "octane")

        if not messagebox.askyesno(
                "确认复制",
                f"从当前程序目录复制：\n\n"
                f"AppData → C:\\Users\\{u}\\AppData\n"
                f"octane  → {ot}\n\n"
                f"程序目录：{APP_DIR}\n"
                f"继续吗？"):
            return

        # 复制 AppData → C:\Users\{u}\AppData
        if os.path.exists(src_a):
            self.log(f"[AppData] {src_a} → C:\\Users\\{u}\\AppData")
            try:
                dst = f"C:\\Users\\{u}\\AppData"
                if not os.path.exists(dst):
                    os.makedirs(dst, exist_ok=True)
                for item in os.listdir(src_a):
                    s = os.path.join(src_a, item)
                    d = os.path.join(dst, item)
                    if os.path.isfile(s):
                        shutil.copy2(s, d)
                        self.log(f"  file: {item}")
                    else:
                        if os.path.exists(d):
                            shutil.rmtree(d)
                        shutil.copytree(s, d)
                        self.log(f"  dir:  {item}")
                self.log("  ✅ AppData 完成")
            except Exception as e:
                self.log(f"  ❌ {e}")
        else:
            self.log(f"  ⚠ 当前目录下没有 AppData 文件夹，跳过")
            self.log(f"     查找路径：{src_a}")

        # 复制 octane → 用户指定路径
        if os.path.exists(src_o):
            self.log(f"[octane] {src_o} → {ot}")
            safe_copy_folder(src_o, os.path.join(ot, "octane"), self.log)
        else:
            self.log(f"  ⚠ 当前目录下没有 octane 文件夹，跳过")
            self.log(f"     查找路径：{src_o}")

        self.log("✅ 全部完成\n")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
