#-*-coding:utf-8-*-
#文件名: ch.py
from pylab import mpl 
def set_ch(): 
	mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体 ?
	mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题