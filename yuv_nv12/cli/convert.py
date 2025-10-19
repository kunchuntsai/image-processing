#!/usr/bin/env python3
"""
Command-line interface for converting images to YUV NV12 format.

Usage:
    yuv-convert input.jpg output.yuv
    yuv-convert input.png output.nv12
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
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Check file extension
    input_ext = os.path.splitext(args.input)[1].lower()
    if input_ext not in ['.jpg', '.jpeg', '.png']:
        print(f"Warning: Input file extension is '{input_ext}'. Supported formats: .jpg, .jpeg, .png")

    try:
        if args.verbose:
            print(f"Converting: {args.input}")
            print(f"Output: {args.output}")
            print("Processing...", end='', flush=True)

        # Perform conversion
        width, height = convert_to_nv12(args.input, args.output)

        if args.verbose:
            print(" Done!")

        print(f"✓ Successfully converted to YUV NV12 format")
        print(f"  Dimensions: {width}x{height}")
        print(f"  Output: {args.output}")

        if args.info:
            print("\nFile Information:")
            info = get_file_info(args.output)
            print(f"  Format: {info['format']}")
            print(f"  File size: {info['file_size']:,} bytes")
            print(f"  Total pixels: {info['total_pixels']:,}")

    except DimensionError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        print("\nSuggestion: Resize your image to have even width and height.", file=sys.stderr)
        sys.exit(1)

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
