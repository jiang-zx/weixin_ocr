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
    # 支持半角 (:) 和全角 (：) 冒号的时间匹配
    if re.findall(r'.*\d[:：]\d\d.*', text): return True
    # 匹配日期，如 "2022年11月30日"
    if re.findall(r'.*\d{4}年\d{1,2}月\d{1,2}日.*', text): return True
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
    WIDTH = image.shape[1]
    
    for item in ocr_results:
        text = item['text']
        box = item['box']
        
        # 提取边界
        x_min = min([pt[0] for pt in box])
        x_max = max([pt[0] for pt in box])
        y_min = min([pt[1] for pt in box])
        y_max = max([pt[1] for pt in box])
        
        # 1. 过滤掉顶部信息（如个性签名、状态等）
        if y_min < 100:
            continue
            
        # 2. 过滤系统消息
        if is_system_msg(text):
            if item == ocr_results[-1] and line_text:
                dialog.append(line_text)
            continue
            
        color = get_color_from_box(box, image)
        y = box[0][1] # 左上角 Y 坐标
        
        # 3. 稳健的角色判断逻辑
        is_self = False
        # 如果文本框明显靠右且不跨越左侧 avatar 区域，判定为自己
        if x_max > WIDTH - 100 and x_min > 150:
            is_self = True
        # 如果文本框明显靠左且不跨越右侧 avatar 区域，判定为好友
        elif x_min < 110 and x_max < WIDTH - 150:
            is_self = False
        # 对于长文本或位置模糊的情况，使用颜色判定
        else:
            is_self = color[0] < 200 # 绿色 B 通道较小
            
        if is_self:
            if line_text == '':
                line_text = '自己:' + text
            elif '自己:' in line_text and y - y_point < 40:
                line_text += text
            else:
                if line_text: dialog.append(line_text)
                line_text = '自己:' + text
        else: # 好友
            if line_text == '':
                line_text = '好友:' + text
            elif '好友:' in line_text and y - y_point < 40:
                line_text += text
            else:
                if line_text: dialog.append(line_text)
                line_text = '好友:' + text
                
        y_point = y
        if item == ocr_results[-1] and line_text:
            dialog.append(line_text)
            
    return dialog
