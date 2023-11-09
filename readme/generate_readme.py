from os import listdir
from pathlib import Path
from tests.constants import README_EXAMPLE_HTML


def generate_readme_md_file() -> None:
    with open(Path(__file__).parent.parent / 'README.md', 'w') as file:
        file.write(_get_readme_header())
        file.write('\n<br>\n<br>\n<br>\n\n')
        file.write('## example html\n\n')
        file.write('```html\n')
        file.write(README_EXAMPLE_HTML)
        file.write('```\n\n<br>\n<br>\n\n')
        for idx, code in enumerate(_get_python_examples_code()):
            file.write(f'## scraping example {idx+1}\n')
            file.write('```python\n')
            file.write(code)
            file.write('```\n\n<br>\n<br>\n\n')


def _get_readme_header() -> str:
    with open(Path(__file__).parent / 'header.md', 'r') as file:
        return file.read()


def _get_python_examples_code() -> list[str]:
    directory: Path = Path(__file__).parent.parent / 'tests' / 'readme'
    file_paths: list[Path] = sorted(
        [
            directory / file
            for file in listdir(directory)
            if file.startswith('test_example_') and file.endswith('.py')
        ]
    )
    res: list[str] = []
    for path in file_paths:
        with open(path, 'r') as f:
            res.append(f.read())
    return res


if __name__ == '__main__':
    generate_readme_md_file()
