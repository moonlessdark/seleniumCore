# seleniumCore
selnium二次封装


selenium为了用起来更方便，大家都喜欢二次封装。  
但是，每个人的使用习惯不同，封装的逻辑也不一样，所以会给别人造成一种二次封装的效果并不好。  
针对这种情况，建议按自己的习惯进行封装，自己用  

在release下载了文件后，执行pip安装命令即可。  
例如：  
    pip install D://seleniumCore-0.1.tar.gz

本项目只是将元素等待加入find方法中，没有什么特别的东西

引用：
from seleniumCore import getDriver, basePageByH5, basePageByWeb
from seleniumCore.common.browser_by import BrowserBy
from selenium.webdriver.common.by import By

# 初始化驱动信息
getDriver(driver_path='驱动路径', driver_type='web or h5', browser_type=BrowserBy.Chrome)
# 打开网页
basePageByWeb().get_url('https://www.baidu.com')
# 输入搜索文本
basePageByWeb().send_text(By.ID, 'kw', '输入测试文本')
# 点击查询按钮
basePageByWeb().click(By.ID, 'su')
