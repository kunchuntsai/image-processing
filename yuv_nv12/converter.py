"""
YUV NV12 Image Converter Module

Converts JPG/PNG images to YUV420 NV12 format.
Reference: https://docs.kernel.org/userspace-api/media/v4l/pixfmt-yuv-planar.html

Python 3.4+ compatible version (no type hints, no f-strings)
"""

from PIL import Image
import numpy as np


class DimensionError(Exception):
    """Raised when image dimensions are not even."""
    pass


def validate_dimensions(width, height):
    """
    Validate that image dimensions are even numbers (required for NV12).

    Args:
        width: Image width
        height: Image height

    Raises:
        DimensionError: If width or height is odd
    """
    if width % 2 != 0 or height % 2 != 0:
        raise DimensionError(
            "Image dimensions must be even numbers. Got {0}x{1}. "
            "Please resize the image to even dimensions.".format(width, height)
        )


def rgb_to_yuv_bt601(r, g, b):
    """
    Convert RGB to YUV using BT.601 standard (most common for JPG/PNG).
    Uses full range (0-255).

    Args:
        r, g, b: RGB color channel arrays (0-255)

    Returns:
        Tuple of (Y, U, V) arrays
    """
    # BT.601 conversion matrix (full range)
    Y = 0.299 * r + 0.587 * g + 0.114 * b
    U = -0.168736 * r - 0.331264 * g + 0.5 * b + 128
    V = 0.5 * r - 0.418688 * g - 0.081312 * b + 128

    # Clip values to valid range
    Y = np.clip(Y, 0, 255).astype(np.uint8)
    U = np.clip(U, 0, 255).astype(np.uint8)
    V = np.clip(V, 0, 255).astype(np.uint8)

    return Y, U, V


def convert_to_nv12(image_path, output_path):
    """
    Convert an image (JPG/PNG) to YUV420 NV12 format.

    NV12 format layout:
    - Y plane: full resolution (width x height)
    - UV plane: interleaved U and V, half resolution (width x height/2)

    Args:
        image_path: Path to input image (JPG/PNG)
        output_path: Path to output YUV file

    Returns:
        Tuple of (width, height) of the converted image

    Raises:
        DimensionError: If image dimensions are not even
        IOError: If input image doesn't exist
        ValueError: If image format is not supported
    """
    # Load image
    try:
        img = Image.open(image_path)
    except IOError:
        raise IOError("Input image not found: {0}".format(image_path))
    except Exception as e:
        raise ValueError("Failed to load image: {0}".format(e))

    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Get dimensions and validate
    width, height = img.size
    validate_dimensions(width, height)

    # Convert to numpy array
    rgb_array = np.array(img)
    r = rgb_array[:, :, 0].astype(np.float32)
    g = rgb_array[:, :, 1].astype(np.float32)
    b = rgb_array[:, :, 2].astype(np.float32)

    # Convert to YUV
    Y, U, V = rgb_to_yuv_bt601(r, g, b)

    # Subsample U and V to create YUV420
    # Take average of 2x2 blocks
    U_sub = U[::2, ::2]  # Take every other row and column
    V_sub = V[::2, ::2]

    # Create NV12 format: Y plane followed by interleaved UV plane
    with open(output_path, 'wb') as f:
        # Write Y plane (full resolution)
        Y.tofile(f)

        # Write interleaved UV plane (half resolution)
        uv_height = height // 2
        uv_width = width // 2
        uv_interleaved = np.empty((uv_height, uv_width * 2), dtype=np.uint8)
        uv_interleaved[:, 0::2] = U_sub
        uv_interleaved[:, 1::2] = V_sub
        uv_interleaved.tofile(f)

    return width, height


def get_file_info(yuv_path):
    """
    Get information about a YUV NV12 file.

    Args:
        yuv_path: Path to YUV file

    Returns:
        Dictionary with file information
    """
    import os
    file_size = os.path.getsize(yuv_path)

    # Calculate possible dimensions
    # NV12 size = width * height * 1.5
    # So: width * height = file_size / 1.5
    pixels = file_size / 1.5

    return {
        'file_size': file_size,
        'total_pixels': int(pixels),
        'format': 'YUV420 NV12'
    }
