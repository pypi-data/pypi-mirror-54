from distutils.core import setup
#导入setup函数
 
setup(
	  name="mm_test", #模块的名称
	  version="1.0",#版本号，每次修改代码的时候，可以改一下
	  description="test from xuancloud@gavinzhang",#描述
	  author="牛牛",#作者
	  author_email="xuancloud@163.com",#联系邮箱
	  url="http://www.nnzhp.cn",#你的主页
	  py_modules=['mm_test.my_test','mm_test.my_python']#这个是下面有哪些模块可以用
	  )
