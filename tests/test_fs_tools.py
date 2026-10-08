from pathlib import Path

from src.fs_tools import (
    read_file,
    list_files,
    write_file,
    search_in_file,
)


def test_write_and_read():
    file_path = "output/test.txt"

    write_result = write_file(
        file_path,
        "Python developer with .NET experience."
    )

    assert write_result["success"] is True

    read_result = read_file(file_path)

    assert read_result["success"] is True
    assert "Python developer" in read_result["content"]


def test_search():
    file_path = "output/search_test.txt"

    write_file(
        file_path,
        "Python developer\n.NET developer\nPython developer"
    )

    result = search_in_file(
        file_path,
        "python",
    )

    assert result["success"] is True
    assert result["match_count"] == 2


def test_list_files():
    files = list_files("output", ".txt")

    assert isinstance(files, list)