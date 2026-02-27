import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from typing import List
import json

from .core import FileRenamer
from . import patterns
from .i18n import get_text, LANGUAGES


class BatchRenamerGUI:
    """批量重命名工具 GUI - Batch Renamer GUI"""
    
    def __init__(self, root, lang='en'):
        self.root = root
        self.lang = lang
        self.load_language_preference()
        
        self.root.title(get_text('window_title', self.lang))
        self.root.geometry("1200x700")
        
        # 核心对象
        self.renamer = FileRenamer()
        self.current_directory = None
        self.current_files = []
        self.preview_results = []
        
        # 设置样式
        self.setup_style()
        
        # 创建界面
        self.create_widgets()
        
        # 绑定快捷键
        self.root.bind('<Control-o>', lambda e: self.select_directory())
        self.root.bind('<Control-p>', lambda e: self.preview_rename())
        self.root.bind('<Control-r>', lambda e: self.execute_rename())
        self.root.bind('<Control-z>', lambda e: self.undo_operation())
    
    def load_language_preference(self):
        """加载语言偏好 - Load language preference"""
        try:
            config_file = Path.home() / ".batch_renamer_config.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.lang = config.get('language', 'en')
        except Exception:
            self.lang = 'en'
    
    def save_language_preference(self):
        """保存语言偏好 - Save language preference"""
        try:
            config_file = Path.home() / ".batch_renamer_config.json"
            config = {'language': self.lang}
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def switch_language(self):
        """切换语言 - Switch language"""
        self.lang = 'zh' if self.lang == 'en' else 'en'
        self.save_language_preference()
        
        # 提示重启
        msg = "Language changed. Please restart the application." if self.lang == 'en' else "语言已切换，请重启程序。"
        messagebox.showinfo("Info" if self.lang == 'en' else "信息", msg)
    
    def setup_style(self):
        """设置界面样式 - Setup style"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
    
    def create_widgets(self):
        """创建所有界面组件 - Create all widgets"""
        # 顶部工具栏
        self.create_toolbar()
        
        # 主内容区域
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧：文件列表
        self.create_file_list(main_frame)
        
        # 右侧：重命名选项
        self.create_options_panel(main_frame)
        
        # 底部状态栏
        self.create_statusbar()
    
    def create_toolbar(self):
        """创建顶部工具栏 - Create toolbar"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # 选择目录按钮
        ttk.Button(
            toolbar, 
            text=get_text('select_directory', self.lang), 
            command=self.select_directory
        ).pack(side=tk.LEFT, padx=2)
        
        # 刷新按钮
        ttk.Button(
            toolbar, 
            text=get_text('refresh', self.lang), 
            command=self.refresh_files
        ).pack(side=tk.LEFT, padx=2)
        
        # 分隔符
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # 预览按钮
        ttk.Button(
            toolbar, 
            text=get_text('preview', self.lang), 
            command=self.preview_rename
        ).pack(side=tk.LEFT, padx=2)
        
        # 执行重命名按钮
        self.rename_button = ttk.Button(
            toolbar, 
            text=get_text('execute_rename', self.lang), 
            command=self.execute_rename,
            state=tk.DISABLED
        )
        self.rename_button.pack(side=tk.LEFT, padx=2)
        
        # 撤销按钮
        ttk.Button(
            toolbar, 
            text=get_text('undo', self.lang), 
            command=self.undo_operation
        ).pack(side=tk.LEFT, padx=2)
        
        # 分隔符
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # 清空历史按钮
        ttk.Button(
            toolbar, 
            text=get_text('clear_history', self.lang), 
            command=self.clear_history
        ).pack(side=tk.LEFT, padx=2)
        
        # 语言切换按钮
        lang_text = "中文" if self.lang == 'en' else "English"
        ttk.Button(
            toolbar,
            text=f"🌐 {lang_text}",
            command=self.switch_language
        ).pack(side=tk.RIGHT, padx=2)
        
        # 帮助按钮
        ttk.Button(
            toolbar, 
            text=get_text('help', self.lang), 
            command=self.show_help
        ).pack(side=tk.RIGHT, padx=2)
    
    def create_file_list(self, parent):
        """创建文件列表区域 - Create file list area"""
        left_frame = ttk.Frame(parent)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 标题
        ttk.Label(
            left_frame, 
            text=get_text('file_list', self.lang), 
            style='Header.TLabel'
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # 过滤选项
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(filter_frame, text=get_text('file_type', self.lang)).pack(side=tk.LEFT, padx=(0, 5))
        
        self.file_pattern = tk.StringVar(value="*")
        pattern_combo = ttk.Combobox(
            filter_frame, 
            textvariable=self.file_pattern,
            values=["*", "*.jpg", "*.png", "*.txt", "*.pdf", "*.mp3", "*.mp4"],
            width=15
        )
        pattern_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.recursive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            filter_frame, 
            text=get_text('include_subdirs', self.lang), 
            variable=self.recursive_var,
            command=self.refresh_files
        ).pack(side=tk.LEFT)
        
        # 文件列表和预览对比
        list_notebook = ttk.Notebook(left_frame)
        list_notebook.pack(fill=tk.BOTH, expand=True)
        
        # 原始文件列表标签页
        original_frame = ttk.Frame(list_notebook)
        list_notebook.add(original_frame, text=get_text('original_files', self.lang))
        
        self.file_listbox = tk.Listbox(
            original_frame, 
            selectmode=tk.EXTENDED,
            font=('Courier', 9)
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(original_frame, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # 预览对比标签页
        preview_frame = ttk.Frame(list_notebook)
        list_notebook.add(preview_frame, text=get_text('preview_comparison', self.lang))
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            font=('Courier', 9),
            wrap=tk.NONE
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # 文件统计
        self.file_count_label = ttk.Label(left_frame, text=get_text('file_count', self.lang).format(0))
        self.file_count_label.pack(anchor=tk.W, pady=(5, 0))
    
    def create_options_panel(self, parent):
        """创建右侧选项面板 - Create options panel"""
        right_frame = ttk.Frame(parent, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_frame.pack_propagate(False)
        
        # 标题
        ttk.Label(
            right_frame, 
            text=get_text('rename_options', self.lang), 
            style='Header.TLabel'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # 创建滚动区域
        canvas = tk.Canvas(right_frame)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 重命名模式选择
        self.rename_mode = tk.StringVar(value="prefix")
        modes = [
            (get_text('mode_prefix', self.lang), "prefix"),
            (get_text('mode_suffix', self.lang), "suffix"),
            (get_text('mode_replace', self.lang), "replace"),
            (get_text('mode_number', self.lang), "number"),
            (get_text('mode_case', self.lang), "case"),
            (get_text('mode_datetime', self.lang), "datetime"),
            (get_text('mode_remove', self.lang), "remove"),
        ]
        
        ttk.Label(scrollable_frame, text=get_text('rename_mode', self.lang), font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        for text, mode in modes:
            ttk.Radiobutton(
                scrollable_frame,
                text=text,
                variable=self.rename_mode,
                value=mode,
                command=self.update_options_visibility
            ).pack(anchor=tk.W)
        
        ttk.Separator(scrollable_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # 各种模式的选项
        self.create_prefix_options(scrollable_frame)
        self.create_suffix_options(scrollable_frame)
        self.create_replace_options(scrollable_frame)
        self.create_number_options(scrollable_frame)
        self.create_case_options(scrollable_frame)
        self.create_datetime_options(scrollable_frame)
        self.create_remove_options(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 初始显示
        self.update_options_visibility()
    
    def create_prefix_options(self, parent):
        """创建前缀选项 - Create prefix options"""
        self.prefix_frame = ttk.LabelFrame(parent, text=get_text('prefix_settings', self.lang), padding=10)
        
        ttk.Label(self.prefix_frame, text=get_text('prefix', self.lang)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.prefix_entry = ttk.Entry(self.prefix_frame, width=30)
        self.prefix_entry.grid(row=0, column=1, pady=5)
        self.prefix_entry.insert(0, "new_")
    
    def create_suffix_options(self, parent):
        """创建后缀选项 - Create suffix options"""
        self.suffix_frame = ttk.LabelFrame(parent, text=get_text('suffix_settings', self.lang), padding=10)
        
        ttk.Label(self.suffix_frame, text=get_text('suffix', self.lang)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.suffix_entry = ttk.Entry(self.suffix_frame, width=30)
        self.suffix_entry.grid(row=0, column=1, pady=5)
        self.suffix_entry.insert(0, "_backup")
    
    def create_replace_options(self, parent):
        """创建替换选项 - Create replace options"""
        self.replace_frame = ttk.LabelFrame(parent, text=get_text('replace_settings', self.lang), padding=10)
        
        ttk.Label(self.replace_frame, text=get_text('find', self.lang)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.replace_old = ttk.Entry(self.replace_frame, width=30)
        self.replace_old.grid(row=0, column=1, pady=5)
        
        ttk.Label(self.replace_frame, text=get_text('replace_with', self.lang)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.replace_new = ttk.Entry(self.replace_frame, width=30)
        self.replace_new.grid(row=1, column=1, pady=5)
        
        self.replace_regex = tk.BooleanVar()
        ttk.Checkbutton(
            self.replace_frame, 
            text=get_text('use_regex', self.lang), 
            variable=self.replace_regex
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.replace_case = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.replace_frame, 
            text=get_text('case_sensitive', self.lang), 
            variable=self.replace_case
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def create_number_options(self, parent):
        """创建序号选项 - Create number options"""
        self.number_frame = ttk.LabelFrame(parent, text=get_text('number_settings', self.lang), padding=10)
        
        ttk.Label(self.number_frame, text=get_text('start_number', self.lang)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.number_start = tk.IntVar(value=1)
        ttk.Spinbox(
            self.number_frame, 
            from_=0, 
            to=9999, 
            textvariable=self.number_start,
            width=28
        ).grid(row=0, column=1, pady=5)
        
        ttk.Label(self.number_frame, text=get_text('number_digits', self.lang)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.number_digits = tk.IntVar(value=3)
        ttk.Spinbox(
            self.number_frame, 
            from_=1, 
            to=10, 
            textvariable=self.number_digits,
            width=28
        ).grid(row=1, column=1, pady=5)
        
        ttk.Label(self.number_frame, text=get_text('prefix', self.lang)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.number_prefix = ttk.Entry(self.number_frame, width=30)
        self.number_prefix.grid(row=2, column=1, pady=5)
        self.number_prefix.insert(0, "file_")
        
        self.number_keep = tk.BooleanVar()
        ttk.Checkbutton(
            self.number_frame, 
            text=get_text('keep_original', self.lang), 
            variable=self.number_keep
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def create_case_options(self, parent):
        """创建大小写选项 - Create case options"""
        self.case_frame = ttk.LabelFrame(parent, text=get_text('case_settings', self.lang), padding=10)
        
        self.case_type = tk.StringVar(value="lower")
        cases = [
            (get_text('lowercase', self.lang), "lower"),
            (get_text('uppercase', self.lang), "upper"),
            (get_text('titlecase', self.lang), "title"),
            (get_text('sentencecase', self.lang), "sentence")
        ]
        
        for text, value in cases:
            ttk.Radiobutton(
                self.case_frame,
                text=text,
                variable=self.case_type,
                value=value
            ).pack(anchor=tk.W, pady=2)
    
    def create_datetime_options(self, parent):
        """创建日期时间选项 - Create datetime options"""
        self.datetime_frame = ttk.LabelFrame(parent, text=get_text('datetime_settings', self.lang), padding=10)
        
        ttk.Label(self.datetime_frame, text=get_text('date_format', self.lang)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.datetime_format = tk.StringVar(value="%Y%m%d_%H%M%S")
        format_combo = ttk.Combobox(
            self.datetime_frame,
            textvariable=self.datetime_format,
            values=[
                "%Y%m%d_%H%M%S",
                "%Y-%m-%d_%H-%M-%S",
                "%Y%m%d",
                "%Y-%m-%d",
                "%Y%m%d%H%M%S"
            ],
            width=27
        )
        format_combo.grid(row=0, column=1, pady=5)
        
        self.datetime_modified = tk.BooleanVar(value=True)
        ttk.Radiobutton(
            self.datetime_frame,
            text=get_text('use_modified_time', self.lang),
            variable=self.datetime_modified,
            value=True
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        ttk.Radiobutton(
            self.datetime_frame,
            text=get_text('use_creation_time', self.lang),
            variable=self.datetime_modified,
            value=False
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        ttk.Label(self.datetime_frame, text=get_text('prefix', self.lang)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.datetime_prefix = ttk.Entry(self.datetime_frame, width=30)
        self.datetime_prefix.grid(row=3, column=1, pady=5)
        
        ttk.Label(self.datetime_frame, text=get_text('suffix', self.lang)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.datetime_suffix = ttk.Entry(self.datetime_frame, width=30)
        self.datetime_suffix.grid(row=4, column=1, pady=5)
        
        self.datetime_keep = tk.BooleanVar()
        ttk.Checkbutton(
            self.datetime_frame,
            text=get_text('keep_original', self.lang),
            variable=self.datetime_keep
        ).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def create_remove_options(self, parent):
        """创建删除字符选项 - Create remove options"""
        self.remove_frame = ttk.LabelFrame(parent, text=get_text('remove_settings', self.lang), padding=10)
        
        self.remove_spaces = tk.BooleanVar()
        ttk.Checkbutton(
            self.remove_frame,
            text=get_text('remove_spaces', self.lang),
            variable=self.remove_spaces
        ).pack(anchor=tk.W, pady=2)
        
        self.remove_special = tk.BooleanVar()
        ttk.Checkbutton(
            self.remove_frame,
            text=get_text('remove_special', self.lang),
            variable=self.remove_special
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Label(self.remove_frame, text=get_text('custom_remove', self.lang)).pack(anchor=tk.W, pady=(10, 2))
        self.remove_custom = ttk.Entry(self.remove_frame, width=35)
        self.remove_custom.pack(anchor=tk.W, pady=2)
    
    def create_statusbar(self):
        """创建底部状态栏 - Create status bar"""
        self.statusbar = ttk.Label(
            self.root, 
            text=get_text('status_ready', self.lang), 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_options_visibility(self):
        """根据选择的模式更新选项面板的可见性"""
        # 隐藏所有选项框
        for frame in [self.prefix_frame, self.suffix_frame, self.replace_frame,
                     self.number_frame, self.case_frame, self.datetime_frame,
                     self.remove_frame]:
            frame.pack_forget()
        
        # 显示当前模式的选项框
        mode = self.rename_mode.get()
        if mode == "prefix":
            self.prefix_frame.pack(fill=tk.X, pady=5)
        elif mode == "suffix":
            self.suffix_frame.pack(fill=tk.X, pady=5)
        elif mode == "replace":
            self.replace_frame.pack(fill=tk.X, pady=5)
        elif mode == "number":
            self.number_frame.pack(fill=tk.X, pady=5)
        elif mode == "case":
            self.case_frame.pack(fill=tk.X, pady=5)
        elif mode == "datetime":
            self.datetime_frame.pack(fill=tk.X, pady=5)
        elif mode == "remove":
            self.remove_frame.pack(fill=tk.X, pady=5)
    
    def select_directory(self):
        """选择目录 - Select directory"""
        directory = filedialog.askdirectory(title="Select Directory" if self.lang == 'en' else "选择目录")
        if directory:
            self.current_directory = directory
            self.refresh_files()
            self.update_status(get_text('status_directory_selected', self.lang).format(directory))
    
    def refresh_files(self):
        """刷新文件列表 - Refresh file list"""
        if not self.current_directory:
            return
        
        try:
            pattern = self.file_pattern.get()
            recursive = self.recursive_var.get()
            
            self.current_files = self.renamer.get_files(
                self.current_directory,
                pattern,
                recursive
            )
            
            # 更新文件列表
            self.file_listbox.delete(0, tk.END)
            for file_path in self.current_files:
                rel_path = file_path.relative_to(self.current_directory)
                self.file_listbox.insert(tk.END, str(rel_path))
            
            # 全选
            self.file_listbox.select_set(0, tk.END)
            
            # 更新统计
            self.file_count_label.config(text=get_text('file_count', self.lang).format(len(self.current_files)))
            self.update_status(get_text('status_files_found', self.lang).format(len(self.current_files)))
            
        except Exception as e:
            messagebox.showerror(
                get_text('error', self.lang), 
                get_text('refresh_error', self.lang).format(str(e))
            )
    
    def get_selected_files(self) -> List[Path]:
        """获取选中的文件 - Get selected files"""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            return self.current_files
        return [self.current_files[i] for i in selected_indices]
    
    def preview_rename(self):
        """预览重命名结果 - Preview rename"""
        files = self.get_selected_files()
        
        if not files:
            messagebox.showwarning(
                get_text('warning', self.lang), 
                get_text('no_files', self.lang)
            )
            return
        
        try:
            mode = self.rename_mode.get()
            
            if mode == "prefix":
                rename_func = patterns.add_prefix
                kwargs = {"prefix": self.prefix_entry.get()}
                
            elif mode == "suffix":
                rename_func = patterns.add_suffix
                kwargs = {"suffix": self.suffix_entry.get()}
                
            elif mode == "replace":
                rename_func = patterns.replace_text
                kwargs = {
                    "old_text": self.replace_old.get(),
                    "new_text": self.replace_new.get(),
                    "use_regex": self.replace_regex.get(),
                    "case_sensitive": self.replace_case.get()
                }
                
            elif mode == "number":
                self.preview_number_rename(files)
                return
                
            elif mode == "case":
                rename_func = patterns.change_case
                kwargs = {"case_type": self.case_type.get()}
                
            elif mode == "datetime":
                rename_func = patterns.date_time_name
                kwargs = {
                    "date_format": self.datetime_format.get(),
                    "use_modified_time": self.datetime_modified.get(),
                    "prefix": self.datetime_prefix.get(),
                    "suffix": self.datetime_suffix.get(),
                    "keep_original": self.datetime_keep.get()
                }
                
            elif mode == "remove":
                rename_func = patterns.remove_characters
                kwargs = {
                    "remove_spaces": self.remove_spaces.get(),
                    "remove_special": self.remove_special.get(),
                    "custom_chars": self.remove_custom.get()
                }
                
            else:
                messagebox.showerror(
                    get_text('error', self.lang), 
                    get_text('unknown_mode', self.lang)
                )
                return
            
            # 预览
            self.preview_results = self.renamer.preview_rename(files, rename_func, **kwargs)
            self.display_preview()
            self.rename_button.config(state=tk.NORMAL)
            self.update_status(get_text('status_preview_complete', self.lang).format(len(self.preview_results)))
            
        except Exception as e:
            messagebox.showerror(
                get_text('error', self.lang), 
                get_text('preview_error', self.lang).format(str(e))
            )
    
    def preview_number_rename(self, files: List[Path]):
        """序号重命名的特殊预览处理 - Preview number rename"""
        try:
            results = []
            start = self.number_start.get()
            digits = self.number_digits.get()
            prefix = self.number_prefix.get()
            keep = self.number_keep.get()
            
            for i, file_path in enumerate(files):
                new_name = patterns.number_sequence(
                    file_path, i, start, digits, prefix, keep
                )
                new_path = file_path.parent / new_name
                new_path = self.renamer._resolve_conflict(new_path, file_path)
                results.append((file_path, new_path))
            
            self.preview_results = results
            self.display_preview()
            self.rename_button.config(state=tk.NORMAL)
            self.update_status(get_text('status_preview_complete', self.lang).format(len(results)))
            
        except Exception as e:
            messagebox.showerror(
                get_text('error', self.lang), 
                get_text('preview_error', self.lang).format(str(e))
            )
    
    def display_preview(self):
        """显示预览结果 - Display preview"""
        self.preview_text.delete(1.0, tk.END)
        
        if not self.preview_results:
            no_preview = "No preview results" if self.lang == 'en' else "没有预览结果"
            self.preview_text.insert(tk.END, no_preview)
            return
        
        # 显示对比
        max_len = max(len(old.name) for old, _ in self.preview_results)
        
        for old_path, new_path in self.preview_results:
            old_name = old_path.name
            new_name = new_path.name
            
            # 高亮显示变化
            if old_name != new_name:
                line = f"{old_name:<{max_len}}  →  {new_name}\n"
                self.preview_text.insert(tk.END, line)
            else:
                unchanged = "(no change)" if self.lang == 'en' else "(无变化)"
                line = f"{old_name:<{max_len}}  {unchanged}\n"
                self.preview_text.insert(tk.END, line, "unchanged")
        
        # 配置标签样式
        self.preview_text.tag_config("unchanged", foreground="gray")
    
    def execute_rename(self):
        """执行重命名 - Execute rename"""
        if not self.preview_results:
            messagebox.showwarning(
                get_text('warning', self.lang), 
                "Please preview first" if self.lang == 'en' else "请先预览重命名结果"
            )
            return
        
        # 确认对话框
        result = messagebox.askyesno(
            get_text('confirm', self.lang),
            get_text('confirm_rename', self.lang).format(len(self.preview_results))
        )
        
        if not result:
            return
        
        try:
            success_count, errors = self.renamer.execute_rename(self.preview_results)
            
            # 显示结果
            if errors:
                error_msg = "\n".join(errors[:10])
                if len(errors) > 10:
                    error_msg += f"\n... {len(errors) - 10} more" if self.lang == 'en' else f"\n... 还有 {len(errors) - 10} 个错误"
                messagebox.showwarning(
                    "Partially Complete" if self.lang == 'en' else "部分完成",
                    get_text('rename_partial', self.lang).format(success_count, len(errors), error_msg)
                )
            else:
                messagebox.showinfo(
                    get_text('success', self.lang), 
                    get_text('rename_success', self.lang).format(success_count)
                )
            
            # 刷新列表
            self.refresh_files()
            self.preview_results = []
            self.rename_button.config(state=tk.DISABLED)
            self.preview_text.delete(1.0, tk.END)
            self.update_status(get_text('status_rename_complete', self.lang).format(success_count))
            
        except Exception as e:
            messagebox.showerror(
                get_text('error', self.lang), 
                get_text('rename_error', self.lang).format(str(e))
            )
    
    def undo_operation(self):
        """撤销上次操作 - Undo operation"""
        success, message = self.renamer.undo_last_operation()
        
        if success:
            messagebox.showinfo(get_text('success', self.lang), message)
            self.refresh_files()
            self.update_status(get_text('status_undo_complete', self.lang))
        else:
            messagebox.showwarning(
                "Failed" if self.lang == 'en' else "失败", 
                message
            )
    
    def clear_history(self):
        """清空历史记录 - Clear history"""
        result = messagebox.askyesno(
            get_text('confirm', self.lang), 
            get_text('clear_history_confirm', self.lang)
        )
        if result:
            self.renamer.clear_history()
            messagebox.showinfo(
                get_text('success', self.lang), 
                get_text('history_cleared', self.lang)
            )
            self.update_status(get_text('status_history_cleared', self.lang))
    
    def show_help(self):
        """显示帮助信息 - Show help"""
        help_window = tk.Toplevel(self.root)
        help_window.title(get_text('help_title', self.lang))
        help_window.geometry("600x500")
        
        text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, font=('Arial', 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(1.0, get_text('help_text', self.lang))
        text.config(state=tk.DISABLED)
    
    def update_status(self, message: str):
        """更新状态栏 - Update status"""
        self.statusbar.config(text=message)


def main(lang='en'):
    """主函数 - Main function"""
    root = tk.Tk()
    app = BatchRenamerGUI(root, lang)
    root.mainloop()


if __name__ == "__main__":
    import sys
    lang = sys.argv[1] if len(sys.argv) > 1 else 'en'
    main(lang)
