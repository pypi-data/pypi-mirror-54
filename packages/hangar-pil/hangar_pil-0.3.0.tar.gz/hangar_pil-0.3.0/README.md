# hangar_pil
Hangar PIL plugin

hangar_pil provides `load`, `save` and `board_show` methods and supports jpg, jpeg, png, ppm, bmp, pgm, tif, tiff and webp files

## installation
```bash
pip install hangar_pil
```

## Usage - CLI
Examples here are with minimal options possible, checkout the hangar documentation for all available options

- Importing a directory full of images into hangar. Hangar uses hangar_pil to figure out which file formats are supported by hangar_pil and auto infer plugin at runtime. Note that `--height` and `--width` are plugin specific arguments
```bash
 hangar import aset images_directory --height 299 --width 299
 ```

- Exporting: This exports the sample to the current directory
```bash
hangar export aset --format jpg --sample sample_name
```

## Usage - programmatically