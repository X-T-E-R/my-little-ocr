import pathlib
import git
from pathlib import Path
from git import RemoteProgress
from git.exc import GitCommandError
from tqdm import tqdm

class ProgressPrinter(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = None

    def update(self, op_code, cur_count, max_count=None, message=''):
        if self.pbar is None and max_count:
            self.pbar = tqdm(total=max_count, unit='objects', leave=False)
        
        if self.pbar:
            self.pbar.update(cur_count - self.pbar.n)
        
        if message:
            self.pbar.set_description(f"{message}")

    def close(self):
        if self.pbar:
            self.pbar.close()

def check_install(exe_path:str):
    return Path(exe_path).exists()

def install():
    # 获取当前文件所在的目录
    current_dir = pathlib.Path(__file__).parent

    exe_path = current_dir / 'wxocr-binary' / 'WeChatOCR.exe'
    if check_install(exe_path):
        print(f'WeChatOCR.exe 已存在: {exe_path}')
        return
    
    # 定义目标子模块的路径
    submodule_path = current_dir / 'wxocr-binary'

    repo_url = 'https://github.com/Antonoko/wxocr-binary'

    progress = ProgressPrinter()

    try:
        if submodule_path.exists() and submodule_path.is_dir():
            # 如果目录已经存在，则尝试更新
            repo = git.Repo(submodule_path)
            print(f'仓库已存在，正在更新: {submodule_path}')
            repo.remotes.origin.pull(progress=progress)
            progress.close()
        else:
            # 如果目录不存在，则克隆仓库
            print(f'目录不存在，正在克隆仓库到: {submodule_path}')
            git.Repo.clone_from(repo_url, submodule_path, progress=progress)
            progress.close()

        print(f'操作成功！仓库位于: {submodule_path}')

    except GitCommandError as e:
        print(f'Git 操作失败: {e}')
    except Exception as e:
        print(f'发生错误: {e}')
