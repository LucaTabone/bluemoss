from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / 'docs'


def main() -> None:
    content = DOCS_DIR.joinpath('index.md').read_text()
    ROOT_DIR.joinpath('README.md').write_text(content)


if __name__ == '__main__':
    main()
