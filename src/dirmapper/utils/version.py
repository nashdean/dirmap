from importlib.metadata import version, PackageNotFoundError

def get_package_version(package_name: str) -> str:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Unknown version"
