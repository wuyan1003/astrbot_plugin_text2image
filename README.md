# 🎨 Text2Image 文本渲染插件  
**一款灵活高效的文本转图片工具，让文字呈现更具视觉张力！**  


## 📌 核心功能亮点  
| **功能模块**       | **详细特性**                                                                 |  
|--------------------|-----------------------------------------------------------------------------|  
| **背景定制**       | - 支持自定义背景图片（PNG/JPG/GIF等格式）<br>- 随机背景模式<br>- 保留图片原始比例<br>- 虚化强度与透明度调节 |  
| **字体与样式**     | - 自定义TTF字体文件<br>- 动态调整字体大小<br>- 文本颜色支持名称/十六进制代码<br>- 局部样式标记（如 `[字号,颜色]`） |  
| **文本处理**       | - 自动换行与手动换行（`\n`）<br>- 相对路径与绝对路径混合配置<br>- 插件级路径隔离（基于插件目录） |  


## 🌟 效果演示  
[![示例图片1](https://github.com/wuyan1003/astrbot_plugin_text2image/blob/master/%E7%A4%BA%E4%BE%8B%E5%9B%BE%E7%89%87/1.jpg)](https://github.com/wuyan1003/astrbot_plugin_text2image/blob/master/%E7%A4%BA%E4%BE%8B%E5%9B%BE%E7%89%87/1.jpg)  
[![示例图片2](https://github.com/wuyan1003/astrbot_plugin_text2image/blob/master/%E7%A4%BA%E4%BE%8B%E5%9B%BE%E7%89%87/2.jpg)](https://github.com/wuyan1003/astrbot_plugin_text2image/blob/master/%E7%A4%BA%E4%BE%8B%E5%9B%BE%E7%89%87/2.jpg)  
[![示例图片3](https://github.com/wuyan1003/astrbot_plugin_text2image/blob/master/%E7%A4%BA%E4%BE%8B%E5%9B%BE%E7%89%87/3.jpg)](https://github.com/wuyan1003/astrbot_plugin_text2image/blob/master/%E7%A4%BA%E4%BE%8B%E5%9B%BE%E7%89%87/3.jpg)  


## 🛠️ 安装与配置指南  

### 🔧 依赖安装  
**自动安装**：通过市场安装插件后，astrbot将自动拉取所需依赖。  
**手动安装**（如遇异常）：  
```bash  
# 进入astrbot虚拟环境  
pip install -r requirements.txt  
```  

### 📁 配置说明  
1. **基础配置**：  
   - 插件已预打包基础文件，安装后即可直接使用。  
   - 配置文件路径：`插件目录/config.yaml`（可自定义背景/字体默认路径）。  

2. **路径规则**：  
   - **相对路径**：基于插件目录（例：`./fonts/微软雅黑.ttf`）。  
   - **绝对路径**：完整系统路径（例：`D:/resources/images/background.jpg`）。  


## 📝 使用手册  

### ✍️ 文本样式标记语法  
通过 `[字号,颜色]` 实现局部样式控制，示例：  
```text  
普通文本[32,red]红色32号字[48,#00FFFF]青色48号字[64,rgb(50,150,250)]RGB色值字  
```  

### ↩️ 换行操作  
使用 `\n` 强制换行，示例：  
```text  
第一行内容\n第二行内容（自动换行）  
```  

### 📄 支持格式说明  
| **资源类型** | **支持格式**                          | **注意事项**                     |  
|--------------|---------------------------------------|----------------------------------|  
| 字体文件     | TTF                                   | 需放置于配置路径下               |  
| 背景图片     | PNG/JPG/JPEG/GIF/BMP                  | GIF仅支持静态帧，动态效果将被忽略|  
| 颜色值       | 英文名称（red）/ 十六进制（#FF0000）/ RGB值 | 不支持透明通道（如rgba格式）     |  


## ⚠️ 重要提示  
1. **字体兼容性**：仅支持TTF格式，建议使用通用字体（如思源黑体、Arial）避免渲染异常。  
2. **路径权限**：确保插件对配置路径有读写权限（尤其是Windows系统）。  
3. **性能优化**：大尺寸背景图或复杂样式可能影响渲染速度，建议预处理图片尺寸。  





如需进一步定制或反馈问题，欢迎访问 [项目仓库](https://github.com/wuyan1003/astrbot_plugin_text2image) 提交Issue！ 🚀