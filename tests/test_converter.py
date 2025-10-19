#!/usr/bin/env python3
"""
Test script for YUV NV12 converter and reader.
Creates a test image, converts it to YUV, and reads it back.
"""

from PIL import Image, ImageDraw
import os
import sys


def create_test_image(width=640, height=480, filename='test_image.png'):
    """Create a simple test image with colored stripes."""
    print(f"Creating test image: {width}x{height}")

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
    print(f"✓ Test image saved: {filename}")
    return filename


def test_conversion():
    """Test the complete conversion workflow."""
    print("\n=== YUV NV12 Converter Test ===\n")

    # Import modules
    try:
        from yuv_nv12 import convert_to_nv12, read_nv12
        print("✓ Modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import modules: {e}")
        return False

    # Create test image
    test_img = create_test_image(640, 480, 'test_image.png')
    yuv_file = 'test_output.yuv'
    restored_file = 'test_restored.png'

    try:
        # Test conversion to YUV
        print(f"\nConverting to YUV NV12...")
        width, height = convert_to_nv12(test_img, yuv_file)
        print(f"✓ Converted successfully: {width}x{height}")

        # Check file size
        expected_size = int(width * height * 1.5)
        actual_size = os.path.getsize(yuv_file)
        print(f"  File size: {actual_size} bytes (expected: {expected_size})")

        if actual_size == expected_size:
            print("✓ File size matches expected")
        else:
            print("✗ File size mismatch!")
            return False

        # Test reading YUV
        print(f"\nReading YUV NV12 file...")
        img = read_nv12(yuv_file, width, height)
        print(f"✓ Read successfully: {img.size}")

        # Save restored image
        img.save(restored_file)
        print(f"✓ Restored image saved: {restored_file}")

        print("\n=== Test Summary ===")
        print(f"Original image: {test_img}")
        print(f"YUV file: {yuv_file}")
        print(f"Restored image: {restored_file}")
        print("\nYou can compare the original and restored images to verify quality.")
        print("Note: Some minor color differences may occur due to YUV conversion.")

        return True

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
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
            print(f"✓ Correctly rejected odd dimensions: {e}")
            os.remove('test_odd.png')
            return True

    except Exception as e:
        print(f"✗ Unexpected error: {e}")
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
