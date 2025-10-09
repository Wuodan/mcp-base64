from fastmcp import FastMCP
from pydantic import Field
from typing import Annotated
from . import utils


app = FastMCP("mcp-base64")


@app.tool(
    name="encode_file_to_base64",
    description="Encodes the file at the given absolute path to a base64 string"
)
def encode_file_to_base64(
        file_path: Annotated[str, Field(description="Absolute path to the file to encode (must use absolute path; no traversal allowed)")]
) -> str:
    return utils.encode_file_to_base64(file_path)


@app.tool(
    name="decode_base64_to_file",
    description="Decodes the base64 string to a file at the given absolute path"
)
def decode_base64_to_file(
        base64_content: Annotated[str, Field(description="The base64 encoded content to decode")],
        file_path: Annotated[str, Field(description="Absolute path where the decoded file will be written (must use absolute path; no traversal allowed)")]
) -> str:
    return utils.decode_base64_to_file(base64_content, file_path)


if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run_stdio_async())
