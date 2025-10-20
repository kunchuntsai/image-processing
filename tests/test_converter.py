#!/usr/bin/env python
"""
Test script for YUV NV12 converter and reader.
Creates a test image, converts it to YUV, and reads it back.

Python 3.4+ compatible version (no f-strings)
"""

from PIL import Image, ImageDraw
import os
import sys


def create_test_image(width=640, height=480, filename='test_image.png'):
    """Create a simple test image with colored stripes."""
    print("Creating test image: {0}x{1}".format(width, height))

    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Create colored stripes
    stripe_height = height // 4
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
    ]

    for i, color in enumerate(colors):
        y0 = i * stripe_height
        y1 = (i + 1) * stripe_height if i < 3 else height
        draw.rectangle([0, y0, width, y1], fill=color)

    # Add some text
    draw.text((20, 20), "YUV NV12 Test", fill=(255, 255, 255))

    img.save(filename)
    print("✓ Test image saved: {0}".format(filename))
    return filename


def test_conversion():
    """Test the complete conversion workflow."""
    print("\n=== YUV NV12 Converter Test ===\n")

    # Import modules
    try:
        from yuv_nv12 import convert_to_nv12, read_nv12
        print("✓ Modules imported successfully")
    except ImportError as e:
        print("✗ Failed to import modules: {0}".format(e))
        return False

    # Create test image
    test_img = create_test_image(640, 480, 'test_image.png')
    yuv_file = 'test_output.yuv'
    restored_file = 'test_restored.png'

    try:
        # Test conversion to YUV
        print("\nConverting to YUV NV12...")
        width, height = convert_to_nv12(test_img, yuv_file)
        print("✓ Converted successfully: {0}x{1}".format(width, height))

        # Check file size
        expected_size = int(width * height * 1.5)
        actual_size = os.path.getsize(yuv_file)
        print("  File size: {0} bytes (expected: {1})".format(actual_size, expected_size))

        if actual_size == expected_size:
            print("✓ File size matches expected")
        else:
            print("✗ File size mismatch!")
            return False

        # Test reading YUV
        print("\nReading YUV NV12 file...")
        img = read_nv12(yuv_file, width, height)
        print("✓ Read successfully: {0}".format(img.size))

        # Save restored image
        img.save(restored_file)
        print("✓ Restored image saved: {0}".format(restored_file))

        print("\n=== Test Summary ===")
        print("Original image: {0}".format(test_img))
        print("YUV file: {0}".format(yuv_file))
        print("Restored image: {0}".format(restored_file))
        print("\nYou can compare the original and restored images to verify quality.")
        print("Note: Some minor color differences may occur due to YUV conversion.")

        return True

    except Exception as e:
        print("\n✗ Test failed: {0}".format(e))
        import traceback
        traceback.print_exc()
        return False


def test_odd_dimensions():
    """Test that odd dimensions are properly rejected."""
    print("\n=== Testing Odd Dimension Validation ===\n")

    try:
        from yuv_nv12 import convert_to_nv12, DimensionError

        # Create image with odd dimensions
        img = Image.new('RGB', (641, 480))  # Odd width
        img.save('test_odd.png')

        try:
            convert_to_nv12('test_odd.png', 'test_odd.yuv')
            print("✗ Should have raised DimensionError!")
            return False
        except DimensionError as e:
            print("✓ Correctly rejected odd dimensions: {0}".format(e))
            os.remove('test_odd.png')
            return True

    except Exception as e:
        print("✗ Unexpected error: {0}".format(e))
        return False


if __name__ == '__main__':
    success = True

    # Run tests
    success &= test_conversion()
    success &= test_odd_dimensions()

    print("\n" + "="*50)
    if success:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)
