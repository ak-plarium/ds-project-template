def __attach_src():
    """
    searches up the directory tree until it research the root and attaches /src to sys.path
    only needs to run in DataBricks
    it assumes the root will always contain ['notebooks', 'src', 'tests']
    """
    from pathlib import Path
    import sys
    import os

    project_root_members = ['notebooks', 'src', 'tests']
    current_path = Path(os.getcwd()).resolve()
    
    for parent in current_path.parents:
        if all((parent / _).exists() for _ in project_root_members):
            path = parent  / 'src'
            sys.path.insert(0, str(path))
            print(f"Added '{path}' to sys.path")
    