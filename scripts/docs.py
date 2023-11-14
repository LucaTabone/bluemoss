from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / 'docs'


def main() -> None:
    content = ROOT_DIR.joinpath('README.md').read_text()
    DOCS_DIR.joinpath('index.md').write_text(content)


if __name__ == '__main__':
    main()
