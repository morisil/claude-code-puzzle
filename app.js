// SVG Morph Studio - Main Application Logic

class SVGMorphStudio {
    constructor() {
        this.svg1Data = null;
        this.svg2Data = null;
        this.svg1Paths = [];
        this.svg2Paths = [];
        this.interpolators = [];
        this.colorInterpolators = [];
        this.animationId = null;
        this.isPlaying = false;
        this.isPaused = false;
        this.currentProgress = 0;
        this.startTime = null;
        this.pausedTime = 0;

        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // File uploads
        document.getElementById('svg1-upload').addEventListener('change', (e) => this.handleSVGUpload(e, 1));
        document.getElementById('svg2-upload').addEventListener('change', (e) => this.handleSVGUpload(e, 2));

        // Control updates
        document.getElementById('duration').addEventListener('input', (e) => {
            document.getElementById('duration-value').textContent = e.target.value;
        });

        document.getElementById('max-segment-length').addEventListener('input', (e) => {
            document.getElementById('precision-value').textContent = e.target.value;
            if (this.svg1Data && this.svg2Data) {
                this.prepareMorph();
            }
        });

        // Playback controls
        document.getElementById('play-btn').addEventListener('click', () => this.play());
        document.getElementById('pause-btn').addEventListener('click', () => this.pause());
        document.getElementById('reset-btn').addEventListener('click', () => this.reset());

        // Progress slider
        document.getElementById('progress').addEventListener('input', (e) => {
            this.scrubToPosition(parseFloat(e.target.value) / 100);
        });

        // Settings that require re-preparing the morph
        document.getElementById('color-interpolation').addEventListener('change', () => {
            if (this.svg1Data && this.svg2Data) {
                this.prepareMorph();
            }
        });
    }

    async handleSVGUpload(event, svgNumber) {
        const file = event.target.files[0];
        if (!file) return;

        try {
            const text = await file.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'image/svg+xml');

            // Check for parsing errors
            const parserError = doc.querySelector('parsererror');
            if (parserError) {
                alert('Error parsing SVG file. Please upload a valid SVG.');
                return;
            }

            const svgElement = doc.querySelector('svg');
            if (!svgElement) {
                alert('No SVG element found in file.');
                return;
            }

            // Store the SVG data
            if (svgNumber === 1) {
                this.svg1Data = svgElement;
                document.getElementById('svg1-name').textContent = file.name;
                this.displayPreview(svgElement.cloneNode(true), 'svg1-preview');
            } else {
                this.svg2Data = svgElement;
                document.getElementById('svg2-name').textContent = file.name;
                this.displayPreview(svgElement.cloneNode(true), 'svg2-preview');
            }

            // If both SVGs are loaded, prepare the morph
            if (this.svg1Data && this.svg2Data) {
                this.prepareMorph();
                this.enableControls();
            }
        } catch (error) {
            console.error('Error loading SVG:', error);
            alert('Error loading SVG file: ' + error.message);
        }
    }

    displayPreview(svgElement, previewId) {
        const preview = document.getElementById(previewId);
        preview.innerHTML = '';
        preview.appendChild(svgElement);
        preview.classList.add('active');
    }

    extractPaths(svgElement) {
        const paths = [];

        // Get all path elements
        const pathElements = svgElement.querySelectorAll('path');
        pathElements.forEach(path => {
            const d = path.getAttribute('d');
            if (d) {
                paths.push({
                    d: d,
                    fill: path.getAttribute('fill') || '#000000',
                    stroke: path.getAttribute('stroke') || 'none',
                    strokeWidth: path.getAttribute('stroke-width') || '0'
                });
            }
        });

        // Convert other shapes to paths
        this.convertShapesToPaths(svgElement, paths);

        return paths;
    }

    convertShapesToPaths(svgElement, paths) {
        // Convert circles
        svgElement.querySelectorAll('circle').forEach(circle => {
            const cx = parseFloat(circle.getAttribute('cx') || 0);
            const cy = parseFloat(circle.getAttribute('cy') || 0);
            const r = parseFloat(circle.getAttribute('r') || 0);

            const d = `M ${cx - r},${cy} a ${r},${r} 0 1,0 ${r * 2},0 a ${r},${r} 0 1,0 -${r * 2},0`;
            paths.push({
                d: d,
                fill: circle.getAttribute('fill') || '#000000',
                stroke: circle.getAttribute('stroke') || 'none',
                strokeWidth: circle.getAttribute('stroke-width') || '0'
            });
        });

        // Convert rectangles
        svgElement.querySelectorAll('rect').forEach(rect => {
            const x = parseFloat(rect.getAttribute('x') || 0);
            const y = parseFloat(rect.getAttribute('y') || 0);
            const width = parseFloat(rect.getAttribute('width') || 0);
            const height = parseFloat(rect.getAttribute('height') || 0);

            const d = `M ${x},${y} L ${x + width},${y} L ${x + width},${y + height} L ${x},${y + height} Z`;
            paths.push({
                d: d,
                fill: rect.getAttribute('fill') || '#000000',
                stroke: rect.getAttribute('stroke') || 'none',
                strokeWidth: rect.getAttribute('stroke-width') || '0'
            });
        });

        // Convert ellipses
        svgElement.querySelectorAll('ellipse').forEach(ellipse => {
            const cx = parseFloat(ellipse.getAttribute('cx') || 0);
            const cy = parseFloat(ellipse.getAttribute('cy') || 0);
            const rx = parseFloat(ellipse.getAttribute('rx') || 0);
            const ry = parseFloat(ellipse.getAttribute('ry') || 0);

            const d = `M ${cx - rx},${cy} a ${rx},${ry} 0 1,0 ${rx * 2},0 a ${rx},${ry} 0 1,0 -${rx * 2},0`;
            paths.push({
                d: d,
                fill: ellipse.getAttribute('fill') || '#000000',
                stroke: ellipse.getAttribute('stroke') || 'none',
                strokeWidth: ellipse.getAttribute('stroke-width') || '0'
            });
        });

        // Convert polygons
        svgElement.querySelectorAll('polygon').forEach(polygon => {
            const points = polygon.getAttribute('points');
            if (points) {
                const pointArray = points.trim().split(/\s+/);
                let d = 'M ';
                pointArray.forEach((point, index) => {
                    const coords = point.split(',');
                    if (coords.length === 2) {
                        d += `${coords[0]},${coords[1]} `;
                        if (index > 0) d = d.slice(0, -1) + ' L ';
                    }
                });
                d += 'Z';
                paths.push({
                    d: d,
                    fill: polygon.getAttribute('fill') || '#000000',
                    stroke: polygon.getAttribute('stroke') || 'none',
                    strokeWidth: polygon.getAttribute('stroke-width') || '0'
                });
            }
        });
    }

    prepareMorph() {
        try {
            // Extract paths from both SVGs
            this.svg1Paths = this.extractPaths(this.svg1Data.cloneNode(true));
            this.svg2Paths = this.extractPaths(this.svg2Data.cloneNode(true));

            if (this.svg1Paths.length === 0 || this.svg2Paths.length === 0) {
                alert('One or both SVGs contain no valid paths. Please upload SVGs with path elements or basic shapes.');
                return;
            }

            // Get the viewBox or create one based on content
            const viewBox1 = this.getViewBox(this.svg1Data);
            const viewBox2 = this.getViewBox(this.svg2Data);

            // Use the larger viewBox to accommodate both SVGs
            const finalViewBox = this.mergeViewBoxes(viewBox1, viewBox2);
            document.getElementById('morph-canvas').setAttribute('viewBox',
                `${finalViewBox.x} ${finalViewBox.y} ${finalViewBox.width} ${finalViewBox.height}`);

            // Create interpolators for each path pair
            this.interpolators = [];
            this.colorInterpolators = [];

            const maxPaths = Math.max(this.svg1Paths.length, this.svg2Paths.length);
            const maxSegmentLength = parseFloat(document.getElementById('max-segment-length').value);

            for (let i = 0; i < maxPaths; i++) {
                const path1 = this.svg1Paths[i % this.svg1Paths.length];
                const path2 = this.svg2Paths[i % this.svg2Paths.length];

                try {
                    // Create path interpolator using Flubber
                    const interpolator = flubber.interpolate(path1.d, path2.d, {
                        maxSegmentLength: maxSegmentLength
                    });

                    this.interpolators.push(interpolator);

                    // Create color interpolator
                    this.colorInterpolators.push({
                        fill: this.createColorInterpolator(path1.fill, path2.fill),
                        stroke: this.createColorInterpolator(path1.stroke, path2.stroke),
                        strokeWidth: this.createNumberInterpolator(
                            parseFloat(path1.strokeWidth),
                            parseFloat(path2.strokeWidth)
                        )
                    });
                } catch (error) {
                    console.warn(`Could not create interpolator for path ${i}:`, error);
                    // Create a simple interpolator that just switches between the two
                    this.interpolators.push((t) => t < 0.5 ? path1.d : path2.d);
                    this.colorInterpolators.push({
                        fill: (t) => t < 0.5 ? path1.fill : path2.fill,
                        stroke: (t) => t < 0.5 ? path1.stroke : path2.stroke,
                        strokeWidth: (t) => t < 0.5 ? parseFloat(path1.strokeWidth) : parseFloat(path2.strokeWidth)
                    });
                }
            }

            // Initialize the morph canvas at position 0
            this.updateMorphCanvas(0);

            console.log(`Prepared morph with ${this.interpolators.length} path interpolators`);
        } catch (error) {
            console.error('Error preparing morph:', error);
            alert('Error preparing morph: ' + error.message);
        }
    }

    getViewBox(svgElement) {
        const viewBox = svgElement.getAttribute('viewBox');
        if (viewBox) {
            const [x, y, width, height] = viewBox.split(/\s+/).map(parseFloat);
            return { x, y, width, height };
        }

        // Fallback: use width and height attributes or default
        const width = parseFloat(svgElement.getAttribute('width')) || 800;
        const height = parseFloat(svgElement.getAttribute('height')) || 600;
        return { x: 0, y: 0, width, height };
    }

    mergeViewBoxes(vb1, vb2) {
        const minX = Math.min(vb1.x, vb2.x);
        const minY = Math.min(vb1.y, vb2.y);
        const maxX = Math.max(vb1.x + vb1.width, vb2.x + vb2.width);
        const maxY = Math.max(vb1.y + vb1.height, vb2.y + vb2.height);

        return {
            x: minX,
            y: minY,
            width: maxX - minX,
            height: maxY - minY
        };
    }

    createColorInterpolator(color1, color2) {
        const mode = document.getElementById('color-interpolation').value;

        if (mode === 'none') {
            return (t) => t < 1 ? color1 : color2;
        }

        // Parse colors
        const c1 = this.parseColor(color1);
        const c2 = this.parseColor(color2);

        if (!c1 || !c2) {
            return (t) => t < 0.5 ? color1 : color2;
        }

        if (mode === 'lab') {
            // Convert to LAB color space for more perceptually uniform interpolation
            const lab1 = this.rgbToLab(c1);
            const lab2 = this.rgbToLab(c2);

            return (t) => {
                const l = lab1.l + (lab2.l - lab1.l) * t;
                const a = lab1.a + (lab2.a - lab1.a) * t;
                const b = lab1.b + (lab2.b - lab1.b) * t;
                const rgb = this.labToRgb({ l, a, b });
                return `rgb(${Math.round(rgb.r)}, ${Math.round(rgb.g)}, ${Math.round(rgb.b)})`;
            };
        }

        // Linear RGB interpolation
        return (t) => {
            const r = Math.round(c1.r + (c2.r - c1.r) * t);
            const g = Math.round(c1.g + (c2.g - c1.g) * t);
            const b = Math.round(c1.b + (c2.b - c1.b) * t);
            return `rgb(${r}, ${g}, ${b})`;
        };
    }

    createNumberInterpolator(num1, num2) {
        return (t) => num1 + (num2 - num1) * t;
    }

    parseColor(color) {
        if (!color || color === 'none' || color === 'transparent') {
            return { r: 0, g: 0, b: 0, a: 0 };
        }

        // Handle hex colors
        if (color.startsWith('#')) {
            const hex = color.slice(1);
            if (hex.length === 3) {
                return {
                    r: parseInt(hex[0] + hex[0], 16),
                    g: parseInt(hex[1] + hex[1], 16),
                    b: parseInt(hex[2] + hex[2], 16),
                    a: 1
                };
            } else if (hex.length === 6) {
                return {
                    r: parseInt(hex.slice(0, 2), 16),
                    g: parseInt(hex.slice(2, 4), 16),
                    b: parseInt(hex.slice(4, 6), 16),
                    a: 1
                };
            }
        }

        // Handle rgb/rgba
        const rgbMatch = color.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
        if (rgbMatch) {
            return {
                r: parseInt(rgbMatch[1]),
                g: parseInt(rgbMatch[2]),
                b: parseInt(rgbMatch[3]),
                a: rgbMatch[4] ? parseFloat(rgbMatch[4]) : 1
            };
        }

        return null;
    }

    rgbToLab(rgb) {
        // Convert RGB to XYZ
        let r = rgb.r / 255;
        let g = rgb.g / 255;
        let b = rgb.b / 255;

        r = r > 0.04045 ? Math.pow((r + 0.055) / 1.055, 2.4) : r / 12.92;
        g = g > 0.04045 ? Math.pow((g + 0.055) / 1.055, 2.4) : g / 12.92;
        b = b > 0.04045 ? Math.pow((b + 0.055) / 1.055, 2.4) : b / 12.92;

        let x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047;
        let y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000;
        let z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883;

        x = x > 0.008856 ? Math.pow(x, 1/3) : (7.787 * x) + 16/116;
        y = y > 0.008856 ? Math.pow(y, 1/3) : (7.787 * y) + 16/116;
        z = z > 0.008856 ? Math.pow(z, 1/3) : (7.787 * z) + 16/116;

        return {
            l: (116 * y) - 16,
            a: 500 * (x - y),
            b: 200 * (y - z)
        };
    }

    labToRgb(lab) {
        let y = (lab.l + 16) / 116;
        let x = lab.a / 500 + y;
        let z = y - lab.b / 200;

        x = 0.95047 * ((x * x * x > 0.008856) ? x * x * x : (x - 16/116) / 7.787);
        y = 1.00000 * ((y * y * y > 0.008856) ? y * y * y : (y - 16/116) / 7.787);
        z = 1.08883 * ((z * z * z > 0.008856) ? z * z * z : (z - 16/116) / 7.787);

        let r = x *  3.2406 + y * -1.5372 + z * -0.4986;
        let g = x * -0.9689 + y *  1.8758 + z *  0.0415;
        let b = x *  0.0557 + y * -0.2040 + z *  1.0570;

        r = (r > 0.0031308) ? (1.055 * Math.pow(r, 1/2.4) - 0.055) : 12.92 * r;
        g = (g > 0.0031308) ? (1.055 * Math.pow(g, 1/2.4) - 0.055) : 12.92 * g;
        b = (b > 0.0031308) ? (1.055 * Math.pow(b, 1/2.4) - 0.055) : 12.92 * b;

        return {
            r: Math.max(0, Math.min(255, r * 255)),
            g: Math.max(0, Math.min(255, g * 255)),
            b: Math.max(0, Math.min(255, b * 255))
        };
    }

    updateMorphCanvas(t) {
        const morphGroup = document.getElementById('morph-group');
        morphGroup.innerHTML = '';

        for (let i = 0; i < this.interpolators.length; i++) {
            const pathElement = document.createElementNS('http://www.w3.org/2000/svg', 'path');

            // Interpolate path
            const d = this.interpolators[i](t);
            pathElement.setAttribute('d', d);

            // Interpolate colors and stroke
            const colors = this.colorInterpolators[i];
            pathElement.setAttribute('fill', colors.fill(t));
            pathElement.setAttribute('stroke', colors.stroke(t));
            pathElement.setAttribute('stroke-width', colors.strokeWidth(t));

            morphGroup.appendChild(pathElement);
        }

        // Update progress display
        this.currentProgress = t;
        document.getElementById('progress').value = t * 100;
        document.getElementById('progress-value').textContent = Math.round(t * 100) + '%';
    }

    getEasingFunction(name) {
        const easings = {
            linear: t => t,
            easeInQuad: t => t * t,
            easeOutQuad: t => t * (2 - t),
            easeInOutQuad: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
            easeInCubic: t => t * t * t,
            easeOutCubic: t => (--t) * t * t + 1,
            easeInOutCubic: t => t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,
            easeInQuart: t => t * t * t * t,
            easeOutQuart: t => 1 - (--t) * t * t * t,
            easeInOutQuart: t => t < 0.5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t
        };

        return easings[name] || easings.linear;
    }

    animate(timestamp) {
        if (!this.isPlaying) return;

        if (!this.startTime) {
            this.startTime = timestamp - this.pausedTime;
        }

        const duration = parseFloat(document.getElementById('duration').value);
        const elapsed = timestamp - this.startTime;
        const rawProgress = Math.min(elapsed / duration, 1);

        // Apply easing function
        const easingName = document.getElementById('easing').value;
        const easingFunc = this.getEasingFunction(easingName);
        let progress = easingFunc(rawProgress);

        // Handle reverse on loop
        const reverseOnLoop = document.getElementById('reverse').checked;
        if (reverseOnLoop && this.shouldReverse) {
            progress = 1 - progress;
        }

        this.updateMorphCanvas(progress);

        if (rawProgress >= 1) {
            const loop = document.getElementById('loop').checked;
            if (loop) {
                this.startTime = timestamp;
                this.pausedTime = 0;
                if (reverseOnLoop) {
                    this.shouldReverse = !this.shouldReverse;
                }
            } else {
                this.stop();
                return;
            }
        }

        this.animationId = requestAnimationFrame((t) => this.animate(t));
    }

    play() {
        if (this.interpolators.length === 0) return;

        this.isPlaying = true;
        this.isPaused = false;
        this.shouldReverse = false;

        if (this.currentProgress >= 1) {
            this.reset();
        }

        document.getElementById('play-btn').disabled = true;
        document.getElementById('pause-btn').disabled = false;
        document.getElementById('progress').disabled = true;

        this.animationId = requestAnimationFrame((t) => this.animate(t));
    }

    pause() {
        this.isPlaying = false;
        this.isPaused = true;

        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }

        // Store the paused time
        this.pausedTime = this.currentProgress * parseFloat(document.getElementById('duration').value);
        this.startTime = null;

        document.getElementById('play-btn').disabled = false;
        document.getElementById('pause-btn').disabled = true;
        document.getElementById('progress').disabled = false;
    }

    stop() {
        this.isPlaying = false;
        this.isPaused = false;

        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }

        this.startTime = null;
        this.pausedTime = 0;

        document.getElementById('play-btn').disabled = false;
        document.getElementById('pause-btn').disabled = true;
        document.getElementById('progress').disabled = false;
    }

    reset() {
        this.stop();
        this.currentProgress = 0;
        this.updateMorphCanvas(0);
    }

    scrubToPosition(progress) {
        this.updateMorphCanvas(progress);
        this.pausedTime = progress * parseFloat(document.getElementById('duration').value);
    }

    enableControls() {
        document.getElementById('play-btn').disabled = false;
        document.getElementById('reset-btn').disabled = false;
        document.getElementById('progress').disabled = false;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.morphStudio = new SVGMorphStudio();
});
