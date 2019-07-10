def extract_ne(tagset):
	result = []
	buf = []
	sind = 0
	last_bi = "O"
	last_type = None
	for i, g in enumerate(tagset):
		if g == "O":
			if len(buf) > 0:
				result.append((len(buf), sind, buf[0]))
				buf = []
			last_bi = "O"
			last_type = None
			continue
		ne_type, bi_tag = g.split("_")
		if bi_tag == "B":
			if len(buf) > 0:
				result.append((len(buf), sind, buf[0]))
				buf = []
			sind = i
			buf.append(ne_type)
			
		if last_bi in "BI" and bi_tag == "I" and last_type == ne_type:
			buf.append(ne_type)

		last_bi = bi_tag
		last_type = ne_type
	if len(buf) > 0:
		result.append((len(buf), sind, buf[0]))
	return result

def eval_ner(gold, pred, lens_with_pad, lens):
	sin = 0
	tp, fp, fn = 0, 0, 0
	for pl, l in zip(lens_with_pad, lens):
		g = gold[sin:sin+l]
		p = pred[sin:sin+l]
		sin += pl
		# print(g)
		# print(p)
		gold_instances = extract_ne(g)
		pred_instances = extract_ne(p)
		# print(len(gold_instances), len(pred_instances))
		if len(gold_instances) == len(pred_instances) == 0:
			continue
		

		for gtaglen, gidx, gtype in gold_instances:
			for ptaglen, pidx, ptype in pred_instances:
				if gtaglen == ptaglen and gidx == pidx and gtype == ptype:
					tp += 1
					break
			else:
				fn += 1
		for ptaglen, pidx, ptype in pred_instances:
			for gtaglen, gidx, gtype in gold_instances:
				if gtaglen == ptaglen and gidx == pidx and gtype == ptype:
					break
			else:
				fp += 1
	precision = tp / (tp+fp) if tp+fp > 0 else 0
	recall = tp / (tp+fn) if tp+fn > 0 else 0
	f1 = 2*precision*recall/(precision+recall) if precision + recall > 0 else 0
	
	return precision, recall, f1