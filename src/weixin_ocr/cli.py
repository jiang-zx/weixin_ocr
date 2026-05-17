import os
from .image_utils import image_split, image_resize
from .ocr_engine import LocalOCRProvider
from .wechat_parser import parse_dialogue

def process_image(filepath: str) -> list:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
        
    with open(filepath, "rb") as f:
        imageBytes = f.read()
        
    image_list = image_split(imageBytes)
    ocr_provider = LocalOCRProvider()
    
    all_dialogue = []
    
    for image in image_list:
        image = image_resize(image)
        results = ocr_provider.ocr(image)
        if not results: continue
        
        dialogue = parse_dialogue(results, image)
        all_dialogue.extend(dialogue)
        
    return all_dialogue

def main():
    import sys
    filename = "image/5e5eb526-90e7-4915-8e00-b363f8bce2b2.jpg"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        
    if not os.path.exists(filename):
        print(f"找不到文件: {filename}")
    else:
        print(f"正在解析: {filename} ...")
        try:
            dialogues = process_image(filename)
            with open('result.txt', 'w', encoding='utf-8') as f:
                for dia in dialogues:
                    print(dia)
                    f.write(dia + '\n')
            print(f"\n解析完成，结果已保存至 result.txt")
        except Exception as e:
            print(f"处理失败: {e}")

if __name__ == '__main__':
    main()
