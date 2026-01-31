"""
各种文件重命名模式
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Optional


def add_prefix(file_path: Path, prefix: str) -> str:
    """
    添加前缀
    
    Args:
        file_path: 文件路径
        prefix: 要添加的前缀
        
    Returns:
        新文件名
    """
    return f"{prefix}{file_path.name}"


def add_suffix(file_path: Path, suffix: str) -> str:
    """
    添加后缀（在扩展名之前）
    
    Args:
        file_path: 文件路径
        suffix: 要添加的后缀
        
    Returns:
        新文件名
    """
    stem = file_path.stem
    ext = file_path.suffix
    return f"{stem}{suffix}{ext}"


def replace_text(
    file_path: Path, 
    old_text: str, 
    new_text: str, 
    use_regex: bool = False,
    case_sensitive: bool = True
) -> str:
    """
    替换文本
    
    Args:
        file_path: 文件路径
        old_text: 要替换的文本
        new_text: 新文本
        use_regex: 是否使用正则表达式
        case_sensitive: 是否区分大小写
        
    Returns:
        新文件名
    """
    name = file_path.name
    
    if use_regex:
        flags = 0 if case_sensitive else re.IGNORECASE
        new_name = re.sub(old_text, new_text, name, flags=flags)
    else:
        if case_sensitive:
            new_name = name.replace(old_text, new_text)
        else:
            # 不区分大小写的替换
            pattern = re.compile(re.escape(old_text), re.IGNORECASE)
            new_name = pattern.sub(new_text, name)
    
    return new_name


def number_sequence(
    file_path: Path,
    index: int,
    start: int = 1,
    digits: int = 3,
    prefix: str = "",
    keep_original: bool = False
) -> str:
    """
    序号命名
    
    Args:
        file_path: 文件路径
        index: 当前文件索引
        start: 起始数字
        digits: 数字位数
        prefix: 前缀
        keep_original: 是否保留原文件名
        
    Returns:
        新文件名
    """
    number = start + index
    number_str = str(number).zfill(digits)
    ext = file_path.suffix
    
    if keep_original:
        stem = file_path.stem
        return f"{prefix}{number_str}_{stem}{ext}"
    else:
        return f"{prefix}{number_str}{ext}"


def change_case(
    file_path: Path,
    case_type: str = "lower"
) -> str:
    """
    改变大小写
    
    Args:
        file_path: 文件路径
        case_type: 大小写类型 ('lower', 'upper', 'title', 'sentence')
        
    Returns:
        新文件名
    """
    stem = file_path.stem
    ext = file_path.suffix.lower()  # 扩展名统一小写
    
    if case_type == "lower":
        new_stem = stem.lower()
    elif case_type == "upper":
        new_stem = stem.upper()
    elif case_type == "title":
        new_stem = stem.title()
    elif case_type == "sentence":
        # 首字母大写，其余小写
        new_stem = stem.capitalize()
    else:
        new_stem = stem
    
    return f"{new_stem}{ext}"


def date_time_name(
    file_path: Path,
    date_format: str = "%Y%m%d_%H%M%S",
    use_modified_time: bool = True,
    prefix: str = "",
    suffix: str = "",
    keep_original: bool = False
) -> str:
    """
    使用日期时间命名
    
    Args:
        file_path: 文件路径
        date_format: 日期格式字符串
        use_modified_time: True=使用修改时间, False=使用创建时间
        prefix: 前缀
        suffix: 后缀
        keep_original: 是否保留原文件名
        
    Returns:
        新文件名
    """
    # 获取文件时间
    if use_modified_time:
        timestamp = file_path.stat().st_mtime
    else:
        timestamp = file_path.stat().st_ctime
    
    date_str = datetime.fromtimestamp(timestamp).strftime(date_format)
    ext = file_path.suffix
    
    if keep_original:
        stem = file_path.stem
        return f"{prefix}{date_str}_{stem}{suffix}{ext}"
    else:
        return f"{prefix}{date_str}{suffix}{ext}"


def remove_characters(
    file_path: Path,
    remove_spaces: bool = False,
    remove_special: bool = False,
    custom_chars: str = ""
) -> str:
    """
    删除特定字符
    
    Args:
        file_path: 文件路径
        remove_spaces: 是否删除空格
        remove_special: 是否删除特殊字符
        custom_chars: 自定义要删除的字符
        
    Returns:
        新文件名
    """
    stem = file_path.stem
    ext = file_path.suffix
    
    # 删除空格
    if remove_spaces:
        stem = stem.replace(" ", "")
    
    # 删除特殊字符（保留字母、数字、中文、下划线、连字符）
    if remove_special:
        stem = re.sub(r'[^\w\u4e00-\u9fff\-]', '', stem)
    
    # 删除自定义字符
    if custom_chars:
        for char in custom_chars:
            stem = stem.replace(char, "")
    
    return f"{stem}{ext}"


def insert_text(
    file_path: Path,
    text: str,
    position: int = 0
) -> str:
    """
    在指定位置插入文本
    
    Args:
        file_path: 文件路径
        text: 要插入的文本
        position: 插入位置（0=开头，-1=扩展名前）
        
    Returns:
        新文件名
    """
    stem = file_path.stem
    ext = file_path.suffix
    
    if position == -1 or position >= len(stem):
        # 在扩展名前插入
        return f"{stem}{text}{ext}"
    elif position == 0:
        # 在开头插入
        return f"{text}{stem}{ext}"
    else:
        # 在指定位置插入
        new_stem = stem[:position] + text + stem[position:]
        return f"{new_stem}{ext}"


def truncate_name(
    file_path: Path,
    max_length: int = 50,
    from_start: bool = True
) -> str:
    """
    截断文件名
    
    Args:
        file_path: 文件路径
        max_length: 最大长度
        from_start: True=从开头截断，False=从结尾截断
        
    Returns:
        新文件名
    """
    stem = file_path.stem
    ext = file_path.suffix
    
    if len(stem) <= max_length:
        return file_path.name
    
    if from_start:
        new_stem = stem[:max_length]
    else:
        new_stem = stem[-max_length:]
    
    return f"{new_stem}{ext}"
