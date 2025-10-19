#!/usr/bin/env python3
"""
Command-line interface for reading and visualizing YUV NV12 files.

Usage:
    yuv-read input.yuv 1920 1080
    yuv-read input.yuv 1920 1080 --output restored.png
    yuv-read input.yuv 1920 1080 --no-show
"""

import argparse
import sys
import os

from yuv_nv12 import read_nv12, visualize_nv12, get_nv12_info


def main():
    parser = argparse.ArgumentParser(
        description='Read and visualize YUV420 NV12 files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  yuv-read video.yuv 1920 1080
  yuv-read frame.yuv 640 480 --output restored.png
  yuv-read data.nv12 1280 720 --no-show --output image.jpg

Note: Width and height must be even numbers and match the original image dimensions.
        """
    )

    parser.add_argument(
        'input',
        help='Input YUV NV12 file'
    )

    parser.add_argument(
        'width',
        type=int,
        nargs='?',
        help='Image width (must be even)'
    )

    parser.add_argument(
        'height',
        type=int,
        nargs='?',
        help='Image height (must be even)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Save converted image to this path (JPG/PNG)'
    )

    parser.add_argument(
        '--no-show',
        action='store_true',
        help='Do not display the image (only save if --output is specified)'
    )

    parser.add_argument(
        '-i', '--info',
        action='store_true',
        help='Show file information only (no conversion)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed information'
    )

    args = parser.parse_args()

    # Validate input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # If --info flag, show info and exit
    if args.info:
        try:
            info = get_nv12_info(args.input)
            print("File Information:")
            print(f"  File: {info['file_path']}")
            print(f"  Format: {info['format']}")
            print(f"  Size: {info['file_size']:,} bytes")

            # Handle image files vs YUV files
            if 'dimensions' in info:
                # It's an image file
                print(f"  Dimensions: {info['dimensions']}")
                print(f"  Total pixels: {info['total_pixels']:,}")
                if 'note' in info:
                    print(f"\nNote: {info['note']}")
            else:
                # It's a YUV file
                print(f"  Total pixels: {info['total_pixels']:,}")
                if info.get('suggested_dimensions'):
                    print(f"\n  Suggested dimensions (width x height):")
                    for w, h in info['suggested_dimensions']:
                        print(f"    {w} x {h}")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Require width and height for conversion
    if args.width is None or args.height is None:
        print("Error: Width and height are required for conversion.", file=sys.stderr)
        print("Use --info to see file information and suggested dimensions.", file=sys.stderr)
        print("\nUsage: yuv-read input.yuv WIDTH HEIGHT", file=sys.stderr)
        sys.exit(1)

    try:
        if args.verbose:
            print(f"Reading: {args.input}")
            print(f"Dimensions: {args.width}x{args.height}")
            print("Processing...", end='', flush=True)

        # Read and visualize
        img = visualize_nv12(
            args.input,
            args.width,
            args.height,
            output_path=args.output,
            show=not args.no_show
        )

        if args.verbose:
            print(" Done!")

        print(f"✓ Successfully read YUV NV12 file")
        print(f"  Dimensions: {args.width}x{args.height}")

        if args.output:
            print(f"  Saved to: {args.output}")

        if not args.no_show and not args.output:
            print("  (Displaying image...)")

    except ValueError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        print("\nTry using --info to see file information and suggested dimensions.", file=sys.stderr)
        sys.exit(1)

    except FileNotFoundError as e:
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
