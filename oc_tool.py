import os
import sys
import shutil
import webbrowser
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


def auto_username():
    """自动获取当前 Windows 用户名"""
    return os.environ.get("USERNAME", "")


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
        shutil.copytree(src, dst, dirs_exist_ok=True)
        log_func(f"  ✅ 复制完成")
        return True
    except Exception as e:
        log_func(f"  ⚠ 部分文件跳过（{e}）")
        return False


def set_dark_titlebar(root):
    try:
        from ctypes import windll, c_int, byref
        HWND = windll.user32.GetParent(root.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 20, byref(c_int(2)), c_int(4))
    except Exception:
        pass


def open_in_explorer(path):
    """在资源管理器中打开路径，不存在则先创建"""
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        os.startfile(path)
        return True
    except Exception as e:
        return False


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
        self.root.geometry("600x980")
        self.root.minsize(600, 700)
        self.root.configure(bg=BG)

        self.config = load_config()
        set_dark_titlebar(root)
        try:
            root.iconbitmap(os.path.join(APP_DIR, "icon.ico"))
        except Exception:
            pass
        self.build_ui()

    def lbl(self, parent, text, fg=FG, bg=None, font=None, side=None):
        w = tk.Label(parent, text=text, bg=bg or BG, fg=fg,
                     font=font or ("Microsoft YaHei", 10))
        if side:
            w.pack(side=side)
        return w

    def btn(self, parent, text, cmd, bg=BLUE, fg="white", font_size=11):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=bg, fg=fg, activebackground="#555", activeforeground=fg,
                      font=("Microsoft YaHei", font_size, "bold"),
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

    def build_ui(self):
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        row = 0

        # ── 标题 ──
        self.lbl(self.root, "OC插件 快速激活工具",
                 fg="white", font=("Microsoft YaHei", 15, "bold")
                 ).grid(row=row, column=0, pady=(18, 0)); row += 1

        # ── 使用说明 ──
        guide = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        guide.grid(row=row, column=0, padx=16, pady=(0, 6), sticky="ew"); row += 1
        tk.Label(guide, text="确保当前程序目录包含：octane、OctaneRender、thirdparty 文件夹",
                 bg=CARD, fg="#ffcc00", font=("Microsoft YaHei", 10, "bold")
                 ).pack(pady=(6, 2), padx=10, fill="x")
        guide_text = (
            "① 在 C4D 中配置 octane 插件目录\n"
            "② 先「清空」移除 OctaneRender 残留文件\n"
            "③ 后「复制」部署 thirdparty、OctaneRender 等资源\n"
            "④ 保持 YellowStar.exe 程序运行\n"
            "⑤ 运行 C4D 使用 Octane 插件\n"
            "⑥ (可选) 把 YellowStar 放入启动路径，开机自动运行\n"
            "插件失效时，重复 ② ③ 即可恢复。"
        )
        tk.Label(guide, text=guide_text, justify="left",
                 bg=CARD, fg="#aaa", font=("Microsoft YaHei", 12),
                 wraplength=530).pack(padx=10, pady=6, fill="x")

        # ── 配置卡片 ──
        c1 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c1.grid(row=row, column=0, padx=16, pady=12, sticky="ew"); row += 1
        tk.Label(c1, text="配置", bg=CARD, fg="white", anchor="w",
                 font=("Microsoft YaHei", 10, "bold")).pack(pady=(8, 0), padx=4)

        # 配置表单项（grid 对齐）
        cfg_grid = tk.Frame(c1, bg=CARD)
        cfg_grid.pack(fill="x", padx=0, pady=(8, 4))
        cfg_grid.columnconfigure(1, weight=1)

        # 用户名行
        tk.Label(cfg_grid, text="用户名：", bg=CARD, fg=FG,
                 font=("Microsoft YaHei", 10), width=10, anchor="e"
                 ).grid(row=0, column=0, sticky="e", pady=5)

        saved_username = self.config.get("username", "")
        default_username = saved_username if saved_username else auto_username()
        self.u_var = tk.StringVar(value=default_username)
        ue = tk.Entry(cfg_grid, textvariable=self.u_var,
                      bg=INPUT, fg=FG, insertbackground=FG,
                      relief="flat", bd=2)
        ue.grid(row=0, column=1, sticky="ew", padx=(8, 4), pady=5)
        ue.bind("<KeyRelease>", lambda e: self.refresh())
        tk.Label(cfg_grid, text="（已自动获取）", bg=CARD, fg="#888",
                 font=("Microsoft YaHei", 9)).grid(row=0, column=2, pady=5)

        # octane 目标行
        tk.Label(cfg_grid, text="octane目录：", bg=CARD, fg=FG,
                 font=("Microsoft YaHei", 10), width=10, anchor="e"
                 ).grid(row=1, column=0, sticky="e", pady=5)

        self.o_var = tk.StringVar(value=self.config.get("octane_target", ""))
        oe = tk.Entry(cfg_grid, textvariable=self.o_var,
                      bg=INPUT, fg=FG, insertbackground=FG,
                      relief="flat", bd=2)
        oe.grid(row=1, column=1, sticky="ew", padx=(8, 4), pady=5)
        oe.bind("<KeyRelease>", lambda e: self.refresh())
        tk.Button(cfg_grid, text="① 浏览", command=self.pick_oct,
                  bg="#555", fg="white", relief="flat",
                  font=("Microsoft YaHei", 9), padx=6, pady=1
                  ).grid(row=1, column=2, pady=5)

        # 保存按钮
        btn_save = tk.Button(c1, text="保存配置", command=self.save_cfg,
                             bg=BLUE, fg="white", relief="flat",
                             font=("Microsoft YaHei", 10), padx=12, pady=2)
        btn_save.pack(pady=(4, 8))

        # ── 路径预览 ──
        c2 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c2.grid(row=row, column=0, padx=16, pady=(0, 10), sticky="ew"); row += 1
        tk.Label(c2, text="路径预览", bg=BG, fg=FG, anchor="w",
                 font=("Microsoft YaHei", 10, "bold")).pack(pady=(6, 0), padx=4)
        self.pv = tk.Text(c2, height=4, wrap="word",
                          font=("Consolas", 9),
                          bg=BG, fg=FG, insertbackground=FG,
                          relief="flat", bd=0)
        self.pv.pack(fill="x", padx=8, pady=(4, 8))
        self.refresh()

        # ── 功能按钮 ──
        c3 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c3.grid(row=row, column=0, padx=16, pady=(0, 10), sticky="ew"); row += 1
        tk.Label(c3, text="功能操作", bg=CARD, fg="white", anchor="w",
                 font=("Microsoft YaHei", 10, "bold")).pack(pady=(6, 0), padx=4)

        inner = tk.Frame(c3, bg=CARD)
        inner.pack(padx=12, pady=8, fill="x")

        # "打开文件夹" 右对齐小按钮
        open_row = tk.Frame(inner, bg=CARD)
        open_row.pack(fill="x", pady=(0, 8))
        tk.Button(open_row, text="⑥ 📂 打开启动路径",
                  command=lambda: self.open_dir(
                      "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp"),
                  bg="#555", fg="white", relief="flat",
                  font=("Microsoft YaHei", 9), padx=8, pady=2).pack(side="right", padx=(0, 8))
        tk.Button(open_row, text="📂 打开 OctaneRender 文件夹",
                  command=self.open_octane_dirs,
                  bg="#555", fg="white", relief="flat",
                  font=("Microsoft YaHei", 9), padx=8, pady=2).pack(side="right", padx=0)

        self.btn(inner, "② 清空 OctaneRender 残留文件",
                 self.do_clean, bg=RED).pack(pady=4, fill="x")

        self.btn(inner, "③ 复制资源到目标路径",
                 self.do_copy).pack(pady=4, fill="x")

        # ── 日志区 ──
        c4 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove", height=140)
        c4.grid_propagate(False)
        c4.grid(row=row, column=0, padx=16, pady=(0, 10), sticky="ew")
        c4.grid_rowconfigure(1, weight=1)
        c4.grid_columnconfigure(0, weight=1)
        row += 1

        tk.Label(c4, text="操作日志", bg=CARD, fg="white", anchor="w",
                 font=("Microsoft YaHei", 10, "bold")
                 ).grid(row=0, column=0, pady=(6, 0), padx=4)

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

        url_label1 = tk.Label(
            self.root,
            text="20260623  /  世界的风吹向你  /  Workbuddy技术支持  /  开源软件",
            bg=BG, fg="#888", font=("Microsoft YaHei", 8))
        url_label1.grid(row=row, column=0, pady=(0, 0)); row += 1

        def open_url(e):
            webbrowser.open("https://github.com/Simiely/oc-plugin-activator")

        url_label2 = tk.Label(
            self.root,
            text="https://github.com/Simiely/oc-plugin-activator",
            bg=BG, fg="#888", font=("Microsoft YaHei", 8), cursor="hand2")
        url_label2.grid(row=row, column=0, pady=(0, 8)); row += 1
        url_label2.bind("<Button-1>", open_url)
        url_label2.bind("<Enter>", lambda e: url_label2.config(fg="#aaa"))
        url_label2.bind("<Leave>", lambda e: url_label2.config(fg="#888"))

    # ── 功能方法 ──
    def refresh(self):
        u = self.u_var.get().strip()
        o = self.o_var.get().strip()

        lines = [
            f"清空残留 1：C:\\Users\\{u}\\AppData\\Local\\OctaneRender" if u else "清空残留 1：(待填写用户名)",
            f"清空残留 2：C:\\Users\\{u}\\AppData\\Roaming\\OctaneRender" if u else "清空残留 2：(待填写用户名)",
            f"清空残留 3：{o}\\octane" if o else "清空残留 3：(待填写 octane 目标)",
            f"复制 thirdparty  →  C:\\Users\\{u}\\AppData\\Local\\OctaneRender" if u else "复制 thirdparty → (待填写用户名)",
            f"复制 OctaneRender →  C:\\Users\\{u}\\AppData\\Roaming\\OctaneRender" if u else "复制 OctaneRender → (待填写用户名)",
            f"复制 octane  →  {o if o else '(待填写)'}",
        ]
        self.pv.config(state="normal")
        self.pv.delete("1.0", "end")
        self.pv.insert("1.0", "\n".join(lines))
        self.pv.config(state="disabled")

    def save_cfg(self):
        self.config["username"] = self.u_var.get().strip()
        self.config["octane_target"] = self.o_var.get().strip()
        save_config(self.config)

    def fill_username(self):
        """自动获取并填入用户名"""
        name = auto_username()
        if name:
            self.u_var.set(name)
            self.refresh()

    def pick_oct(self):
        p = filedialog.askdirectory(title="选择 octane 复制目标")
        if p:
            self.o_var.set(p)
            self.config["octane_target"] = p
            save_config(self.config)
            self.refresh()

    def open_dir(self, path):
        """通用：在资源管理器打开路径"""
        if open_in_explorer(path):
            self.log(f"📂 {path}（已在资源管理器打开）")
        else:
            self.log(f"  ⚠ 无法打开：{path}")

    def open_octane_dirs(self):
        """在资源管理器中打开两个 OctaneRender 目录"""
        u = self.u_var.get().strip()
        if not u:
            messagebox.showerror("错误", "请先填写用户名！")
            return
        paths = [
            f"C:\\Users\\{u}\\AppData\\Local\\OctaneRender",
            f"C:\\Users\\{u}\\AppData\\Roaming\\OctaneRender",
        ]
        for p in paths:
            if open_in_explorer(p):
                self.log(f"📂 {p}（已在资源管理器打开）")
            else:
                self.log(f"  ⚠ 无法打开：{p}")

    def do_clean(self):
        u = self.get_user()
        if not u:
            return
        o = self.o_var.get().strip()
        paths = [
            f"C:\\Users\\{u}\\AppData\\Local\\OctaneRender",
            f"C:\\Users\\{u}\\AppData\\Roaming\\OctaneRender",
        ]
        if o:
            paths.append(os.path.join(o, "octane"))
        msg = "将清空以下目录的所有内容：\n\n" + "\n".join(paths) + "\n\n此操作不可撤销！"
        if not messagebox.askyesno("确认清空", msg):
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

        src_3rd = os.path.join(APP_DIR, "thirdparty")
        src_or = os.path.join(APP_DIR, "OctaneRender")
        src_oct = os.path.join(APP_DIR, "octane")

        if not messagebox.askyesno(
                "确认复制",
                f"将从程序目录复制：\n\n"
                f"thirdparty  →  C:\\Users\\{u}\\AppData\\Local\\OctaneRender\n"
                f"OctaneRender →  C:\\Users\\{u}\\AppData\\Roaming\\OctaneRender\n"
                f"octane      →  {ot}\n\n"
                f"继续吗？"):
            return

        # 1. thirdparty
        if os.path.exists(src_3rd):
            dst = f"C:\\Users\\{u}\\AppData\\Local\\OctaneRender\\thirdparty"
            self.log(f"[thirdparty] → {dst}")
            safe_copy_folder(src_3rd, dst, self.log)
        else:
            self.log(f"  ⚠ 当前目录下没有 thirdparty 文件夹")
            self.log(f"     查找路径：{src_3rd}")

        # 2. OctaneRender
        if os.path.exists(src_or):
            dst = f"C:\\Users\\{u}\\AppData\\Roaming\\OctaneRender"
            self.log(f"[OctaneRender] → {dst}")
            safe_copy_folder(src_or, dst, self.log)
        else:
            self.log(f"  ⚠ 当前目录下没有 OctaneRender 文件夹")
            self.log(f"     查找路径：{src_or}")

        # 3. octane
        if os.path.exists(src_oct):
            self.log(f"[octane] → {ot}")
            safe_copy_folder(src_oct, os.path.join(ot, "octane"), self.log)
        else:
            self.log(f"  ⚠ 当前目录下没有 octane 文件夹")
            self.log(f"     查找路径：{src_oct}")

        self.log("✅ 全部完成\n")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
