# MS_ppm_alarm
use python to scan .raw File "LockMass m/z-Correction" from Thermo mass spectrum rawdata. If ppm>4.5 will send a message to dingtalk.  
使用python脚本从Thermo质谱仪产生的原始数据中获取“LockMass m/z-Correction”值，并计算质量轴偏离程度ppm平均值
如果ppm>4.5，则发送钉钉提醒
# Set Lock Mass Method
Need to set the Lock Mass List in the mass acquisition method, usually in the wash between samples.  
需要在质谱采集方法中设置Lock Mass List，通常在样品之间的wash方法里  
Polydimethylcyclosiloxanes are ubiquitously present in ambient air. \(Mass difference 74.018793\)  
聚二甲基环硅氧烷普遍存在于环境空气中。（其质量差异74.018793）在蛋白质谱分析模式中以m/z=445.12003丰度最高  
![Polydimethylcyclosiloxanes](http://www.proteomicsresource.washington.edu/images/esi_background_02.png)
|Polysiloxanes Mono mass \[M+H\]<sup>+</sup>|Polarity|Formula|
|:-:|:-:|:-:|
|445.12003|Positive|\[\(Si\[CH<sub>3</sub>\]<sub>2</sub>O\)<sub>6</sub><sup>+</sup>H\]<sup>+</sup>|
|371.10124|Positive|\[\(Si\[CH<sub>3</sub>\]<sub>2</sub>O\)<sub>5</sub><sup>+</sup>H\]<sup>+</sup>|
|519.13883|Positive|\[\(Si\[CH<sub>3</sub>\]<sub>2</sub>O\)<sub>7</sub><sup>+</sup>H\]<sup>+</sup>|
|593.15762|Positive|\[\(Si\[CH<sub>3</sub>\]<sub>2</sub>O\)<sub>8</sub><sup>+</sup>H\]<sup>+</sup>|
|667.17641|Positive|\[\(Si\[CH<sub>3</sub>\]<sub>2</sub>O\)<sub>9</sub><sup>+</sup>H\]<sup>+</sup>|
# Notice
I AM A NEWBEE
