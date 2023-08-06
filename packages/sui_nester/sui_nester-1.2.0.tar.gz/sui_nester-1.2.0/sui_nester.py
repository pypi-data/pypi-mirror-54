"""这是一个函数模块的测试

	在此之前，已经成功将此函数模块发布到了Pypi上，

	目前版本1.2.0

	函数参数：the_list : 列表
			level : 缩进的等级，默认省缺值0
			indent 	: 是否缩紧，默认省缺值为False，不缩进

"""
def print_recursion(the_list, indent=False, level=0):
	for items in the_list:
		if isinstance(items, list):
			print_recursion(items, indent, level+1)
		else:
			if indent :
				for tab_stop in range(level):
					print("\t", end='')
			print(items)

			

