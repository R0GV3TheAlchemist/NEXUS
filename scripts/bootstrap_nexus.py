from pathlib import Path


FILES = {
    "src/nexus/__init__.py": "",
    "src/nexus/app/__init__.py": "",
    "src/nexus/policy/__init__.py": "",
    "src/nexus/accounting/__init__.py": "",
    "src/nexus/sim/__init__.py": "",
    "src/nexus/domains/__init__.py": "",
}


def ensure_file(path: str, content: str = "") -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(content, encoding="utf-8")


def main() -> None:
    for path, content in FILES.items():
        ensure_file(path, content)
    print("NEXUS bootstrap complete")


if __name__ == "__main__":
    main()
