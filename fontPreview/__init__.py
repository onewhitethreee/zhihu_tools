import os
import shutil
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode
from PIL import Image, ImageDraw, ImageFont
import logging

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import ddddocr


class FontDocument:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)


class FontPreview:
    def __init__(self):
        self.font_meta = []
        self.font_dict = {}
        self.market_spider = None  # 用于关联MarketSpider实例

    def set_market_spider(self, market_spider):
        # 设置MarketSpider实例，用于重新请求文章
        self.market_spider = market_spider

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
        retry_count = 3  # 最大重试次数
        for image in images:
            result = ocr.classification(open(os.path.join(image_path, image), "rb").read())
            if not result:  # 如果识别结果为空
                logging.warning(f"图片 {image} 识别结果为空，尝试重新请求文章...")
                for attempt in range(retry_count):
                    self.market_spider.re_fetch_article()  # 重新请求文章
                    result = ocr.classification(open(os.path.join(image_path, image), "rb").read())
                    if result:  # 如果重新识别成功
                        break
                    logging.warning(f"第 {attempt + 1} 次重试失败")
                if not result:  # 如果重试后仍然为空
                    logging.error(f"图片 {image} 识别结果仍然为空，跳过该字符")
                    result = "一"  # 设置为默认值
            self.font_dict[chr(int(image.split(".")[0], 16))] = result

    def remove_files(self, path):
        if os.path.exists("font_preview.png"):
            os.remove("font_preview.png")
        # if os.path.exists('font.woff'):
        # os.remove('font.woff')
        shutil.rmtree(path)

    def fill_font_dict(self):
        for key, value in self.font_dict.items():
            if value == "":
                self.font_dict[key] = "一"
                # 或者根据需求设置默认值
                # self.font_dict[key] = "?"

    def correct_font_dict(self):
        # 检查字体映射表，将所有的“二”替换为“一”。
        for key, value in self.font_dict.items():
            if value == "二":
                self.font_dict[key] = "一"
                logging.info("字体映射表已检查并修正。")

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
        preview.correct_font_dict()  # 调用修正方法
        return preview.font_dict

