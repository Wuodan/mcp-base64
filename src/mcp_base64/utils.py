import base64
from pathlib import Path


def encode_file_to_base64(file_path: str) -> str:
    """
    Encodes the file at the given absolute path to a base64 string.
    Requires absolute path; validates existence; rejects path traversal.
    """
    path = Path(file_path)
    if not path.is_absolute():
        raise ValueError("File path must be absolute")
    if ".." in path.parts:
        raise ValueError("Path traversal not allowed")
    if not path.exists() or not path.is_file():
        raise ValueError("File does not exist or is not a file")
    with path.open("rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("ascii")


def decode_base64_to_file(base64_content: str, file_path: str) -> str:
    """
    Decodes the base64 string to a file at the given absolute path.
    Validates path; creates directories if needed; binary write.
    """
    path = Path(file_path)
    if not path.is_absolute():
        raise ValueError("File path must be absolute")
    if ".." in path.parts:
        raise ValueError("Path traversal not allowed")
    try:
        data = base64.b64decode(base64_content.encode("ascii"))
    except Exception as e:
        raise ValueError(f"Invalid base64 content: {e}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(data)
    return f"Decoded to {file_path}"
