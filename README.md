# Text2Image 文本渲染插件

这是一个将文本渲染成图片的插件，支持自定义背景图片、字体、颜色和样式。

## 功能特性

- 支持自定义背景图片或随机背景
- 支持保持背景图片原始比例
- 支持背景图片虚化和透明度调整
- 支持自定义字体和字体大小
- 支持文本颜色自定义
- 支持文本样式标记（字号和颜色）
- 支持文本换行
- 支持相对路径配置

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

### 基本配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| command_name | 插件命令名称 | 渲染 |
| text | 要渲染的文本内容 | 示例文本 |
| width | 图片宽度(像素) | 800 |
| height | 图片高度(像素) | 600 |
| margin | 文本边距(像素) | 50 |

### 背景配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| use_random_background | 是否使用随机背景图片 | false |
| background_folder | 背景图片文件夹路径 | .\图片 |
| background_image | 指定背景图片路径 | .\图片\1c2aa4d0895817a56a9d13c74d472e88.jpg |
| maintain_aspect_ratio | 保持背景图片比例 | true |
| blur_radius | 背景图片虚化程度(0-100) | 0 |
| background_opacity | 背景图片透明度(0-100) | 100 |

### 字体配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| font_size | 默认字体大小 | 32 |
| font_path | 字体文件路径 | .\字体\源古宋体\源古宋體-F.ttf |
| text_color | 默认文本颜色 | black |

## 使用说明

### 文本样式标记

在文本中使用 `[字号,颜色]` 格式的标记来设置样式，例如：
```
这是普通文本[32,red]这是红色32号字[48,blue]这是蓝色48号字
```

### 换行

使用 `\n` 进行换行，例如：
```
这是第一行\n这是第二行
```

### 路径配置

支持相对路径和绝对路径：
- 相对路径示例：`.\图片`、`.\字体\arial.ttf`
- 绝对路径示例：`C:\图片`、`C:\字体\arial.ttf`

## 使用示例

1. 基本使用：
```json
{
    "text": "Hello World",
    "font_size": 32,
    "text_color": "black"
}
```

2. 使用样式标记：
```json
{
    "text": "这是普通文本[32,red]这是红色32号字[48,blue]这是蓝色48号字",
    "font_size": 24,
    "text_color": "black"
}
```

3. 使用随机背景：
```json
{
    "text": "Hello World",
    "use_random_background": true,
    "background_folder": ".\\图片"
}
```

4. 自定义背景效果：
```json
{
    "text": "Hello World",
    "background_image": ".\\图片\\background.jpg",
    "maintain_aspect_ratio": true,
    "blur_radius": 10,
    "background_opacity": 80
}
```

## 注意事项

1. 字体文件必须是 TTF 格式
2. 背景图片支持 PNG、JPG、JPEG、GIF、BMP 格式
3. 颜色可以使用颜色名称（如 "red"、"blue"）或十六进制颜色代码（如 "#FF0000"）
4. 使用相对路径时，路径是相对于插件目录的
