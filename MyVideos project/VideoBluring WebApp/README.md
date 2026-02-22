# Image Blur Tool - Web Application

A fully functional, client-side web application that allows users to apply blur effects to images with real-time preview and download capabilities.

## Features

✨ **Key Features:**
- 🖼️ Drag-and-drop or click-to-upload image interface
- 👁️ Real-time before/after comparison view
- 🎚️ Interactive blur intensity slider (0-20 pixels)
- ⬇️ Download blurred images in original format
- 🔒 100% client-side processing (privacy-focused)
- 📱 Fully responsive design (desktop and mobile)
- ⚡ Optimized performance for images up to 10MB

## Supported Formats

- JPG/JPEG
- PNG
- GIF
- WebP

## How to Use

1. **Open the Application**
   - Simply open `index.html` in any modern web browser
   - No installation or server required!

2. **Upload an Image**
   - Drag and drop an image onto the upload area, or
   - Click the upload area to browse and select an image

3. **Adjust Blur Intensity**
   - Use the slider to adjust blur from 0 to 20 pixels
   - See the effect in real-time on the right side

4. **Download Your Image**
   - Click "Download Blurred Image" to save the result
   - The image will be saved in its original format

5. **Start Over**
   - Click "Upload New Image" to process a different image

## Technical Details

### Technologies Used
- **HTML5** - Structure and Canvas API for image processing
- **CSS3** - Modern, responsive styling with gradients and animations
- **Vanilla JavaScript** - No dependencies, pure client-side processing

### Browser Compatibility
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

### Performance Optimization
- Images are automatically resized for preview (max 500px width)
- Full-resolution processing for downloads
- Efficient Canvas API blur implementation
- RequestAnimationFrame for smooth slider updates

## Privacy & Security

🔒 **Your images never leave your device!**
- All processing happens locally in your browser
- No data is sent to any server
- No tracking or analytics
- Completely offline-capable

## File Structure

```
VideoBluring WebApp/
├── index.html      # Main HTML structure
├── styles.css      # Styling and responsive design
├── script.js       # Image processing logic
└── README.md       # This file
```

## Error Handling

The application includes comprehensive error handling for:
- Unsupported file formats
- Files exceeding 10MB size limit
- Failed image loading
- Download errors

## Customization

You can easily customize the application by modifying:
- **Color scheme**: Edit CSS variables in `styles.css`
- **Max blur value**: Change `max` attribute in the slider (line 67 in `index.html`)
- **Max file size**: Modify `MAX_FILE_SIZE` constant in `script.js`
- **Preview dimensions**: Adjust `maxWidth` in `setupCanvases()` function

## License

This project is open source and available for personal and commercial use.

## Credits

Created with ❤️ for easy image blurring

---

**Note**: For best results, use images with good resolution. Very small images may not show significant blur effects.