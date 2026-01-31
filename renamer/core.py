import os
from pathlib import Path
from typing import List, Tuple, Callable
import json
from datetime import datetime


class FileRenamer:
    
    def __init__(self):
        self.history = []
        self.history_file = Path.home() / ".batch_renamer_history.json"
        self._load_history()
    
    def get_files(self, directory: str, pattern: str = "*", recursive: bool = False) -> List[Path]:

        path = Path(directory)
        if not path.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")
        
        if recursive:
            files = list(path.rglob(pattern))
        else:
            files = list(path.glob(pattern))

        return [f for f in files if f.is_file()]
    
    def preview_rename(
        self, 
        files: List[Path], 
        rename_func: Callable,
        **kwargs
    ) -> List[Tuple[Path, Path]]:

        results = []
        for file_path in files:
            new_name = rename_func(file_path, **kwargs)
            new_path = file_path.parent / new_name

            new_path = self._resolve_conflict(new_path, file_path)
            
            results.append((file_path, new_path))
        
        return results
    
    def execute_rename(
        self, 
        rename_list: List[Tuple[Path, Path]],
        save_history: bool = True
    ) -> Tuple[int, List[str]]:

        success_count = 0
        errors = []
        operation_record = {
            "timestamp": datetime.now().isoformat(),
            "operations": []
        }
        
        for old_path, new_path in rename_list:
            try:
                old_path.rename(new_path)
                success_count += 1
                operation_record["operations"].append({
                    "old": str(old_path),
                    "new": str(new_path)
                })
                
            except Exception as e:
                errors.append(f"重命名失败 {old_path.name}: {str(e)}")

        if save_history and success_count > 0:
            self.history.append(operation_record)
            self._save_history()
        
        return success_count, errors
    
    def undo_last_operation(self) -> Tuple[bool, str]:

        if not self.history:
            return False, "没有可撤销的操作"
        
        last_operation = self.history[-1]
        success_count = 0
        errors = []

        for op in reversed(last_operation["operations"]):
            try:
                new_path = Path(op["new"])
                old_path = Path(op["old"])
                
                if new_path.exists():
                    new_path.rename(old_path)
                    success_count += 1
                else:
                    errors.append(f"文件不存在: {new_path.name}")
                    
            except Exception as e:
                errors.append(f"撤销失败 {new_path.name}: {str(e)}")
        
        if success_count > 0:
            self.history.pop()
            self._save_history()
            message = f"成功撤销 {success_count} 个文件"
            if errors:
                message += f"\n失败 {len(errors)} 个"
            return True, message
        else:
            return False, "撤销失败: " + "; ".join(errors)
    
    def _resolve_conflict(self, new_path: Path, original_path: Path) -> Path:
        if new_path == original_path:
            return new_path

        if not new_path.exists():
            return new_path

        stem = new_path.stem
        suffix = new_path.suffix
        parent = new_path.parent
        counter = 1
        
        while new_path.exists() and new_path != original_path:
            new_name = f"{stem}_{counter}{suffix}"
            new_path = parent / new_name
            counter += 1
        
        return new_path
    
    def _load_history(self):
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                    # 只保留最近50条记录
                    self.history = self.history[-50:]
        except Exception:
            self.history = []
    
    def _save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history[-50:], f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def get_history(self, limit: int = 10) -> List[dict]:
        return self.history[-limit:]
    
    def clear_history(self):
        self.history = []
        self._save_history()
