## Context
This project is to create an image converter from all types to YUV (NV12) format

## Details
- Reference: https://docs.kernel.org/userspace-api/media/v4l/pixfmt-yuv-planar.html
- Implement it by python
- Input: Be able to read a jpg, png image
- Output: YUV420 (NV12)


## Questions
1. Output format: Should the output be:
  - A binary file (raw YUV data)?
  - Or should it include any headers/metadata?
  - What should be the file extension? (e.g., .yuv, .nv12)?
  > It will be a binary file, so please also implement a reader to ready the output format and be able to visualize it
2. Image dimensions: Should the converter:
  - Preserve the original image dimensions?
  - Handle odd-width/odd-height images (NV12 typically requires even dimensions)?
  - Resize if dimensions are odd?
  > It will be even width/height, so add a checking before converting
3. Color space: Should I assume the input images are in:
  - sRGB color space (standard for JPG/PNG)?
  - Any specific color range (full range 0-255 or limited range 16-235)?
  > Please use the most common way to do it
4. Usage interface: How should the tool be used?
  - Command-line interface (e.g., python convert.py input.jpg output.yuv)?
  - A Python function/module that can be imported?
  - Both?
  > Please provide both, but go for command-line first and make it be able to separate
5. Dependencies: Are you okay with using common Python libraries like:
  - PIL/Pillow for image reading?
  - NumPy for array operations?
  > Yes
6. Additional features: Do you need:
  - Batch conversion support? Please focus on single image first
  - Error handling for invalid inputs? Yes
  - Progress indicators? Yes