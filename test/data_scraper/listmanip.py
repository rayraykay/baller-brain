def selected_items(given_list, desired_idx):
	to_return = []
	for i in range(len(given_list)):
		if i in desired_idx:
			to_return.append(given_list[i])

	return to_return
