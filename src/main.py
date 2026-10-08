from fs_tools import (
    read_file,
    list_files,
    write_file,
    search_in_file,
)


def main():
    print("=== LLM File Tools ===")

    # 1. List files
    print("\n1. Listing resume files")

    files = list_files("resumes", ".txt")

    for file in files:
        print(file)

    # 2. Read file
    print("\n2. Reading resume")

    result = read_file("resumes/sample.txt")

    if result["success"]:
        print(result["content"])
    else:
        print("Error:", result["error"])

    # 3. Search
    print("\n3. Searching for ASP.NET")

    result = search_in_file(
        "resumes/sample.txt",
        "ASP.NET",
    )

    print("Matches:", result["match_count"])

    for match in result["matches"]:
        print("\nContext:")
        print(match["context"])

    # 4. Write file
    print("\n4. Writing output")

    result = write_file(
        "output/summary.txt",
        "Resume processing completed successfully."
    )

    print(result)


if __name__ == "__main__":
    main()