# Image to YUV NV12 Converter

Convert JPG/PNG images to YUV420 NV12 format and read/visualize YUV NV12 files.

## Features

- Convert JPG/PNG images to YUV420 NV12 binary format
- Read and visualize YUV NV12 files
- Command-line interface and Python module API
- Automatic dimension validation (requires even width/height)
- Error handling and progress indicators

## Project Structure

```
image-processing/
├── yuv_nv12/               # Main package
│   ├── __init__.py         # Package initialization
│   ├── converter.py        # Image to YUV converter
│   ├── reader.py           # YUV to image reader
│   └── cli/                # Command-line interface
│       ├── __init__.py
│       ├── convert.py      # yuv-convert CLI tool
│       └── read.py         # yuv-read CLI tool
├── tests/
│   └── test_converter.py   # Test suite
├── examples/
│   └── basic_usage.py      # Python API examples
├── docs/                   # Documentation (future)
├── requirements.txt        # Python dependencies
├── setup.py                # Package setup script
└── README.md               # This file
```

## Installation

### Development Setup

```bash
# Clone or navigate to the project directory
cd image-processing

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

#### Convert Image to YUV NV12

```bash
# Using installed CLI tools (after pip install)
yuv-convert input.jpg output.yuv

# With verbose output
yuv-convert input.png output.nv12 -v

# Show file information after conversion
yuv-convert image.jpg output.yuv --info
```

#### Read and Visualize YUV NV12

```bash
# Display YUV file (requires width and height)
yuv-read video.yuv 1920 1080

# Convert YUV to PNG without displaying
yuv-read frame.yuv 640 480 --output restored.png --no-show

# Show file information (works with both YUV and image files)
yuv-read data.nv12 --info
yuv-read image.jpg --info  # Shows image format and dimensions

# Note: yuv-read only reads YUV files for conversion
# Image files (.jpg, .png) can only be inspected with --info
# To convert images to YUV, use yuv-convert
```

### Python Module Usage

#### Converting to YUV NV12

```python
from yuv_nv12 import convert_to_nv12

# Convert image to YUV NV12
width, height = convert_to_nv12('input.jpg', 'output.yuv')
print(f"Converted image: {width}x{height}")
```

#### Reading YUV NV12

```python
from yuv_nv12 import read_nv12, visualize_nv12, get_nv12_info

# Read YUV file and get PIL Image
img = read_nv12('video.yuv', 1920, 1080)

# Visualize and save
img = visualize_nv12('frame.yuv', 640, 480, output_path='restored.png')

# Get file information (works with YUV and image files)
info = get_nv12_info('data.yuv')
print(f"Format: {info['format']}")
print(f"Total pixels: {info['total_pixels']}")

# Also works with image files
img_info = get_nv12_info('photo.jpg')
print(f"Format: {img_info['format']}")  # Shows "JPEG Image"
print(f"Dimensions: {img_info['dimensions']}")  # e.g., "1920 x 1080"
```

#### See More Examples

Check out `examples/basic_usage.py` for comprehensive Python API examples:

```bash
source venv/bin/activate
python examples/basic_usage.py
```

## YUV NV12 Format

NV12 is a YUV 4:2:0 format with the following layout:

- **Y plane**: Full resolution (width × height) luminance data
- **UV plane**: Half resolution (width × height/2) interleaved chrominance data
  - U and V samples are interleaved: UVUVUV...

Total file size: `width × height × 1.5` bytes

Reference: https://docs.kernel.org/userspace-api/media/v4l/pixfmt-yuv-planar.html

## Requirements

- Python 3.7+
- Pillow (PIL) >= 10.0.0
- NumPy >= 1.24.0

## Testing

Run the test suite to verify the installation:

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests from project root
cd tests && python test_converter.py && cd ..

# Or run from tests directory
cd tests
python test_converter.py
```

Expected output:
```
=== YUV NV12 Converter Test ===
✓ Modules imported successfully
✓ Converted successfully: 640x480
✓ File size matches expected
✓ Read successfully: (640, 480)
✓ All tests passed!
```

## Important Notes

- Input images must have **even width and height** (required by NV12 format)
- Color conversion uses BT.601 standard (most common for JPG/PNG)
- Full range YUV (0-255) is used
- `yuv-read --info` can inspect both YUV files and image files (JPG, PNG, etc.)
- `yuv-read` can only convert YUV files to images; use `yuv-convert` to convert images to YUV
- `get_nv12_info()` API function detects and reports the actual file format

## Examples

### Complete Workflow

```bash
# Activate virtual environment
source venv/bin/activate

# 1. Convert image to YUV
yuv-convert photo.jpg photo.yuv -v

# 2. Read and verify conversion
yuv-read photo.yuv 1920 1080 --output verified.png

# 3. Compare original and verified images
```

### Error Handling

The converter validates dimensions and provides helpful error messages:

```bash
$ yuv-convert odd_size.jpg output.yuv
✗ Error: Image dimensions must be even numbers. Got 1921x1080.
Please resize the image to even dimensions.
```

## Development

### Running Tests

```bash
source venv/bin/activate
python tests/test_converter.py
```

### Code Structure

- **yuv_nv12/converter.py**: Core RGB to YUV NV12 conversion logic
- **yuv_nv12/reader.py**: YUV NV12 to RGB conversion and visualization
- **yuv_nv12/cli/convert.py**: Command-line tool for image conversion
- **yuv_nv12/cli/read.py**: Command-line tool for reading YUV files

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you:
1. Activated the virtual environment: `source venv/bin/activate`
2. Installed dependencies: `pip install -r requirements.txt`
3. Are running scripts from the project root directory

### Dimension Errors

If conversion fails with dimension errors:
- Verify your image has even width and height
- Use an image editor to resize if needed
- The converter will reject odd dimensions automatically

## License

MIT License
