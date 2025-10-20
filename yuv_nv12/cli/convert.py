#!/usr/bin/env python
"""
Command-line interface for converting images to YUV NV12 format.

Usage:
    yuv-convert input.jpg output.yuv
    yuv-convert input.png output.nv12

Python 3.4+ compatible version (no f-strings)
"""

import argparse
import sys
import os

from yuv_nv12 import convert_to_nv12, DimensionError, get_file_info


def main():
    parser = argparse.ArgumentParser(
        description='Convert JPG/PNG images to YUV420 NV12 format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  yuv-convert image.jpg output.yuv
  yuv-convert photo.png output.nv12

Note: Input image must have even width and height dimensions.
        """
    )

    parser.add_argument(
        'input',
        help='Input image file (JPG/PNG)'
    )

    parser.add_argument(
        'output',
        help='Output YUV file path'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed information'
    )

    parser.add_argument(
        '--info',
        action='store_true',
        help='Show output file information after conversion'
    )

    args = parser.parse_args()

    # Validate input file exists
    if not os.path.exists(args.input):
        print("Error: Input file not found: {0}".format(args.input), file=sys.stderr)
        sys.exit(1)

    # Check file extension
    input_ext = os.path.splitext(args.input)[1].lower()
    if input_ext not in ['.jpg', '.jpeg', '.png']:
        print("Warning: Input file extension is '{0}'. Supported formats: .jpg, .jpeg, .png".format(input_ext))

    try:
        if args.verbose:
            print("Converting: {0}".format(args.input))
            print("Output: {0}".format(args.output))
            sys.stdout.write("Processing...")
            sys.stdout.flush()

        # Perform conversion
        width, height = convert_to_nv12(args.input, args.output)

        if args.verbose:
            print(" Done!")

        print("✓ Successfully converted to YUV NV12 format")
        print("  Dimensions: {0}x{1}".format(width, height))
        print("  Output: {0}".format(args.output))

        if args.info:
            print("\nFile Information:")
            info = get_file_info(args.output)
            print("  Format: {0}".format(info['format']))
            print("  File size: {0:,} bytes".format(info['file_size']))
            print("  Total pixels: {0:,}".format(info['total_pixels']))

    except DimensionError as e:
        print("\n✗ Error: {0}".format(e), file=sys.stderr)
        print("\nSuggestion: Resize your image to have even width and height.", file=sys.stderr)
        sys.exit(1)

    except IOError as e:
        print("\n✗ Error: {0}".format(e), file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print("\n✗ Error: {0}".format(e), file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print("\n✗ Unexpected error: {0}".format(e), file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
