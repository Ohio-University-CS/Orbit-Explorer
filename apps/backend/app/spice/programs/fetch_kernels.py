from pathlib import Path
import requests

CURRENT_DIR = Path(__file__).parent
KERNEL_ROOT = CURRENT_DIR.parent / "kernels"

# Minimal kernels for Earth, Moon, Sun calculations
KERNELS = {
    "lsk": [
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls",
    ],
    "pck": [
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_1962_250826_2125_combined.bpc",
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00011.tpc",
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_fixed.tf",
    ],
    "spk": [
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de432s.bsp",
    ],
    "fk": [
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/planets/earth_assoc_itrf93.tf",
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/planets/earth_assoc_itrf93.tf",
    ]
    # Optional: add FK, DSK URLs here
}


def download_kernel(url: str, base_folder: Path, kernel_type: str):
    """
    Download a kernel while preserving subdirectories from the remote URL.
    """
    # Try to preserve subdirectory structure after kernel type
    path_parts = Path(url).parts
    try:
        type_index = path_parts.index(kernel_type)
        relative_path = Path(*path_parts[type_index + 1:])
    except ValueError:
        relative_path = Path(url).name  # fallback: just the file name

    local_file = base_folder / kernel_type / relative_path
    local_file.parent.mkdir(parents=True, exist_ok=True)

    if not local_file.exists():
        print(f"Downloading {url} → {local_file}")
        r = requests.get(url)
        r.raise_for_status()
        local_file.write_bytes(r.content)
    else:
        print(f"Already exists: {local_file}")

    return local_file

def download_all_kernels():
    """
    Download all kernels to KERNEL_ROOT, preserving subdirectories.
    Does NOT load them into SPICE.
    """
    for kernel_type, urls in KERNELS.items():
        for url in urls:
            download_kernel(url, KERNEL_ROOT, kernel_type)

    print("All kernels downloaded. Loading is optional and done separately.")

def load_kernel(file_path: Path):
    """
    Load a SPICE kernel into the kernel pool.
    """
    import spiceypy as sp
    sp.furnsh(str(file_path))
    print(f"Loaded {file_path}")

def unload_all_kernels():
    """
    Clear the SPICE kernel pool.
    """
    import spiceypy as sp
    sp.kclear()
    print("Kernel pool cleared.")

# Example usage
if __name__ == "__main__":
    download_all_kernels()
    # Later, when you need to compute:
    # import spiceypy as sp
    # load_kernel(KERNEL_ROOT / "lsk/naif0012.tls")
    # load_kernel(KERNEL_ROOT / "spk/planets/de432s.bsp")
    # load_kernel(my_custom_site_spk)
