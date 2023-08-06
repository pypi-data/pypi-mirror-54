"""这是一个函数模块的测试"""
def print_recursion(the_list, level):
	for items in the_list:
		if isinstance(items, list):
			print_recursion(items)
		else:
			for tab_stop in range(level):
				print("\t", end='')
			print(items)

			

