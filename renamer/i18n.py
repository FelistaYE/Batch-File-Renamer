"""
Language configuration for the application
"""

# Supported languages
LANGUAGES = {
    'en': 'English',
    'zh': '中文'
}

# Translations
TRANSLATIONS = {
    'en': {
        # Window
        'window_title': 'Batch File Renamer v1.0',
        
        # Toolbar
        'select_directory': '📁 Select Directory (Ctrl+O)',
        'refresh': '🔄 Refresh',
        'preview': '👁 Preview (Ctrl+P)',
        'execute_rename': '✅ Execute Rename (Ctrl+R)',
        'undo': '↶ Undo Last Operation (Ctrl+Z)',
        'clear_history': '🗑 Clear History',
        'help': '❓ Help',
        
        # File list
        'file_list': 'File List',
        'file_type': 'File Type:',
        'include_subdirs': 'Include Subdirectories',
        'original_files': 'Original Files',
        'preview_comparison': 'Preview Comparison',
        'file_count': 'Files: {}',
        
        # Rename modes
        'rename_options': 'Rename Options',
        'rename_mode': 'Rename Mode:',
        'mode_prefix': 'Add Prefix',
        'mode_suffix': 'Add Suffix',
        'mode_replace': 'Text Replace',
        'mode_number': 'Number Sequence',
        'mode_case': 'Case Conversion',
        'mode_datetime': 'Date/Time',
        'mode_remove': 'Remove Characters',
        'mode_insert': 'Insert Text',
        
        # Prefix options
        'prefix_settings': 'Prefix Settings',
        'prefix': 'Prefix:',
        
        # Suffix options
        'suffix_settings': 'Suffix Settings',
        'suffix': 'Suffix:',
        
        # Replace options
        'replace_settings': 'Replace Settings',
        'find': 'Find:',
        'replace_with': 'Replace with:',
        'use_regex': 'Use Regular Expression',
        'case_sensitive': 'Case Sensitive',
        
        # Number options
        'number_settings': 'Number Settings',
        'start_number': 'Start Number:',
        'number_digits': 'Digits:',
        'keep_original': 'Keep Original Name',
        
        # Case options
        'case_settings': 'Case Settings',
        'lowercase': 'All Lowercase',
        'uppercase': 'All Uppercase',
        'titlecase': 'Title Case',
        'sentencecase': 'Sentence Case',
        
        # DateTime options
        'datetime_settings': 'Date/Time Settings',
        'date_format': 'Date Format:',
        'use_modified_time': 'Use Modified Time',
        'use_creation_time': 'Use Creation Time',
        
        # Remove options
        'remove_settings': 'Remove Characters Settings',
        'remove_spaces': 'Remove All Spaces',
        'remove_special': 'Remove Special Characters',
        'custom_remove': 'Custom Characters to Remove:',
        
        # Insert options
        'insert_settings': 'Insert Text Settings',
        'insert_text': 'Text to Insert:',
        'insert_position': 'Position:',
        'position_start': 'Start',
        'position_end': 'End',
        
        # Status messages
        'status_ready': 'Ready',
        'status_directory_selected': 'Directory selected: {}',
        'status_files_found': 'Found {} files',
        'status_preview_complete': 'Preview complete, {} files',
        'status_rename_complete': 'Rename complete: {} successful',
        'status_undo_complete': 'Undo complete',
        'status_history_cleared': 'History cleared',
        
        # Dialog messages
        'warning': 'Warning',
        'error': 'Error',
        'success': 'Success',
        'confirm': 'Confirm',
        'info': 'Information',
        
        'no_directory': 'Please select a directory first',
        'no_files': 'Please select directory and files',
        'confirm_rename': 'Rename {} files?\nThis operation can be undone.',
        'rename_success': 'Successfully renamed {} files',
        'rename_partial': 'Successfully renamed {} files\nFailed {}: \n{}',
        'undo_success': '{}',
        'undo_fail': '{}',
        'clear_history_confirm': 'Clear all history?',
        'history_cleared': 'History cleared',
        'refresh_error': 'Failed to refresh file list: {}',
        'preview_error': 'Preview failed: {}',
        'rename_error': 'Rename failed: {}',
        'unknown_mode': 'Unknown rename mode',
        
        # Help text
        'help_title': 'Help',
        'help_text': '''
Batch File Renamer - Help

Shortcuts:
  Ctrl+O: Select Directory
  Ctrl+P: Preview Rename
  Ctrl+R: Execute Rename
  Ctrl+Z: Undo Last Operation

Rename Modes:
  • Add Prefix: Add text at the beginning
  • Add Suffix: Add text before extension
  • Text Replace: Replace specified text
  • Number Sequence: Rename with sequential numbers
  • Case Conversion: Convert filename case
  • Date/Time: Name using file timestamp
  • Remove Characters: Remove spaces, special chars
  • Insert Text: Insert text at position

Usage Steps:
  1. Click "Select Directory"
  2. Choose file type and subdirectory option
  3. Select files in the list
  4. Choose rename mode and set parameters
  5. Click "Preview" to see results
  6. Click "Execute Rename" after confirmation

Notes:
  • Always preview before executing
  • Operations can be undone
  • Program handles name conflicts automatically
  • Backup important files first
        ''',
    },
    'zh': {
        # Window
        'window_title': '批量文件重命名工具 v1.0',
        
        # Toolbar
        'select_directory': '📁 选择目录 (Ctrl+O)',
        'refresh': '🔄 刷新',
        'preview': '👁 预览 (Ctrl+P)',
        'execute_rename': '✅ 执行重命名 (Ctrl+R)',
        'undo': '↶ 撤销上次操作 (Ctrl+Z)',
        'clear_history': '🗑 清空历史',
        'help': '❓ 帮助',
        
        # File list
        'file_list': '文件列表',
        'file_type': '文件类型:',
        'include_subdirs': '包含子目录',
        'original_files': '原始文件',
        'preview_comparison': '预览对比',
        'file_count': '文件数: {}',
        
        # Rename modes
        'rename_options': '重命名选项',
        'rename_mode': '重命名模式:',
        'mode_prefix': '添加前缀',
        'mode_suffix': '添加后缀',
        'mode_replace': '文本替换',
        'mode_number': '序号命名',
        'mode_case': '大小写转换',
        'mode_datetime': '日期时间',
        'mode_remove': '删除字符',
        'mode_insert': '插入文本',
        
        # Prefix options
        'prefix_settings': '前缀设置',
        'prefix': '前缀:',
        
        # Suffix options
        'suffix_settings': '后缀设置',
        'suffix': '后缀:',
        
        # Replace options
        'replace_settings': '替换设置',
        'find': '查找:',
        'replace_with': '替换为:',
        'use_regex': '使用正则表达式',
        'case_sensitive': '区分大小写',
        
        # Number options
        'number_settings': '序号设置',
        'start_number': '起始数字:',
        'number_digits': '数字位数:',
        'keep_original': '保留原文件名',
        
        # Case options
        'case_settings': '大小写设置',
        'lowercase': '全部小写',
        'uppercase': '全部大写',
        'titlecase': '首字母大写',
        'sentencecase': '句首大写',
        
        # DateTime options
        'datetime_settings': '日期时间设置',
        'date_format': '日期格式:',
        'use_modified_time': '使用修改时间',
        'use_creation_time': '使用创建时间',
        
        # Remove options
        'remove_settings': '删除字符设置',
        'remove_spaces': '删除所有空格',
        'remove_special': '删除特殊字符',
        'custom_remove': '自定义删除字符:',
        
        # Insert options
        'insert_settings': '插入文本设置',
        'insert_text': '插入文本:',
        'insert_position': '插入位置:',
        'position_start': '开头',
        'position_end': '结尾',
        
        # Status messages
        'status_ready': '就绪',
        'status_directory_selected': '已选择目录: {}',
        'status_files_found': '找到 {} 个文件',
        'status_preview_complete': '预览完成，共 {} 个文件',
        'status_rename_complete': '重命名完成: 成功 {} 个',
        'status_undo_complete': '已撤销上次操作',
        'status_history_cleared': '历史记录已清空',
        
        # Dialog messages
        'warning': '警告',
        'error': '错误',
        'success': '成功',
        'confirm': '确认',
        'info': '信息',
        
        'no_directory': '请先选择目录',
        'no_files': '请先选择目录和文件',
        'confirm_rename': '确定要重命名 {} 个文件吗？\n此操作可以撤销。',
        'rename_success': '成功重命名 {} 个文件',
        'rename_partial': '成功重命名 {} 个文件\n失败 {} 个:\n{}',
        'undo_success': '{}',
        'undo_fail': '{}',
        'clear_history_confirm': '确定要清空所有历史记录吗？',
        'history_cleared': '历史记录已清空',
        'refresh_error': '刷新文件列表失败: {}',
        'preview_error': '预览失败: {}',
        'rename_error': '重命名失败: {}',
        'unknown_mode': '未知的重命名模式',
        
        # Help text
        'help_title': '帮助',
        'help_text': '''
批量文件重命名工具 - 使用帮助

快捷键:
  Ctrl+O: 选择目录
  Ctrl+P: 预览重命名
  Ctrl+R: 执行重命名
  Ctrl+Z: 撤销上次操作

重命名模式:
  • 添加前缀: 在文件名开头添加文本
  • 添加后缀: 在文件名结尾（扩展名前）添加文本
  • 文本替换: 替换文件名中的指定文本
  • 序号命名: 按序号重新命名文件
  • 大小写转换: 转换文件名的大小写
  • 日期时间: 使用文件时间戳命名
  • 删除字符: 删除空格、特殊字符等
  • 插入文本: 在指定位置插入文本

使用步骤:
  1. 点击"选择目录"选择要处理的文件夹
  2. 选择文件类型和是否包含子目录
  3. 在文件列表中选择要重命名的文件
  4. 选择重命名模式并设置参数
  5. 点击"预览"查看效果
  6. 确认后点击"执行重命名"

注意事项:
  • 重命名前请务必预览
  • 可随时撤销操作
  • 程序会自动处理文件名冲突
  • 建议在重要文件操作前先备份
        ''',
    }
}

def get_text(key: str, lang: str = 'en') -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)
