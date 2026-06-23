import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
APP_DIR = os.path.dirname(os.path.abspath(__file__))


def load_config():
    if os.path.exists(CONFIG_FILE):
        import json
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"username": "", "c4doctane_target": ""}


def save_config(config):
    import json
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def get_octane_paths(username):
    """根据用户名生成 OctaneRender 的两个路径"""
    base = f"C:\\Users\\{username}"
    return (
        os.path.join(base, "AppData", "Local", "OctaneRender"),
        os.path.join(base, "AppData", "Roaming", "OctaneRender"),
    )


def safe_clean_folder(path, log_func):
    """安全清空文件夹内容，不删除文件夹本身"""
    if not os.path.exists(path):
        log_func(f"  文件夹不存在，跳过：{path}")
        return
    count_file = 0
    count_dir = 0
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
    """安全复制文件夹"""
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


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("OC插件 快速激活工具")
        self.root.geometry("560x560")
        self.root.resizable(False, False)

        self.config = load_config()

        self.setup_ui()

    def setup_ui(self):
        # 标题
        title_frame = ttk.Frame(self.root, padding=(20, 20, 20, 10))
        title_frame.pack(fill="x")
        ttk.Label(title_frame, text="OC插件 快速激活工具",
                  font=("Microsoft YaHei", 14, "bold")).pack()

        # ===== 配置区 =====
        cfg_frame = ttk.LabelFrame(self.root, text=" 配置 ", padding=15)
        cfg_frame.pack(fill="x", padx=20, pady=(0, 10))
        cfg_frame.columnconfigure(1, weight=1)

        # 用户名
        ttk.Label(cfg_frame, text="用户名：").grid(row=0, column=0, sticky="w", pady=6)
        self.username_var = tk.StringVar(value=self.config.get("username", ""))
        user_entry = ttk.Entry(cfg_frame, textvariable=self.username_var, width=20)
        user_entry.grid(row=0, column=1, sticky="w", padx=(5, 0), pady=6)

        # c4doctane 目标路径
        ttk.Label(cfg_frame, text="c4doctane 复制目标路径：").grid(row=1, column=0, sticky="w", pady=6)
        self.target_var = tk.StringVar(value=self.config.get("c4doctane_target", ""))
        ttk.Entry(cfg_frame, textvariable=self.target_var, width=32).grid(row=1, column=1, sticky="ew", padx=(5, 5), pady=6)
        ttk.Button(cfg_frame, text="选择文件夹", command=self.on_select_target,
                    padding=(8, 2)).grid(row=1, column=2, pady=6)

        # 保存按钮
        ttk.Button(cfg_frame, text="保存配置", command=self.on_save_config,
                    padding=(10, 3)).grid(row=2, column=0, columnspan=3, pady=(6, 0))

        # ===== 路径预览 =====
        preview_frame = ttk.LabelFrame(self.root, text=" 路径预览 ", padding=10)
        preview_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.preview_text = tk.Text(preview_frame, height=4, wrap="word",
                                     font=("Consolas", 9), state="disabled", bg="#f8f8f8")
        self.preview_text.pack(fill="x")
        self.refresh_preview()

        # 用户名改动时实时刷新预览
        user_entry.bind("<KeyRelease>", lambda e: self.refresh_preview())
        self.username_var.trace_add("write", lambda *a: self.refresh_preview())
        self.target_var.trace_add("write", lambda *a: self.refresh_preview())

        # ===== 功能按钮 =====
        btn_frame = ttk.LabelFrame(self.root, text=" 功能操作 ", padding=18)
        btn_frame.pack(fill="x", padx=20, pady=(0, 10))
        btn_inner = ttk.Frame(btn_frame)
        btn_inner.pack(expand=True)

        btn_style = {"width": 38, "padding": (0, 8)}

        ttk.Button(btn_inner, text="🗑 清空 OctaneRender (Local)",
                    command=self.on_clean_local, **btn_style).pack(pady=5, fill="x")
        ttk.Button(btn_inner, text="🗑 清空 OctaneRender (Roaming)",
                    command=self.on_clean_roaming, **btn_style).pack(pady=5, fill="x")
        ttk.Button(btn_inner, text="📋 复制 AppData 文件夹到用户目录",
                    command=self.on_copy_appdata, **btn_style).pack(pady=5, fill="x")
        ttk.Button(btn_inner, text="📋 复制 c4doctane 文件夹到目标路径",
                    command=self.on_copy_c4doctane, **btn_style).pack(pady=5, fill="x")

        # ===== 日志区 =====
        log_frame = ttk.LabelFrame(self.root, text=" 操作日志 ", padding=8)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        self.log_text = tk.Text(log_frame, height=7, wrap="word", font=("Consolas", 9))
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def refresh_preview(self):
        username = self.username_var.get().strip()
        target = self.target_var.get().strip()
        local_path = f"C:\\Users\\{username}\\AppData\\Local\\OctaneRender" if username else "(请填写用户名)"
        roam_path = f"C:\\Users\\{username}\\AppData\\Roaming\\OctaneRender" if username else "(请填写用户名)"
        appdata_src = os.path.join(APP_DIR, "AppData")
        c4d_src = os.path.join(APP_DIR, "c4doctane")

        text = (
            f"清空 Local  ：{local_path}\n"
            f"清空 Roaming：{roam_path}\n"
            f"复制 AppData ：{appdata_src}  →  C:\\Users\\{username if username else '(请填写用户名)'}\n"
            f"复制 c4doctane：{c4d_src}  →  {target if target else '(请填写目标路径)'}"
        )
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
        self.config["c4doctane_target"] = self.target_var.get().strip()
        save_config(self.config)
        messagebox.showinfo("成功", "配置已保存！")

    def on_select_target(self):
        path = filedialog.askdirectory(title="选择 c4doctane 复制目标文件夹")
        if path:
            self.target_var.set(path)
            self.config["c4doctane_target"] = path
            save_config(self.config)
            self.refresh_preview()

    def on_clean_local(self):
        username = self.get_username()
        if not username:
            return
        path = f"C:\\Users\\{username}\\AppData\\Local\\OctaneRender"
        if not messagebox.askyesno("确认清空", f"确定要清空以下文件夹吗？\n\n{path}\n\n此操作不可撤销！"):
            return
        self.log(f"[清空 Local] 开始：{path}")
        safe_clean_folder(path, self.log)
        self.log("✅ 完成\n")

    def on_clean_roaming(self):
        username = self.get_username()
        if not username:
            return
        path = f"C:\\Users\\{username}\\AppData\\Roaming\\OctaneRender"
        if not messagebox.askyesno("确认清空", f"确定要清空以下文件夹吗？\n\n{path}\n\n此操作不可撤销！"):
            return
        self.log(f"[清空 Roaming] 开始：{path}")
        safe_clean_folder(path, self.log)
        self.log("✅ 完成\n")

    def on_copy_appdata(self):
        username = self.get_username()
        if not username:
            return
        src = os.path.join(APP_DIR, "AppData")
        dst = f"C:\\Users\\{username}"
        if not os.path.exists(src):
            messagebox.showerror("错误", f"源文件夹不存在：\n{src}")
            return
        if not messagebox.askyesno("确认复制", f"确定要复制吗？\n\n源：{src}\n目标：{dst}"):
            return
        self.log(f"[复制 AppData] 开始：{src} → {dst}")
        # 复制 AppData 文件夹到 C:\Users\{username}\AppData
        # 实际上是把程序目录下的 AppData 文件夹，合并到目标 AppData
        dst_appdata = os.path.join(dst, "AppData")
        try:
            if not os.path.exists(dst_appdata):
                os.makedirs(dst_appdata, exist_ok=True)
            # 复制 AppData 下的内容到目标
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst_appdata, item)
                if os.path.isfile(s):
                    shutil.copy2(s, d)
                    self.log(f"  已复制文件：{item}")
                else:
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                    self.log(f"  已复制文件夹：{item}")
            self.log("✅ 完成\n")
            messagebox.showinfo("完成", "AppData 复制完成！")
        except Exception as e:
            self.log(f"❌ 错误：{e}\n")
            messagebox.showerror("错误", str(e))

    def on_copy_c4doctane(self):
        username = self.get_username()
        if not username:
            return
        target = self.target_var.get().strip()
        if not target:
            messagebox.showerror("错误", "请先填写或选择 c4doctane 复制目标路径！")
            return
        src = os.path.join(APP_DIR, "c4doctane")
        if not os.path.exists(src):
            messagebox.showerror("错误", f"源文件夹不存在：\n{src}")
            return
        if not messagebox.askyesno("确认复制", f"确定要复制吗？\n\n源：{src}\n目标：{target}"):
            return
        self.log(f"[复制 c4doctane] 开始：{src} → {target}")
        if safe_copy_folder(src, os.path.join(target, "c4doctane"), self.log):
            self.log("✅ 完成\n")
            messagebox.showinfo("完成", "c4doctane 复制完成！")
        else:
            self.log("❌ 失败\n")


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
