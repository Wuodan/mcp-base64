from fastmcp import FastMCP
from . import utils


app = FastMCP("mcp-base64")


@app.tool()
def encode_file_to_base64(file_path: str) -> str:
    """
    Encodes the file at the given absolute path to a base64 string.
    Requires absolute path; validates existence; rejects path traversal.
    """
    return utils.encode_file_to_base64(file_path)


@app.tool()
def decode_base64_to_file(base64_content: str, file_path: str) -> str:
    """
    Decodes the base64 string to a file at the given absolute path.
    Validates path; creates directories if needed; binary write.
    """
    return utils.decode_base64_to_file(base64_content, file_path)


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run_stdio_async())
