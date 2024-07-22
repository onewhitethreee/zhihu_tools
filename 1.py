def replace_text(text, replacement_dict):
    # 遍历替换字典
    for key, value in replacement_dict.items():
        # 替换文本中的字符
        text = text.replace(key, value)
    return text
      src: url();

# 定义替换字典
replacement_dict = {
    "一": "对",
    "上": "动",
    "不": "和",
    "与": "中",
    "业": "上",
    "个": "要",
    "中": "了",
    "为": "法",
    "了": "多",
    "人": "学",
    "以": "是",
    "体": "二",
    "作": "能",
    "到": "个",
    "动": "大",
    "发": "到",
    "和": "在",
    "国": "生",
    "在": "人",
    "多": "国",
    "大": "以",
    "学": "业",
    "定": "心",
    "对": "为",
    "心": "与",
    "我": "有",
    "时": "定",
    "是": "发",
    "有": "这",
    "来": "说",
    "法": "不",
    "理": "来",
    "生": "体",
    "的": "理",
    "能": "我",
    "要": "作",
    "说": "的",
    "这": "时",
}

# 要替换的文本
original_text = "周晚，能他么和你有里就值三块钱？"

# 执行替换
replaced_text = replace_text(original_text, replacement_dict)

print("原始文本:", original_text)
print("替换后的文本:", replaced_text)
