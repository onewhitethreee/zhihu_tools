import os
import shutil
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode
from PIL import Image, ImageDraw, ImageFont

import ddddocr


class FontDocument:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)


class FontPreview:
    def __init__(self):
        self.font_meta = []
        self.font_dict = {}

    def open_font(self, file_path):
        return FontDocument(file_path)

    def parse_font(self, document):
        try:
            font = TTFont(document.file_path)
            cmap = font.getBestCmap()

            for unicode_val, glyph_name in cmap.items():
                try:
                    name = Unicode[unicode_val]
                except KeyError:
                    name = f"U+{unicode_val:04X}"

                glyph_info = {
                    "name": glyph_name,
                    "unicode": f"U+{unicode_val:04X}",
                    "unicode_value": unicode_val,
                    "character": chr(unicode_val),
                }

                self.font_meta.append(glyph_info)

            return font
        except Exception as e:
            raise Exception(f"Error parsing font: {str(e)}")

    def generate_image(self, font_file_path):
        # Set up image parameters
        glyph_size = 100
        glyphs_per_row = 10
        padding = 10

        # Calculate image dimensions
        num_glyphs = len(self.font_meta)
        num_rows = (num_glyphs + glyphs_per_row - 1) // glyphs_per_row
        img_width = (glyph_size + padding) * glyphs_per_row + padding
        img_height = (glyph_size + padding) * num_rows + padding

        # Create image and draw object
        image = Image.new("RGB", (img_width, img_height), color="white")
        draw = ImageDraw.Draw(image)

        # Load fonts
        try:
            preview_font = ImageFont.truetype(font_file_path, size=60)
        except IOError:
            preview_font = ImageFont.load_default()

        unicode_font = ImageFont.truetype("arial.ttf", size=12)

        # Draw glyphs
        for i, glyph in enumerate(self.font_meta):
            row = i // glyphs_per_row
            col = i % glyphs_per_row
            x = col * (glyph_size + padding) + padding
            y = row * (glyph_size + padding) + padding

            # Draw glyph box
            draw.rectangle([x, y, x + glyph_size, y + glyph_size], outline="black")

            # Draw glyph
            draw.text(
                (x + glyph_size // 2, y + glyph_size // 2 - 15),
                glyph["character"],
                font=preview_font,
                fill="black",
                anchor="mm",
            )

            # Draw Unicode value
            draw.text(
                (x + glyph_size // 2, y + glyph_size - 15),
                glyph["unicode"],
                font=unicode_font,
                fill="black",
                anchor="mm",
            )

        return image

    def generate_single_character_image(self, font_file_path, glyph_info, size=200):
        # 创建一个新的图像
        image = Image.new("RGB", (size, size), color="white")
        draw = ImageDraw.Draw(image)

        # 加载字体
        try:
            font = ImageFont.truetype(font_file_path, size=size // 2)
        except IOError:
            font = ImageFont.load_default()

        # 绘制字符
        draw.text(
            (size // 2, size // 2 - size // 8),
            glyph_info["character"],
            font=font,
            fill="black",
            anchor="mm",
        )

        # 绘制Unicode值
        unicode_font = ImageFont.truetype("arial.ttf", size=size // 10)
        draw.text(
            (size // 2, size - size // 10),
            glyph_info["unicode"],
            font=unicode_font,
            fill="black",
            anchor="mm",
        )

        return image

    def save_image(self, image, output_path):
        image.save(output_path)

    def generate_all_single_character_images(self, font_file_path, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for glyph_info in self.font_meta:
            image = self.generate_single_character_image(font_file_path, glyph_info)
            output_path = os.path.join(
                output_dir, f"{glyph_info['unicode'].split('+')[1]}.png"
            )
            self.save_image(image, output_path)

    def recognize_image(self, image_path):
        ocr = ddddocr.DdddOcr()
        images = os.listdir(image_path)
        for image in images:
            result = ocr.classification(
                open(os.path.join(image_path, image), "rb").read()
            )
            self.font_dict[chr(int(image.split(".")[0], 16))] = result

    def remove_files(self, path):
        if os.path.exists("font_preview.png"):
            os.remove("font_preview.png")
        shutil.rmtree(path)

    # 判断字典中是否有某个值为空，如果为空，填充一
    def fill_font_dict(self):

        for key, value in self.font_dict.items():
            if value == "":
                self.font_dict[key] = "一"

    # 获取字体信息 font_file_path: 字体文件路径 output_dir: 输出目录 remove_files: 是否删除生成的文件
    def preview(self, font_file_path, output_dir, remove_files=True):
        preview = FontPreview()
        font_document = preview.open_font(font_file_path)
        parsed_font = preview.parse_font(font_document)
        image = preview.generate_image(font_file_path)
        preview.save_image(image, "font_preview.png")
        preview.generate_all_single_character_images(font_file_path, output_dir)
        preview.recognize_image(output_dir)
        if remove_files:
            preview.remove_files(output_dir)
        preview.fill_font_dict()
        return preview.font_dict
