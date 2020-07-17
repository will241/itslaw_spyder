# itslaw_spyder
用selenium+Chrome在无讼网上对案例进行爬取。

itslaw_case_id.py 用来获取网站中每个案例独有的ID号，并将他们存储为csv。  
itslaw_case_detail.py 用来获取每个案例及被告人的相关信息，并将他们存储为csv。  
Data_Cleaning.py 对爬取的数据进行数据清洗。  
model.py 简单地线性模型对判刑时间进行预测和验证。  
