import shutil

def command_exists(command: str) -> bool:
    """Check if a command exists on the system."""
    return shutil.which(command) is not None
