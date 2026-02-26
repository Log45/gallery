import os
import rawpy
from PIL import Image

from gallery.file_modules import FileModule
from gallery.util import hash_file

# Thumbnail size for RAW previews (higher than default 256 for sharper previews)
RAW_THUMBNAIL_SIZE = 1024
RAW_JPEG_QUALITY = 90


class NEFFile(FileModule):
    def __init__(self, file_path, dir_path):
        FileModule.__init__(self, file_path, dir_path)
        self.mime_type = "image/x-nikon-nef"

        self.generate_thumbnail()

    def generate_thumbnail(self):
        self.thumbnail_uuid = hash_file(self.file_path) + ".jpg"
        thumb_path = os.path.join(self.dir_path, self.thumbnail_uuid)

        with rawpy.imread(self.file_path) as raw:
            # Full resolution (half_size=False), 8-bit for smaller output
            rgb = raw.postprocess(output_bps=8, half_size=False)

            h, w, _ = rgb.shape
            size = min(h, w)
            y = (h - size) // 2
            x = (w - size) // 2
            rgb = rgb[y:y+size, x:x+size]

            # Resize to higher-res thumbnail and save with good quality
            img = Image.fromarray(rgb)
            img = img.resize((RAW_THUMBNAIL_SIZE, RAW_THUMBNAIL_SIZE), Image.Resampling.LANCZOS)
            img.save(thumb_path, "JPEG", quality=RAW_JPEG_QUALITY)