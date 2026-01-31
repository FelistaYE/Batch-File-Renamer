import re
from pathlib import Path
from datetime import datetime


def add_prefix(file_path: Path, prefix: str) -> str:
    return f"{prefix}{file_path.name}"


def add_suffix(file_path: Path, suffix: str) -> str:
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
    name = file_path.name
    
    if use_regex:
        flags = 0 if case_sensitive else re.IGNORECASE
        new_name = re.sub(old_text, new_text, name, flags=flags)
    else:
        if case_sensitive:
            new_name = name.replace(old_text, new_text)
        else:
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
    stem = file_path.stem
    ext = file_path.suffix.lower()  # 扩展名统一小写
    
    if case_type == "lower":
        new_stem = stem.lower()
    elif case_type == "upper":
        new_stem = stem.upper()
    elif case_type == "title":
        new_stem = stem.title()
    elif case_type == "sentence":
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
    stem = file_path.stem
    ext = file_path.suffix

    if remove_spaces:
        stem = stem.replace(" ", "")

    if remove_special:
        stem = re.sub(r'[^\w\u4e00-\u9fff\-]', '', stem)

    if custom_chars:
        for char in custom_chars:
            stem = stem.replace(char, "")
    
    return f"{stem}{ext}"


def insert_text(
    file_path: Path,
    text: str,
    position: int = 0
) -> str:

    stem = file_path.stem
    ext = file_path.suffix
    
    if position == -1 or position >= len(stem):
        return f"{stem}{text}{ext}"
    elif position == 0:
        return f"{text}{stem}{ext}"
    else:
        new_stem = stem[:position] + text + stem[position:]
        return f"{new_stem}{ext}"


def truncate_name(
    file_path: Path,
    max_length: int = 50,
    from_start: bool = True
) -> str:
    stem = file_path.stem
    ext = file_path.suffix
    
    if len(stem) <= max_length:
        return file_path.name
    
    if from_start:
        new_stem = stem[:max_length]
    else:
        new_stem = stem[-max_length:]
    
    return f"{new_stem}{ext}"
