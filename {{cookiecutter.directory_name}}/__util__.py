def __attach_src():
    """spots if the runtime is in databricks or local
        if it's databricks, we piggy back on the path to the root of the project and add the src as a valid path
        if local, we inform and do nothing
        if neither, we raise a warning
    """
    from pathlib import Path
    import sys
    from importlib.metadata import distributions
    
    modules = [_.metadata['Name'] for _ in distributions()]
    
    if 'databricks-sdk' in modules:
        path = [Path(_).resolve() for _ in sys.path if Path(_).resolve().parts[-1] == '{{cookiecutter.directory_name}}'][0]
        path = path / "src"
        sys.path.insert(0, str(path))
        print(f"added '{path}' to sys.path")
    elif '{{cookiecutter.directory_name}}' in modules:
        print(f"editable version detected, ignoring")
    else:
        from warnings import warn
        warn(f"unidentified runtime: your src path might not be attached to sys.path")