import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import webbrowser
import os
import sys

# Ensure sibling top-level modules are importable when running this file directly
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_CURRENT_DIR)
if _REPO_ROOT not in sys.path:
    sys.path.append(_REPO_ROOT)
import marketSpider
from spider import zhihuSpider


class ZhihuSpiderGUI:
    def __init__(self, master):
        self.master = master
        master.title("ZhiHu Tools GUI")
        master.geometry("600x600")
        master.resizable(True, True)

        self.spider = zhihuSpider()  # 复用原有类，获取 header 等

        # ------------------- 顶部说明 -------------------
        tk.Label(master, text="ZhiHu Tools", font=("微软雅黑", 14, "bold")).pack(pady=10)

        # ------------------- 选项选择（Radiobutton） -------------------
        frame_option = tk.Frame(master)
        frame_option.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_option, text="选择功能：", font=("微软雅黑", 12)).pack(anchor="w")
        self.radio_buttons = {}
        self.option_var = tk.StringVar(value="2")  # 默认选中 2

        options = [
            ("1. 爬取盐选的单个问题（暂未实现）", "1", False),
            ("2. 爬取书的单个章节（已实现）", "2", True),
            ("3. 爬取整本书（暂未实现）", "3", False),
            ("4. 关键词搜索爬取（暂未实现）", "4", False),
        ]

        for text, value, enabled in options:
            rb = tk.Radiobutton(
                frame_option,
                text=text,
                variable=self.option_var,
                value=value,
                font=("微软雅黑", 11),
                anchor="w",
                state="normal" if enabled else "disabled"
            )
            rb.pack(fill="x", pady=3)
            self.radio_buttons[value] = rb

        # ------------------- 链接输入区 -------------------
        frame_input = tk.Frame(master)
        frame_input.pack(pady=15, padx=20, fill="x")

        tk.Label(frame_input, text="目标链接：", font=("微软雅黑", 11)).pack(side="left", padx=(0, 10))

        self.placeholder_text = "https://www.zhihu.com/market/paid_column/xxxx/section/xxxx"
        self.link_entry = tk.Entry(frame_input, width=56, font=("Consolas", 11), fg="grey")
        self.link_entry.pack(side="left", expand=False, fill="x")
        self.link_entry.insert(0, self.placeholder_text)

        self.link_entry.bind("<FocusIn>", lambda e: (
            self.link_entry.delete(0, tk.END),
            self.link_entry.config(fg="black")
        ) if self.link_entry.get() == self.placeholder_text else None)

        self.link_entry.bind("<FocusOut>", lambda e: (
            self.link_entry.insert(0, self.placeholder_text),
            self.link_entry.config(fg="grey")
        ) if not self.link_entry.get() else None)

        # ------------------- 开始按钮 -------------------
        btn_start = ttk.Button(master, text="开始爬取", command=self.start_crawl_thread, style="Accent.TButton")
        btn_start.pack(pady=15)

        # ------------------- 日志输出区 -------------------
        self.log_text = scrolledtext.ScrolledText(master, height=10, font=("Consolas", 10),
                                                  bg="#f8f8f8", state="disabled")
        self.log_text.pack(padx=20, pady=(0,10), fill="both", expand=False)

        # ------------------- 状态栏 -------------------
        self.status_var = tk.StringVar(value="就绪")
        status_bar = tk.Label(master, textvariable=self.status_var, bd=1, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")

        # 美化按钮（可选，使用 ttk 主题）
        style = ttk.Style()
        style.configure("Accent.TButton", font=("微软雅黑", 12, "bold"))

        # -------------------- Github地址 ---------------
        footer_frame = tk.Frame(master)
        footer_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 5))
        author_label = tk.Label(
            footer_frame,
            text="作者：onewhitethreee",
            font=("微软雅黑", 9),
            fg="#666666"
        )
        author_label.pack(side="right")
        github_label = tk.Label(
            footer_frame,
            text="GitHub: onewhitethreee/zhihu_tools",
            font=("微软雅黑", 9, "underline"),
            fg="#0066cc",  # 蓝色链接色
            cursor="hand2"  # 鼠标悬停变小手
        )
        github_label.pack(side="right")
        def open_github(event=None):
            webbrowser.open_new("https://github.com/onewhitethreee/zhihu_tools")
        github_label.bind("<Button-1>", open_github)  # 左键点击
        github_label.bind("<Enter>", lambda e: github_label.config(fg="#003366"))  # 悬停变深蓝
        github_label.bind("<Leave>", lambda e: github_label.config(fg="#0066cc"))  # 离开恢复

    def log(self, message):
        """向文本框追加日志"""
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def start_crawl_thread(self):
        """用线程防止 GUI 卡死"""
        option = self.option_var.get()
        link = self.link_entry.get().strip()

        if option != "2":
            messagebox.showwarning("提示", f"选项 {option} 暂未实现，敬请期待！\n\nGitHub: https://github.com/onewhitethreee/zhihu_tools")
            return

        # Treat placeholder text as empty input so it cannot be crawled
        if (not link) or (hasattr(self, "placeholder_text") and link == self.placeholder_text):
            messagebox.showerror("错误", "请输入目标链接！")
            return

        self.log("═══════════════════════════════════════")
        self.log("开始爬取...")
        self.status_var.set("爬取中... 请稍候")

        # 用线程运行爬取（避免阻塞主线程）
        thread = threading.Thread(target=self.do_crawl, args=(link,))
        thread.daemon = True
        thread.start()

    def do_crawl(self, link):
        try:
            market = marketSpider.MarketSpider(self.spider._zhihuSpider__header)
            market.spider(link)
            # 在主线程中更新日志
            self.master.after(0, lambda: self.log("爬取完成！文件已保存。"))
        except Exception as e:
            # 在主线程中更新错误日志
            msg = f"爬取失败：{str(e)}"
            self.master.after(0, lambda m=msg: self.log(m))
        finally:
            # 在主线程中更新状态
            self.master.after(0, lambda: self.status_var.set("就绪"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ZhihuSpiderGUI(root)
    root.mainloop()