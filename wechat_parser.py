import re
import numpy as np

def get_color_from_box(box, image):
    """
    为了避免采样到文字的黑色墨迹，从 Bounding Box 左侧边缘外进行颜色采样。
    box 格式: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] (左上, 右上, 右下, 左下)
    """
    x_min = min([pt[0] for pt in box])
    y_min = min([pt[1] for pt in box])
    y_max = max([pt[1] for pt in box])
    
    # 采样点：高度居中，水平方向稍微偏左
    sample_y = int((y_min + y_max) / 2)
    sample_x = max(0, int(x_min) - 5)
    
    # Ensure within bounds
    sample_y = min(sample_y, image.shape[0] - 1)
    sample_x = min(sample_x, image.shape[1] - 1)
    
    color = image[sample_y][sample_x]
    return color

def is_system_msg(text):
    sys_msgs = ['...', '我通过了你的朋友验证请求，现在', '我们可以开始聊天了', '以上是打招呼的内容', '三', '+', '你撤回了一条消息', 'HD', ':', '按住说话']
    if text in sys_msgs: return True
    if re.findall(r'.*\d:\d\d.*', text): return True
    if re.findall(r'(\d{0,1})月\d{0,1}日.*', text): return True
    try:
        battery_num = int(text)
        if 0 < battery_num <= 100: return True
    except:
        pass
    return False

def parse_dialogue(ocr_results, image):
    dialog = []
    line_text = ''
    y_point = 0
    
    for item in ocr_results:
        text = item['text']
        box = item['box']
        
        if is_system_msg(text):
            if item == ocr_results[-1] and line_text:
                dialog.append(line_text)
            continue
            
        color = get_color_from_box(box, image)
        y = box[0][1] # 左上角 Y 坐标
        
        # 颜色逻辑：利用 OpenCV BGR 格式
        # 白色: color[0] (Blue通道) > 200 -> 好友
        # 绿色: color[0] (Blue通道) < 150 -> 自己
        
        if color[0] > 200: # 好友 (白底)
            if line_text == '':
                line_text = '好友:' + text
            elif y - y_point < 40:
                line_text += text
            else:
                dialog.append(line_text)
                line_text = '好友:' + text
        elif color[0] < 150: # 自己 (绿底)
            if line_text == '':
                line_text = '自己:' + text
            elif y - y_point < 40:
                line_text += text
            else:
                dialog.append(line_text)
                line_text = '自己:' + text
                
        y_point = y
        if item == ocr_results[-1] and line_text:
            dialog.append(line_text)
            
    return dialog
