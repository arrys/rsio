from pathlib import Path
import zipfile
import shutil


class TemporaryTemplatedPath:
    def __init__(self, template_file_path: Path | str | None, extraction_path: Path | str, remove_after_completion: bool = True):
        self.template_file_path = Path(template_file_path) if isinstance(template_file_path, str) else template_file_path
        self.extraction_path = extraction_path if isinstance(extraction_path, Path) else Path(extraction_path)
        self.remove_after_completion = remove_after_completion

    def __enter__(self):
        if not self.template_file_path:
            return self.extraction_path
        elif self.template_file_path.suffix == ".git":
            shutil.copytree(self.template_file_path, self.extraction_path)
        elif self.template_file_path.suffix == ".zip":
            with zipfile.ZipFile(self.template_file_path) as zip_file:
                zip_file.extractall(self.extraction_path)
        else:
            raise ValueError(f"Unexpected extension '{self.template_file_path.suffix}'.")
        return self.extraction_path

    def __exit__(self, exc_type, exc_value, traceback):
        if self.remove_after_completion:
            try:
                shutil.rmtree(self.extraction_path)
            except FileNotFoundError:
                pass

class TemporaryPath(TemporaryTemplatedPath):
    def __init__(self, path: Path | str, remove_after_completion: bool = True):
        super().__init__(None, path if isinstance(path, Path) else Path(path), remove_after_completion)
