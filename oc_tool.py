import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

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
            log_func(f"  跳过：{item} - {e}")
    log_func(f"  已删除 {c1} 个文件，{c2} 个文件夹")


def safe_copy_folder(src, dst, log_func):
    if not os.path.exists(src):
        log_func(f"  源文件夹不存在：{src}")
        return False
    try:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        log_func(f"  复制完成")
        return True
    except Exception as e:
        log_func(f"  复制失败：{e}")
        return False


# 颜色
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
        self.root.geometry("460x540")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.config = load_config()
        self.build_ui()

    # ---- 工具方法 ----
    def btn(self, parent, text, cmd, bg=BLUE, fg="white", w=0, h=0):
        """安全的按钮，不含 tuple 参数"""
        kwargs = dict(text=text, command=cmd, bg=bg, fg=fg,
                      font=("Microsoft YaHei", 11, "bold"),
                      relief="flat", cursor="hand2",
                      activebackground=bg, activeforeground=fg)
        if w: kwargs["width"] = w
        if h: kwargs["height"] = h
        b = tk.Button(parent, **kwargs)
        b.bind("<Enter>", lambda e: b.config(bg="#555"))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        return b

    def label(self, parent, text, fg=FG, bg=None, font=None):
        return tk.Label(parent, text=text, bg=bg or BG, fg=fg,
                        font=font or ("Microsoft YaHei", 10))

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

    # ---- 界面 ----
    def build_ui(self):
        # ── 标题 ──
        self.label(self.root, "OC插件 快速激活工具",
                   fg="white", font=("Microsoft YaHei", 15, "bold")
                   ).pack(pady=(18, 0))

        # ── 配置卡片 ──
        c1 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c1.pack(fill="x", padx=16, pady=14)

        self.label(c1, "配置", fg="white",
                   font=("Microsoft YaHei", 10, "bold")).pack(pady=(8, 0))

        r1 = tk.Frame(c1, bg=CARD)
        r1.pack(fill="x", padx=12, pady=(8, 4))
        self.label(r1, "用户名：", bg=CARD).pack(side="left")
        self.u_var = tk.StringVar(value=self.config.get("username", ""))
        ue = tk.Entry(r1, textvariable=self.u_var, width=22,
                      bg=INPUT, fg=FG, insertbackground=FG,
                      relief="flat", bd=2)
        ue.pack(side="left", padx=8)
        ue.bind("<KeyRelease>", lambda e: self.refresh())

        r2 = tk.Frame(c1, bg=CARD)
        r2.pack(fill="x", padx=12, pady=(4, 8))
        self.label(r2, "octane 目标：", bg=CARD).pack(side="left")
        self.o_var = tk.StringVar(value=self.config.get("octane_target", ""))
        oe = tk.Entry(r2, textvariable=self.o_var, width=16,
                      bg=INPUT, fg=FG, insertbackground=FG,
                      relief="flat", bd=2)
        oe.pack(side="left", padx=8)
        oe.bind("<KeyRelease>", lambda e: self.refresh())
        tk.Button(r2, text="选", command=self.pick_oct,
                  bg="#555", fg="white", relief="flat",
                  font=("Microsoft YaHei", 9), padx=6, pady=2).pack(side="left")

        tk.Button(c1, text="保存配置", command=self.save_cfg,
                  bg=BLUE, fg="white", relief="flat",
                  font=("Microsoft YaHei", 10), padx=12, pady=2).pack(pady=(0, 8))

        # ── 预览 ──
        c2 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c2.pack(fill="x", padx=16, pady=(0, 12))

        self.label(c2, "路径预览", fg="white",
                   font=("Microsoft YaHei", 10, "bold")).pack(pady=(6, 0))
        self.pv = tk.Text(c2, height=4, wrap="word",
                          font=("Consolas", 9),
                          bg=BG, fg=FG, insertbackground=FG,
                          relief="flat", bd=0)
        self.pv.pack(fill="x", padx=8, pady=(4, 8))
        self.refresh()

        # ── 按钮 ──
        c3 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c3.pack(fill="x", padx=16, pady=(0, 12))

        self.label(c3, "功能操作", fg="white",
                   font=("Microsoft YaHei", 10, "bold")).pack(pady=(6, 0))

        inner = tk.Frame(c3, bg=CARD)
        inner.pack(padx=12, pady=8, fill="x")

        self.btn(inner, "🗑  清空 OctaneRender 缓存",
                 self.do_clean, bg=RED).pack(pady=4, fill="x")
        self.btn(inner, "📋  复制资源到目标路径",
                 self.do_copy).pack(pady=4, fill="x")

        # ── 日志 ──
        c4 = tk.Frame(self.root, bg=CARD, bd=1, relief="groove")
        c4.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self.label(c4, "操作日志", fg="white",
                   font=("Microsoft YaHei", 10, "bold")).pack(pady=(6, 0))

        lf = tk.Frame(c4, bg=BG)
        lf.pack(fill="both", expand=True, padx=8, pady=(4, 8))

        self.log_box = tk.Text(lf, height=6, wrap="word",
                               font=("Consolas", 9),
                               bg=BG, fg=FG, insertbackground=FG,
                               relief="flat", bd=0)
        self.log_box.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(lf, command=self.log_box.yview)
        sb.pack(side="right", fill="y")
        self.log_box.config(yscrollcommand=sb.set)

        # ── 底部 ──
        self.label(self.root, f"程序目录：{APP_DIR}",
                   fg="#666", font=("Microsoft YaHei", 8)
                   ).pack(pady=(0, 6))

    # ---- 方法 ----
    def refresh(self):
        u = self.u_var.get().strip()
        o = self.o_var.get().strip()
        lines = [
            ("清空", f"C:\\Users\\{u}\\AppData\\Local\\OctaneRender" if u else "(待填写)"),
            ("清空", f"C:\\Users\\{u}\\AppData\\Roaming\\OctaneRender" if u else "(待填写)"),
            ("复制", f"{os.path.join(APP_DIR, 'AppData')}  →  C:\\Users\\{u if u else '(待填写)'}\\AppData"),
            ("复制", f"{os.path.join(APP_DIR, 'octane')}  →  {o if o else '(待填写)'}"),
        ]
        t = "\n".join(f"{a}：{b}" for a, b in lines)
        self.pv.config(state="normal")
        self.pv.delete("1.0", "end")
        self.pv.insert("1.0", t)
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
                "确认", f"清空以下两个目录所有内容？\n\n{paths[0]}\n{paths[1]}\n\n不可撤销！"):
            return
        for p in paths:
            self.log(f"[清理] {p}")
            safe_clean_folder(p, self.log)
        self.log("✅ 完成\n")

    def do_copy(self):
        u = self.get_user()
        if not u:
            return
        ot = self.o_var.get().strip()
        if not ot:
            messagebox.showerror("错误", "请填写 octane 复制目标路径！")
            return
        src_a = os.path.join(APP_DIR, "AppData")
        dst = f"C:\\Users\\{u}\\AppData"
        src_o = os.path.join(APP_DIR, "octane")
        dst_o = os.path.join(ot, "octane")
        if not messagebox.askyesno(
                "确认", f"复制 AppData → {dst}\n复制 octane → {ot}\n\n继续？"):
            return
        if os.path.exists(src_a):
            self.log(f"[AppData] 开始")
            try:
                if not os.path.exists(dst):
                    os.makedirs(dst, exist_ok=True)
                for item in os.listdir(src_a):
                    s = os.path.join(src_a, item)
                    d = os.path.join(dst, item)
                    if os.path.isfile(s):
                        shutil.copy2(s, d)
                    else:
                        if os.path.exists(d):
                            shutil.rmtree(d)
                        shutil.copytree(s, d)
                self.log("  ✅ AppData 完成")
            except Exception as e:
                self.log(f"  ❌ {e}")
        else:
            self.log("  ⚠ AppData 不存在，跳过")
        if os.path.exists(src_o):
            self.log(f"[octane] 开始")
            safe_copy_folder(src_o, dst_o, self.log)
        else:
            self.log("  ⚠ octane 不存在，跳过")
        self.log("✅ 全部完成\n")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
