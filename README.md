# SVG Morph Studio

A powerful web application for creating smooth morphing animations between two SVG images with extensive control over the transition.

## Features

- **SVG Upload**: Upload any two SVG files and preview them before morphing
- **Automatic Shape Conversion**: Automatically converts circles, rectangles, ellipses, and polygons to paths
- **Smooth Morphing**: Uses Flubber library for high-quality path interpolation
- **Animation Controls**:
  - Adjustable duration (100ms - 5000ms)
  - Multiple easing functions (Linear, Quad, Cubic, Quart variations)
  - Loop mode with optional reverse
  - Play/Pause/Reset controls
  - Scrubbing via progress slider
- **Color Interpolation**:
  - None (instant switch)
  - Linear RGB interpolation
  - LAB color space (perceptually uniform)
- **Path Precision Control**: Adjust the detail level of morphed paths
- **Responsive Design**: Works on desktop and mobile devices

## Usage

1. Open `index.html` in a modern web browser
2. Upload your first SVG file using the left upload button
3. Upload your second SVG file using the right upload button
4. Adjust animation parameters using the control panel
5. Click "Play" to start the morphing animation
6. Use the progress slider to scrub through the animation manually

## Sample Files

The `samples/` directory contains example SVG files you can use for testing:

- `sample1-star.svg` - A colorful star shape
- `sample2-chinese-char.svg` - Chinese character "中" (zhōng - middle/center)
- `sample3-person.svg` - A simple colored person icon
- `sample4-korean-char.svg` - Korean character "한" (han - Korean)

Try morphing between different combinations, such as:
- Star → Chinese character (colored to monochrome)
- Person → Korean character (complex to simple)

## Animation Controls Explained

### Duration
Controls how long the morphing animation takes to complete from start to finish.

### Easing Function
Determines the acceleration curve of the animation:
- **Linear**: Constant speed throughout
- **Ease In**: Slow start, fast finish
- **Ease Out**: Fast start, slow finish
- **Ease In-Out**: Slow start and finish, fast middle
- **Quad/Cubic/Quart**: Different acceleration intensities

### Loop Animation
When enabled, the animation repeats continuously.

### Reverse on Loop
When enabled with Loop, creates a ping-pong effect (A→B→A→B...).

### Color Interpolation
- **None**: Instantly switches to target color
- **Linear**: Simple RGB color mixing
- **LAB**: More natural-looking color transitions using LAB color space

### Path Precision
Controls the `maxSegmentLength` parameter:
- **Lower values (1-5)**: Smoother paths, less detail preservation
- **Higher values (15-20)**: More detail, potentially choppier curves

## Technical Details

### Technologies Used
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Application logic
- **Flubber**: SVG path morphing library

### Browser Compatibility
Works in all modern browsers that support:
- ES6 JavaScript
- SVG rendering
- CSS Grid and Flexbox

### How It Works

1. **SVG Parsing**: The app parses uploaded SVG files using DOMParser
2. **Path Extraction**: Extracts all path elements and converts other shapes (circles, rects, etc.) to paths
3. **ViewBox Merging**: Combines viewBoxes from both SVGs to ensure all content is visible
4. **Interpolation**: Uses Flubber to create interpolation functions between corresponding paths
5. **Color Morphing**: Creates custom color interpolators (RGB or LAB color space)
6. **Animation Loop**: Uses requestAnimationFrame for smooth 60fps animations
7. **Easing**: Applies mathematical easing functions to create natural motion

### Color Space Conversion

The LAB color space option provides more perceptually uniform color transitions. The app includes:
- RGB → LAB conversion
- LAB → RGB conversion
- Proper color clamping to prevent invalid values

## Limitations

- Works best with SVGs that have similar path complexity
- Very complex SVGs (100+ paths) may have performance impacts
- Some exotic SVG features (filters, gradients, patterns) may not be preserved
- Text elements are not automatically converted (use path-based text)

## Tips for Best Results

1. **Simplify your SVGs**: Remove unnecessary elements before uploading
2. **Match complexity**: SVGs with similar numbers of paths morph more smoothly
3. **Use path-based shapes**: Convert text and complex shapes to paths in your SVG editor
4. **Experiment with precision**: Different shapes work better with different precision settings
5. **Try LAB color space**: For more natural color transitions, especially with saturated colors

## Future Enhancements

Potential features for future versions:
- Export animation as video or GIF
- Save/load animation presets
- Multiple keyframe support
- Custom easing curves (Bezier editor)
- SVG optimization tools
- Batch processing

## License

This project is open source and available for personal and commercial use.

## Credits

Built with [Flubber](https://github.com/veltman/flubber) by Noah Veltman for SVG path interpolation.
