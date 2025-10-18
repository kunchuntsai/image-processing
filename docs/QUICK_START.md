# Quick Start Guide

## Installation

```bash
# 1. Navigate to project directory
cd image-processing

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### Convert an Image to YUV NV12

```bash
# Make sure venv is activated
source venv/bin/activate

# Convert image
bin/yuv-convert input.jpg output.yuv

# With verbose output and file info
bin/yuv-convert input.jpg output.yuv -v --info
```

### Read a YUV NV12 File

```bash
# Read and display YUV file (requires dimensions)
bin/yuv-read output.yuv 1920 1080

# Save to PNG without displaying
bin/yuv-read output.yuv 1920 1080 --output restored.png --no-show

# Get file information
bin/yuv-read output.yuv --info
```

## Python API

### Import the Module

```python
from yuv_nv12 import convert_to_nv12, read_nv12, visualize_nv12
```

### Convert Image

```python
# Convert image to YUV
width, height = convert_to_nv12('input.jpg', 'output.yuv')
print(f"Converted: {width}x{height}")
```

### Read YUV File

```python
# Read YUV and get PIL Image
img = read_nv12('output.yuv', 1920, 1080)

# Or read, save, and display
img = visualize_nv12('output.yuv', 1920, 1080,
                     output_path='restored.png',
                     show=True)
```

## Testing

```bash
# Run test suite
source venv/bin/activate
python tests/test_converter.py
```

## Common Issues

### "Module not found" Error

Make sure you:
1. Activated the virtual environment
2. Installed dependencies
3. Are in the project root directory

### "Dimension Error"

Images must have even width and height:
- ✓ 1920x1080 (valid)
- ✗ 1921x1080 (invalid - odd width)

Use an image editor to resize to even dimensions.

### File Size Mismatch

When reading YUV files, ensure the width and height match the original image dimensions. Use `--info` flag to see suggested dimensions:

```bash
bin/yuv-read myfile.yuv --info
```

## Examples

See `examples/basic_usage.py` for more detailed Python API examples:

```bash
source venv/bin/activate
python examples/basic_usage.py
```

## Next Steps

- Read the full [README.md](../README.md) for complete documentation
- Check [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for technical details
- Review [REQUIREMENTS.md](REQUIREMENTS.md) for project requirements
