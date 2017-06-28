
class Utilities:
	@staticmethod
	def list_to_dict(my_lists, my_key, my_val):
		my_dict = dict()

		for list in my_lists:
			try:
				my_dict.update({
					list[my_key]: list[my_val]
				})
			except:
				my_dict.update({
					getattr(list, my_key): getattr(list, my_val)
				})

		return my_dict