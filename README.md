# ocr_decode
## 说明
语言：python  
函数库：opencv、tesseract、libdmtx  
platfrom: window10 x64  
图片中包含字符和二维码，二维码的信息对应字符，识别字符，解码二维码，将其信息做对比

## 环境配置（python工程中创建虚拟环境）
### 安装opencv 
`pip install opencv-python`
### 安装tesserocr
tesseract [下载地址](https://digi.bib.uni-mannheim.de/tesseract/) 是一个强大的ocr引擎    
tesserocr [下载地址](https://github.com/simonflueckiger/tesserocr-windows_build/releases) 是对tesseract做的一层Python API封装，所以它的核心是tesseract,所以要先安装tesseraact   
**注意** ：tesseract 与 tesserocr 版本要一致，如果直接使用 `pip install tesserocr` 很可能会版本不一致，产生错误（别掉进这个坑）  
下载 _.whl_ 文件，执行 `pip install tesserocr-2.2.2-cp36-cp36m-win_amd64.whl` (以tesseract 3.5.1 为例）
### 安装libdmtx
libdmtx函数库对二维码进行解析  
`pip install pylibdmtx`

## 处理流程
### 图像样张
![待处理图片](https://raw.githubusercontent.com/Plinys/ocr_decode/master/img/MER-504-10GM-P(192.168.1.60%5B00-21-49-00-F0-C5%5D)_2018-08-02_10_08_30_944-0.bmp)
### 预处理
转换为灰度图  
自适应阈值分割--oust  
中值滤波，去除散粒噪声
### 分离二维码与字符区域，做特征提取
采用较大kernal 进行膨胀处理，使二维码成为一个完整区域  
寻找轮廓，找出二维码区域对应轮廓区域，分离出来，返回二维码img和字符img
### 字符识别
寻找字符img的轮廓，得出轮廓区域的boundrect,每个boundrect 包含一个字符  
字符识别需要按照顺序进行，boundrect的存储结构并不按照顺序，因此需要利用sorted()进行排序  
利用tesserocr进行单个字符识别
### 二维码重建与识别
二维码质量过于低，无法直接进行识别，因此需要根据特征进行重建  
此二维码为18×18的矩阵块组成，因此可以遍历每个矩阵块，判断矩阵块应该是黑色还是白色部分，通过此过程进行重建
![二维码](https://github.com/Plinys/ocr_decode/blob/master/rebuilt_dm.png)


    
