"""
YUV NV12 Reader and Visualizer Module

Reads YUV420 NV12 binary files and converts them back to displayable images.
"""

import numpy as np
from PIL import Image
from typing import Tuple


def yuv_to_rgb_bt601(Y: np.ndarray, U: np.ndarray, V: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convert YUV to RGB using BT.601 standard (inverse of conversion).
    Uses full range (0-255).

    Args:
        Y, U, V: YUV color channel arrays

    Returns:
        Tuple of (R, G, B) arrays
    """
    # Convert to float for calculation
    Y = Y.astype(np.float32)
    U = U.astype(np.float32) - 128
    V = V.astype(np.float32) - 128

    # BT.601 inverse conversion
    R = Y + 1.402 * V
    G = Y - 0.344136 * U - 0.714136 * V
    B = Y + 1.772 * U

    # Clip values to valid range
    R = np.clip(R, 0, 255).astype(np.uint8)
    G = np.clip(G, 0, 255).astype(np.uint8)
    B = np.clip(B, 0, 255).astype(np.uint8)

    return R, G, B


def read_nv12(yuv_path: str, width: int, height: int) -> Image.Image:
    """
    Read a YUV420 NV12 binary file and convert to RGB image.

    NV12 format layout:
    - Y plane: full resolution (width x height)
    - UV plane: interleaved U and V, half resolution (width x height/2)

    Args:
        yuv_path: Path to YUV NV12 file
        width: Image width (must be even)
        height: Image height (must be even)

    Returns:
        PIL Image in RGB format

    Raises:
        ValueError: If dimensions are invalid or file size doesn't match
        FileNotFoundError: If YUV file doesn't exist
    """
    import os

    # Validate dimensions
    if width % 2 != 0 or height % 2 != 0:
        raise ValueError(f"Dimensions must be even numbers. Got {width}x{height}")

    # Calculate expected file size
    expected_size = int(width * height * 1.5)  # Y + UV/2

    # Check file exists and size
    if not os.path.exists(yuv_path):
        raise FileNotFoundError(f"YUV file not found: {yuv_path}")

    file_size = os.path.getsize(yuv_path)
    if file_size != expected_size:
        raise ValueError(
            f"File size mismatch. Expected {expected_size} bytes for {width}x{height}, "
            f"but got {file_size} bytes. Please verify the dimensions are correct."
        )

    # Read binary file
    with open(yuv_path, 'rb') as f:
        # Read Y plane (full resolution)
        y_size = width * height
        Y = np.frombuffer(f.read(y_size), dtype=np.uint8).reshape((height, width))

        # Read interleaved UV plane (half resolution)
        uv_height = height // 2
        uv_width = width // 2
        uv_size = uv_width * uv_height * 2
        uv_data = np.frombuffer(f.read(uv_size), dtype=np.uint8).reshape((uv_height, uv_width * 2))

        # De-interleave UV
        U_sub = uv_data[:, 0::2]
        V_sub = uv_data[:, 1::2]

    # Upsample U and V to full resolution
    # Repeat each pixel in 2x2 blocks
    U = np.repeat(np.repeat(U_sub, 2, axis=0), 2, axis=1)
    V = np.repeat(np.repeat(V_sub, 2, axis=0), 2, axis=1)

    # Convert YUV to RGB
    R, G, B = yuv_to_rgb_bt601(Y, U, V)

    # Create RGB image
    rgb_array = np.stack([R, G, B], axis=2)
    img = Image.fromarray(rgb_array, 'RGB')

    return img


def visualize_nv12(yuv_path: str, width: int, height: int, output_path: str = None, show: bool = True) -> Image.Image:
    """
    Visualize a YUV NV12 file by converting to RGB and optionally saving/displaying.

    Args:
        yuv_path: Path to YUV NV12 file
        width: Image width
        height: Image height
        output_path: Optional path to save the RGB image
        show: Whether to display the image (requires display)

    Returns:
        PIL Image in RGB format
    """
    img = read_nv12(yuv_path, width, height)

    if output_path:
        img.save(output_path)
        print(f"Saved RGB image to: {output_path}")

    if show:
        try:
            img.show()
        except Exception as e:
            print(f"Could not display image: {e}")
            print("Image data is still available but display failed.")

    return img


def get_nv12_info(yuv_path: str) -> dict:
    """
    Get information about a YUV NV12 file.

    Args:
        yuv_path: Path to YUV file

    Returns:
        Dictionary with file information
    """
    import os

    if not os.path.exists(yuv_path):
        raise FileNotFoundError(f"YUV file not found: {yuv_path}")

    file_size = os.path.getsize(yuv_path)

    # Calculate total pixels
    # NV12 size = width * height * 1.5
    total_pixels = file_size / 1.5

    # Suggest possible dimensions (common aspect ratios)
    possible_dims = []
    for width in range(2, 10000, 2):  # Even numbers only
        height = total_pixels / width
        if height == int(height) and height % 2 == 0:
            possible_dims.append((width, int(height)))
            if len(possible_dims) >= 10:  # Limit suggestions
                break

    return {
        'file_path': yuv_path,
        'file_size': file_size,
        'total_pixels': int(total_pixels),
        'format': 'YUV420 NV12',
        'suggested_dimensions': possible_dims[:5] if possible_dims else []
    }
