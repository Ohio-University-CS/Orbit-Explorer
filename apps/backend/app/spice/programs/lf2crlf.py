from pathlib import Path

file_path = Path(r"C:\Users\Jim\Documents\Classes\CS3560\Orbit-Explorer\apps\backend\app\spice\kernels\pck\pck00011.tpc")

text = file_path.read_text()
file_path.write_text(text.replace("\n", "\r\n"))

print(f"Fixed line endings: {file_path}")
