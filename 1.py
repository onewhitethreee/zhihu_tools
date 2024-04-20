from fontTools.ttLib import TTFont

base_font = TTFont("03337c30.woff")
print(base_font)

base_list = base_font.getGlyphOrder()[2:]

print(base_list)

# 假设抓取到的评分字符串如下所示
# &#xe6e0;&#xe5bf;&#xe415;&#xf078;&#xf078;
font_str = "&#xe6e0;&#xe5bf;&#xe415;&#xf078;&#xf078;"

font_list = font_str.split(";")[:-1]
font_list = ["uni" + _[3:].upper() for _ in font_list]

font_dict = {
    "uniE415": "3",
    "uniF41A": "8",
    "uniF078": "7",
    "uniE5BF": "0",
    "uniE36C": "9",
    "uniF8DF": "1",
    "uniE5A5": "6",
    "uniEF4D": "4",
    "uniE6E0": "2",
    "uniED3D": "5",
}

real_numm = [font_dict[f] for f in font_list]
print(real_numm)
