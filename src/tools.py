from datetime import datetime
import src.config  # noqa: F401

import os
import uuid


import httpx
from pydantic import BaseModel
from bs4 import BeautifulSoup
import duckdb
from langchain_core.language_models import BaseChatModel
from html_to_markdown import convert
import sqlglot
from langchain.tools import tool


DDB_BASE_URL = "https://duckdb.org"
DDB_SITEMAP_URL = f"{DDB_BASE_URL}/sitemap"

DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
)

CONTENT_DIR = os.path.join(
    DATA_DIR,
    "content",
)


RUN_ID = datetime.now().strftime("%Y%m%dT%H%M%S")

print(f"Tools module initialized with RUN_ID: {RUN_ID}")

class ListFilesSchema(BaseModel):
    """Schema for listing files tool."""
    filter: str

@tool(
    "list_files",
    description="List all files available, along with their sizes, in the data directory. This will help you know what files are available to analyze (query), read directly or update. Optionally, provide a filter string to only list files that contain that string in their filename (set it as an empty string to list all files).",
    args_schema=ListFilesSchema
)
def list_files(filter: str = "") -> str:
    try:
        text = ""

        for root, _, filenames in os.walk(DATA_DIR):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, os.path.join(DATA_DIR, ".."))
                size = os.path.getsize(file_path)

                if filter and len(filter) > 0 and filter.lower() not in filename.lower():
                    continue

                if any(
                    filename.lower().endswith(_ext)
                    for _ext in [".parquet", ".csv"]
                ):
                    text += f"- {rel_path} ({size} bytes) [Queriable using DuckDB]\n"

                else:
                    text += f"- {rel_path} ({size} bytes) [Readable/Updatable]\n"

        return text

    except FileNotFoundError:
        return f"Error: Directory '{DATA_DIR}' does not exist."

class WriteFileSchema(BaseModel):
    """Schema for writing a file tool."""
    filename: str
    content: str

@tool(
    "write_file",
    description="Write content to a file in the data directory. Provide the filename and content as input.",
    args_schema=WriteFileSchema
)
def write_file(filename: str, content: str) -> str:
    try:
        os.makedirs(CONTENT_DIR, exist_ok=True)

        file_path = os.path.join(CONTENT_DIR, filename)

        if os.path.exists(file_path):
            return f"Error: File '{filename}' already exists. Aborting to prevent overwrite."

        with open(file_path, "w") as f:
            f.write(content)

        return f"File '{filename}' written successfully."

    except Exception as e:
        return f"Error: Could not write file '{filename}': {str(e)}"

class ReadFileSchema(BaseModel):
    """Schema for reading a file tool."""
    filename: str

@tool(
    "read_file",
    description="Read content from a file in the data directory. Provide the filename as input.",
    args_schema=ReadFileSchema
)
def read_file(filename: str) -> str:
    try:
        os.makedirs(CONTENT_DIR, exist_ok=True)

        file_path = os.path.join(CONTENT_DIR, filename)

        if not os.path.exists(file_path):
            return f"File '{filename}' does not exist."

        with open(file_path, "r") as f:
            content = f.read()

        return content

    except Exception as e:
        return f"Error: Could not read file '{filename}': {str(e)}"

class UpdateFileSchema(BaseModel):
    """Schema for updating a file tool."""
    filename: str
    old_str: str
    new_str: str
    replace_all: bool

@tool(
    "update_file",
    description="Update content of a file in the data directory. Provide the filename and new content as input.",
    args_schema=UpdateFileSchema
)
def update_file(filename: str, old_str: str, new_str: str, replace_all: bool = True) -> str:
    try:
        os.makedirs(CONTENT_DIR, exist_ok=True)

        file_path = os.path.join(CONTENT_DIR, filename)

        if not os.path.exists(file_path):
            return f"File '{filename}' does not exist."

        with open(file_path, "r") as f:
            current_content = f.read()

        if replace_all:
            updated_content = current_content.replace(old_str, new_str)
        
        else:
            updated_content = current_content.replace(old_str, new_str, 1)

        with open(file_path, "w") as f:
            f.write(updated_content)

        return f"File '{filename}' updated successfully, replaced {'all occurrences' if replace_all else 'first occurrence'}"

    except Exception as e:
        return f"Error: Could not update file '{filename}': {str(e)}"

class ValidateSQLSchema(BaseModel):
    """Schema for validating SQL tool."""
    sql: str

@tool(
    "validate_sql",
    description="""Useful for validating DuckDB SQL syntax.""",
    args_schema=ValidateSQLSchema
)
def validate_sql(sql: str) -> str:
    try:
        sqlglot.parse(sql, read="duckdb")
        return "Valid DuckDB SQL"

    except sqlglot.ParseError as e:
        return f"Error: Invalid SQL, here's the error:\n{str(e)}"

class ExecuteSQLSchema(BaseModel):
    """Schema for executing SQL tool."""
    sql: str

@tool(
    "execute_sql",
    description="""Execute a DuckDB SQL query on an in-memory database and return the results as a string. The SQL query should be provided as input.""",
    args_schema=ExecuteSQLSchema
)
def execute_sql(sql: str) -> str:
    try:
        db_path = f"/tmp/agent-ctx__{RUN_ID}.db"

        con = duckdb.connect(
            db_path,
            config={
                "allow_unsigned_extensions": "true",
                "temp_directory": f"/tmp/agent-ctx-tmp/{RUN_ID}",
            }
        )

        con.install_extension("httpfs")
        con.load_extension("httpfs")

        # Escape newlines in the SQL in case double \\n are passed
        sql = sql.replace("\\n", "\n")

        print(f"Executing SQL:\n{sql}")

        result = con.execute(sql).fetchall()
        con.close()

        if not result:
            return "Query executed successfully, but returned no results."

        # Format the results as a string
        result_str = "\n".join([", ".join(map(str, row)) for row in result])
        return result_str

    except duckdb.Error as e:
        if "No files found" in str(e):
            return "Error: Could not execute SQL, one or more queried fiels were not found! Please verify the file paths used (`FROM` clauses in the query) to ensure they are queriable using the `list_files` tool to check available files."

        return f"Error: Could not execute SQL\n{str(e)}\nPlease, validate the SQL syntax before executing, check table and column names, and ensure the SQL is compatible with DuckDB."


class ReadDocsSchema(BaseModel):
    """Schema for reading DuckDB documentation tool."""
    path: str

@tool(
    "read_docs",
    description="""Perform a web request to read DuckDB documentation pages. Optional path parameter can be provided to specify a specific page to read. If no path or empty is provided, the "/sitemap" page will be read.""",
    args_schema=ReadDocsSchema
)
async def read_docs(
    path: str | None = None
) -> str:
    async with httpx.AsyncClient(
        base_url=DDB_BASE_URL,
        follow_redirects=True,
    ) as client:
        print(f"Fetching DuckDB docs page: {path or '/sitemap'}")

        r = await client.get(
            path or "/sitemap",
            follow_redirects=True,
        )

        if r.status_code == 404:
            return "Error: Page not found (404), use the '/sitemap' to find valid pages."

        if r.status_code >= 400:
            return f"Error: Received status code {r.status_code}"

        # Check for canonical URL in HTML
        soup = BeautifulSoup(r.text, 'html.parser')
        canonical = soup.find('link', rel='canonical')
        
        if canonical and canonical.get('href'):
            canonical_url = canonical['href']
            r = await client.get(canonical_url) # type: ignore

        return convert(r.text)


def get_tools():
    return [
        list_files,
        write_file,
        read_file,
        update_file,
        validate_sql,
        execute_sql,
        read_docs,
    ]


def bind_tools(llm: BaseChatModel):
    return llm.bind_tools(
        tools=get_tools()
    )
