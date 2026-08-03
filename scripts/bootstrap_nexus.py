from pathlib import Path


FILES = {
    "src/nexus/__init__.py": "",
    "src/nexus/__main__.py": "from nexus.cli import main\n\n\nif __name__ == \"__main__\":\n    main()\n",
    "src/nexus/app/__init__.py": "",
    "src/nexus/core/__init__.py": "from .models import CoreState, Stability, GrowthTag, RunResult\n\n__all__ = [\"CoreState\", \"Stability\", \"GrowthTag\", \"RunResult\"]\n",
    "src/nexus/core/policy/__init__.py": "from .aaa import decide, account, should_accept_ability\n\n__all__ = [\"decide\", \"account\", \"should_accept_ability\"]\n",
    "src/nexus/core/policy/aaa.py": "from nexus.policy.aaa import decide, account, should_accept_ability\n\n__all__ = [\"decide\", \"account\", \"should_accept_ability\"]\n",
    "src/nexus/policy/__init__.py": "from .aaa import decide, account, should_accept_ability\n\n__all__ = [\"decide\", \"account\", \"should_accept_ability\"]\n",
    "src/nexus/policy/aaa.py": "def decide(*args, **kwargs):\n    return {\"decision\": \"allowed\", \"args\": args, \"kwargs\": kwargs}\n\n\ndef account(*args, **kwargs):\n    return {\"accounted\": True, \"args\": args, \"kwargs\": kwargs}\n\n\ndef should_accept_ability(*args, **kwargs):\n    return True\n",
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
