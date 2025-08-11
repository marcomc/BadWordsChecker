import os
import sys
from contextlib import contextmanager
import shutil

@contextmanager
def silence_stderr():
    """A context manager to temporarily redirect stderr."""
    new_target = open(os.devnull, "w")
    old_target, sys.stderr = sys.stderr, new_target
    try:
        yield new_target
    finally:
        sys.stderr = old_target
        new_target.close()

def command_exists(command: str) -> bool:
    """Check if a command exists on the system."""
    return shutil.which(command) is not None
