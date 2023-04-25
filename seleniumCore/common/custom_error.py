# encoding=utf-8


class SeleniumException(Exception):

    def __init__(self):
        pass


# 常见做法定义异常基类,然后在派生不同类型的异常

class FindError(SeleniumException):
    """
    查找元素是否存在，不判断元素是否显示在页面上
    """
    def __init__(self, ele_value=None):
        super(FindError, self).__init__()
        self.message = "未成功在页面上找到元素" + ele_value


class VisibilityError(SeleniumException):
    """
    元素是否已经渲染在页面上
    """
    def __init__(self, ele_value=None):
        super(VisibilityError, self).__init__()
        self.message = "元素" + ele_value + '未渲染在页面上'


class InVisibilityError(SeleniumException):
    """
    元素是否隐藏不显示在页面上
    """
    def __init__(self, ele_value=None):
        super(InVisibilityError, self).__init__()
        self.message = "元素" + ele_value + '依旧处于显示状态，没有隐藏'


class SendKeyError(SeleniumException):
    """
    元素是否可以输入信息
    """
    def __init__(self, ele_value=None):
        super(SendKeyError, self).__init__()
        self.message = "元素信息 " + ele_value + "的input标签赋值失败"


class ClickError(SeleniumException):
    """
    元素是否可以被点击
    """
    def __init__(self, ele_value=None):
        super(ClickError, self).__init__()
        self.message = "元素" + ele_value + "不可点击"


class ClearError(SeleniumException):
    """
    文本框是否可以被clear
    """
    def __init__(self, ele_value=None):
        super(ClearError, self).__init__()
        self.message = "信息" + ele_value + "清除失败"


class SelectError(SeleniumException):
    """
    下拉框是否可以被选择
    """
    def __init__(self, ele_value=None):
        super(SelectError, self).__init__()
        self.message = "下拉框" + ele_value + "选择失败"
