from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import textwrap
import re
import random

def normalize_path(path: str) -> str:
    """标准化路径，支持相对路径格式"""
    if not path:
        return ""
    try:
        # 获取插件目录的绝对路径
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 处理路径
        if path.startswith('.'):
            # 移除开头的点
            path = path.lstrip('.')
            # 移除开头的斜杠或反斜杠
            path = path.lstrip('\\/')
            # 构建完整路径
            full_path = os.path.join(plugin_dir, path)
            # 转换为绝对路径
            full_path = os.path.abspath(full_path)
            logger.info(f"相对路径转换: {path} -> {full_path}")
            return full_path
        else:
            # 如果不是相对路径，直接返回原始路径
            return path
    except Exception as e:
        logger.error(f"路径处理错误: {str(e)}, 原始路径: {path}")
        return path

def resize_image_with_aspect_ratio(img: Image.Image, target_width: int, target_height: int, maintain_aspect_ratio: bool = True) -> Image.Image:
    """调整图片大小，可选择是否保持宽高比"""
    if not maintain_aspect_ratio:
        return img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # 计算原始宽高比
    original_ratio = img.width / img.height
    target_ratio = target_width / target_height
    
    if original_ratio > target_ratio:
        # 图片更宽，以高度为基准
        new_height = target_height
        new_width = int(new_height * original_ratio)
    else:
        # 图片更高，以宽度为基准
        new_width = target_width
        new_height = int(new_width / original_ratio)
    
    # 调整图片大小
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 创建新的白色背景图片
    background = Image.new('RGB', (target_width, target_height), 'white')
    
    # 计算居中位置
    x = (target_width - new_width) // 2
    y = (target_height - new_height) // 2
    
    # 将调整后的图片粘贴到背景上
    background.paste(resized_img, (x, y))
    
    return background

@register("text2image", "wuyan1003", "将文本渲染成图片的插件", "1.0.0")
class Text2ImagePlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.command_name = config.get('command_name', 'text2image')
        logger.info(f"Text2Image plugin initialized with command: {self.command_name}")
        
        # 动态注册命令
        @filter.command(self.command_name)
        async def text2image(self, event: AstrMessageEvent):
            '''将配置的文本渲染成图片'''
            try:
                # 获取配置
                text = self.config.get('text', '')
                use_random_background = self.config.get('use_random_background', False)
                background_folder = normalize_path(self.config.get('background_folder', ''))
                bg_path = normalize_path(self.config.get('background_image', ''))
                width = self.config.get('width', 800)
                height = self.config.get('height', 600)
                default_font_size = self.config.get('font_size', 32)
                font_path = normalize_path(self.config.get('font_path', ''))
                default_text_color = self.config.get('text_color', 'black')
                margin = self.config.get('margin', 50)
                blur_radius = self.config.get('blur_radius', 0)
                background_opacity = self.config.get('background_opacity', 100)
                maintain_aspect_ratio = self.config.get('maintain_aspect_ratio', True)

                # 记录配置的路径信息
                logger.info(f"字体路径: {font_path}")
                logger.info(f"背景文件夹路径: {background_folder}")
                logger.info(f"背景图片路径: {bg_path}")

                if not text:
                    yield event.plain_result("请在配置文件中设置要渲染的文本内容")
                    return

                # 获取背景图片
                if use_random_background and background_folder:
                    if not os.path.exists(background_folder):
                        yield event.plain_result(f"背景图片文件夹不存在: {background_folder}")
                        return
                    
                    # 获取文件夹中的所有图片文件
                    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
                    image_files = [f for f in os.listdir(background_folder) 
                                 if f.lower().endswith(image_extensions)]
                    
                    if not image_files:
                        yield event.plain_result(f"背景图片文件夹中没有图片: {background_folder}")
                        return
                    
                    # 随机选择一张图片
                    random_image = random.choice(image_files)
                    bg_path = os.path.join(background_folder, random_image)
                    logger.info(f"使用随机背景图片: {bg_path}")

                # 创建图片
                if bg_path and os.path.exists(bg_path):
                    # 使用背景图片
                    img = Image.open(bg_path)
                    # 使用新的调整大小函数
                    img = resize_image_with_aspect_ratio(img, width, height, maintain_aspect_ratio)
                    
                    # 应用虚化效果
                    if blur_radius > 0:
                        img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius/10))
                    
                    # 应用透明度
                    if background_opacity < 100:
                        # 创建一个白色背景
                        white_bg = Image.new('RGB', (width, height), 'white')
                        # 将背景图片转换为RGBA模式
                        img = img.convert('RGBA')
                        # 调整透明度
                        opacity = background_opacity / 100.0
                        img.putalpha(int(255 * opacity))
                        # 将背景图片合成到白色背景上
                        white_bg.paste(img, (0, 0), img)
                        img = white_bg
                else:
                    # 创建纯色背景
                    img = Image.new('RGB', (width, height), color='white')

                # 创建绘图对象
                draw = ImageDraw.Draw(img)

                # 设置默认字体
                try:
                    if font_path and os.path.exists(font_path):
                        logger.info(f"使用自定义字体: {font_path}")
                        default_font = ImageFont.truetype(font_path, default_font_size)
                    else:
                        logger.warning(f"字体文件不存在，使用系统默认字体: {font_path}")
                        # 尝试使用系统字体
                        default_font = ImageFont.truetype("arial.ttf", default_font_size)
                except Exception as e:
                    logger.error(f"加载字体失败: {str(e)}")
                    default_font = ImageFont.load_default()

                # 解析文本样式
                text_segments = []
                current_style = {"size": default_font_size, "color": default_text_color}
                
                # 使用正则表达式匹配样式标记
                style_pattern = r'\[(\d+),([^\]]+)\]'
                
                # 先处理所有样式标记，记录它们的位置和样式
                style_positions = []
                offset = 0  # 用于跟踪已移除的样式标记长度
                for match in re.finditer(style_pattern, text):
                    # 计算实际位置（考虑已移除的样式标记）
                    actual_pos = match.start() - offset
                    style_positions.append({
                        'pos': actual_pos,
                        'size': int(match.group(1)),
                        'color': match.group(2)
                    })
                    # 更新偏移量（加上当前样式标记的长度）
                    offset += len(match.group(0))
                
                # 移除所有样式标记
                clean_text = re.sub(style_pattern, '', text)
                
                # 按样式标记分割文本
                last_pos = 0
                for style in style_positions:
                    if style['pos'] > last_pos:
                        # 添加样式标记之前的文本
                        text_segments.append({
                            "text": clean_text[last_pos:style['pos']],
                            "size": current_style["size"],
                            "color": current_style["color"]
                        })
                    # 更新当前样式
                    current_style["size"] = style['size']
                    current_style["color"] = style['color']
                    last_pos = style['pos']
                
                # 添加最后一段文本
                if last_pos < len(clean_text):
                    text_segments.append({
                        "text": clean_text[last_pos:],
                        "size": current_style["size"],
                        "color": current_style["color"]
                    })
                
                # 处理换行符
                final_segments = []
                for segment in text_segments:
                    lines = segment["text"].split('\\n')
                    for line in lines:
                        if line:  # 只添加非空行
                            final_segments.append({
                                "text": line,
                                "size": segment["size"],
                                "color": segment["color"]
                            })

                # 绘制文本
                offset = margin
                for segment in final_segments:
                    # 为每个文本段创建对应的字体
                    try:
                        if font_path and os.path.exists(font_path):
                            font = ImageFont.truetype(font_path, segment["size"])
                        else:
                            font = ImageFont.truetype("arial.ttf", segment["size"])
                    except:
                        font = ImageFont.load_default()

                    # 计算文本换行
                    chars_per_line = int((width - 2 * margin) / (segment["size"] * 0.6))
                    wrapped_text = textwrap.wrap(segment["text"], width=chars_per_line)

                    # 绘制文本
                    for line in wrapped_text:
                        bbox = font.getbbox(line)
                        text_height = bbox[3] - bbox[1]
                        draw.text((margin, offset), line, font=font, fill=segment["color"])
                        offset += text_height + 10

                # 保存图片
                output_path = "temp_text2image.png"
                img.save(output_path)

                # 发送图片
                yield event.image_result(output_path)

                # 清理临时文件
                if os.path.exists(output_path):
                    os.remove(output_path)

            except Exception as e:
                logger.error(f"Text2Image error: {str(e)}")
                yield event.plain_result(f"渲染图片时发生错误: {str(e)}")

        # 将命令处理函数绑定到实例
        self.text2image = text2image.__get__(self)

    async def terminate(self):
        '''插件终止时的清理工作'''
        pass
