# ocr_decode
***
## 说明
    语言：python
    函数库：opencv、tesseract、libdmtx
    platfrom window10 x64
    图片中包含字符和二维码，二维码的信息对应字符，识别字符，解码二维码，将其信息做对比
***
## 环境配置（python工程中创建虚拟环境）
### 安装opencv 
    **pip install opencv-python**
### 安装tesserocr
    tesseract 是一个强大的ocr引擎
    tesseract https://digi.bib.uni-mannheim.de/tesseract/
    tesserocr 是对tesseract做的一层Python API封装，所以它的核心是tesseract,所以要先安装tesseraact
    tesserocr https://github.com/simonflueckiger/tesserocr-windows_build/releases
    **注意** ：tesseract 与 tesserocr 版本要一致，如果直接使用 *pip install tesserocr* 很可能会版本不一致，产生错误（别掉进这个坑）
    下载 *.whl* 文件，执行 **pip install tesserocr-2.2.2-cp36-cp36m-win_amd64.whl** (以tesseract 3.5.1 为例）
### 安装libdmtx
    libdmtx函数库对二维码进行解析
    **pip install pylibdmtx**
***


    
