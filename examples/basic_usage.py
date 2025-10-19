#!/usr/bin/env python3
"""
Basic usage examples for YUV NV12 converter.

This script demonstrates how to use the yuv_nv12 package in Python code.
"""

import os

from yuv_nv12 import convert_to_nv12, read_nv12, visualize_nv12, DimensionError


def example_convert():
    """Example: Convert an image to YUV NV12."""
    print("=" * 60)
    print("Example 1: Converting an image to YUV NV12")
    print("=" * 60)

    input_image = 'input.jpg'  # Replace with your image path
    output_yuv = 'output.yuv'

    try:
        width, height = convert_to_nv12(input_image, output_yuv)
        print(f"✓ Converted {input_image} to YUV NV12")
        print(f"  Dimensions: {width}x{height}")
        print(f"  Output: {output_yuv}")
    except FileNotFoundError:
        print(f"Note: {input_image} not found. Create an image file first.")
    except DimensionError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def example_read():
    """Example: Read a YUV NV12 file and convert to RGB."""
    print("\n" + "=" * 60)
    print("Example 2: Reading a YUV NV12 file")
    print("=" * 60)

    yuv_file = 'output.yuv'
    width, height = 1920, 1080  # Must match original dimensions

    try:
        # Read YUV and get PIL Image
        img = read_nv12(yuv_file, width, height)
        print(f"✓ Read YUV file: {yuv_file}")
        print(f"  Image size: {img.size}")
        print(f"  Image mode: {img.mode}")

        # You can now use the PIL Image object
        # img.save('restored.png')
        # img.show()

    except FileNotFoundError:
        print(f"Note: {yuv_file} not found. Convert an image first.")
    except Exception as e:
        print(f"Error: {e}")


def example_visualize():
    """Example: Visualize YUV NV12 file (read, save, and optionally display)."""
    print("\n" + "=" * 60)
    print("Example 3: Visualizing a YUV NV12 file")
    print("=" * 60)

    yuv_file = 'output.yuv'
    width, height = 1920, 1080
    output_png = 'restored.png'

    try:
        # Read, save, and display YUV file
        img = visualize_nv12(
            yuv_file,
            width,
            height,
            output_path=output_png,
            show=False  # Set to True to display the image
        )
        print(f"✓ Visualized YUV file: {yuv_file}")
        print(f"  Saved to: {output_png}")

    except FileNotFoundError:
        print(f"Note: {yuv_file} not found. Convert an image first.")
    except Exception as e:
        print(f"Error: {e}")


def example_with_error_handling():
    """Example: Proper error handling."""
    print("\n" + "=" * 60)
    print("Example 4: Error handling")
    print("=" * 60)

    try:
        # This will fail because dimensions are odd
        from PIL import Image

        # Create a test image with odd dimensions
        test_img = Image.new('RGB', (641, 480))  # Odd width
        test_img.save('odd_test.png')

        convert_to_nv12('odd_test.png', 'odd_test.yuv')

    except DimensionError as e:
        print(f"✓ Caught DimensionError as expected:")
        print(f"  {e}")

        # Clean up
        if os.path.exists('odd_test.png'):
            os.remove('odd_test.png')

    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("YUV NV12 Converter - Python API Examples")
    print("=" * 60 + "\n")

    example_convert()
    example_read()
    example_visualize()
    example_with_error_handling()

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
