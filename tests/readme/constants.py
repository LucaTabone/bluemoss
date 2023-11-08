from pathlib import Path


with open(Path(__file__).parent / 'example.html', "r") as f:
    HTML = f.read()
