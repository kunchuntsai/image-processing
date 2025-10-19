# YUV NV12 Converter - Project Overview

## Introduction

This project provides a complete solution for converting images to/from YUV420 NV12 format, a widely used video format in multimedia applications.

## Architecture

### Directory Structure

```
image-processing/
├── yuv_nv12/              # Core package
│   ├── cli/               # CLI implementation
│   ├── converter.py       # Conversion logic
│   └── reader.py          # Reading logic
├── tests/                 # Test suite
├── examples/              # Usage examples
├── docs/                  # Documentation
├── requirements.txt       # Dependencies
└── setup.py               # Package installation
```

### Core Components

#### 1. Converter Module (`yuv_nv12/converter.py`)

Handles conversion from RGB images to YUV NV12 format.

**Key Functions:**
- `convert_to_nv12(image_path, output_path)`: Main conversion function
- `rgb_to_yuv_bt601(r, g, b)`: Color space conversion using BT.601 standard
- `validate_dimensions(width, height)`: Ensures even dimensions

**Process Flow:**
1. Load image using PIL
2. Convert to RGB if needed
3. Validate dimensions (must be even)
4. Apply RGB to YUV color space conversion
5. Subsample U and V channels (4:2:0)
6. Interleave U and V channels
7. Write Y plane followed by UV plane to file

#### 2. Reader Module (`yuv_nv12/reader.py`)

Handles reading YUV NV12 files and converting back to RGB.

**Key Functions:**
- `read_nv12(yuv_path, width, height)`: Read and convert YUV to PIL Image
- `visualize_nv12(yuv_path, width, height, output_path, show)`: Read, save, and display
- `yuv_to_rgb_bt601(Y, U, V)`: Inverse color space conversion
- `get_nv12_info(yuv_path)`: Get file information and detect format (YUV/JPEG/PNG)

**Process Flow:**
1. Validate file size matches expected dimensions
2. Read Y plane (full resolution)
3. Read interleaved UV plane
4. De-interleave U and V channels
5. Upsample U and V to full resolution
6. Apply YUV to RGB color space conversion
7. Create PIL Image from RGB data

#### 3. Command-Line Tools (`yuv_nv12/cli/`)

Installed as console scripts via setuptools. After running `pip install -e .`, these commands become available:

**yuv-convert** (`yuv_nv12/cli/convert.py`):
- User-friendly interface for image conversion
- Progress indicators and verbose mode
- Error handling with helpful messages
- Automatic format detection

**yuv-read** (`yuv_nv12/cli/read.py`):
- Read and visualize YUV files
- File information display (supports YUV and image files)
- Optional save and display modes
- Format detection for inspection

## Technical Details

### YUV NV12 Format

**Layout:**
```
+-------------------+
|                   |
|    Y Plane        |  Full resolution (W x H)
|  (Luminance)      |
|                   |
+-------------------+
|  UV Plane         |  Half resolution (W x H/2)
| (Chrominance)     |  Interleaved: UVUVUV...
+-------------------+
```

**File Size:** `width × height × 1.5` bytes

### Color Space Conversion

**RGB to YUV (BT.601 Full Range):**
```
Y = 0.299*R + 0.587*G + 0.114*B
U = -0.168736*R - 0.331264*G + 0.5*B + 128
V = 0.5*R - 0.418688*G - 0.081312*B + 128
```

**YUV to RGB (BT.601 Full Range):**
```
R = Y + 1.402*(V-128)
G = Y - 0.344136*(U-128) - 0.714136*(V-128)
B = Y + 1.772*(U-128)
```

### Subsampling (4:2:0)

- Y channel: Full resolution (every pixel)
- U channel: Downsampled to 1/4 resolution (every 2x2 block)
- V channel: Downsampled to 1/4 resolution (every 2x2 block)

This reduces file size by 50% compared to RGB while maintaining perceived quality.

## Error Handling

### Dimension Validation

NV12 format requires even dimensions for proper 4:2:0 subsampling:
- Odd dimensions are rejected with `DimensionError`
- User receives clear message suggesting to resize

### File Validation

- Input file existence checked before processing
- File size validated against expected dimensions
- Supported formats: JPG, JPEG, PNG
- Automatic format detection for both conversion and inspection

### Color Range Clipping

All color values are clipped to valid range [0, 255] to prevent overflow/underflow.

## Testing

### Test Suite (`tests/test_converter.py`)

**Tests Include:**
1. Complete conversion workflow (RGB → YUV → RGB)
2. File size validation
3. Dimension validation
4. Odd dimension rejection
5. Round-trip conversion quality

**Run Tests:**
```bash
source venv/bin/activate
python tests/test_converter.py
```

## Performance Considerations

### Optimization Strategies

1. **NumPy Arrays:** Vectorized operations for fast processing
2. **Direct File I/O:** Binary file operations for efficiency
3. **Minimal Memory Copies:** In-place operations where possible

### Typical Performance

- Conversion: ~100-200ms for 1920x1080 image
- Reading: ~50-100ms for 1920x1080 image
- Depends on: CPU, disk I/O, image complexity

## Use Cases

1. **Video Processing:** Prepare frames for video encoding
2. **Computer Vision:** Convert images to YUV for processing
3. **Hardware Testing:** Generate test patterns in NV12 format
4. **Format Conversion:** Batch convert images to/from YUV

## Future Enhancements

### Potential Features

- [ ] Batch conversion support
- [ ] Additional color spaces (BT.709, BT.2020)
- [ ] Other YUV formats (I420, YV12, NV21)
- [ ] GPU acceleration for large batches
- [ ] Quality metrics (PSNR, SSIM)
- [ ] Video file support (read/write sequences)

### Code Improvements

- [ ] Unit tests with pytest
- [ ] Type hints throughout
- [ ] Comprehensive docstrings
- [ ] Performance benchmarks
- [ ] CI/CD pipeline

## References

- [Linux Kernel V4L2 Documentation](https://docs.kernel.org/userspace-api/media/v4l/pixfmt-yuv-planar.html)
- [BT.601 Standard](https://en.wikipedia.org/wiki/Rec._601)
- [YUV Color Space](https://en.wikipedia.org/wiki/YUV)
- [Chroma Subsampling](https://en.wikipedia.org/wiki/Chroma_subsampling)

## Contributing

See main README.md for contribution guidelines.

## License

MIT License - See LICENSE file for details.
