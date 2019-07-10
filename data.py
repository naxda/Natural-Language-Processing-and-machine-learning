def parse(fname):
	result = []
	with open(fname, encoding="UTF8") as f:
		buf = []
		for line in f.readlines():
			line = line.strip()
			if len(line) == 0:
				result.append(buf)
				buf = []
				continue
			id, token, tag = line.split("\t")
			if tag == "-": tag = "O"
			buf.append((token, tag))
	return result

def parse_srl(fname):
	wr = []
	lr = []
	pr = []
	with open(fname, encoding="UTF8") as f:
		result = []
		buf = []
		w = []
		p = []
		l = []
		label = []
		for line in f.readlines():
			line = line.strip()
			if line.startswith(";;"): continue

			if len(line) == 0:
				lb = [[] for _ in range(len(label[0]))]
				for e in label:
					for i, ee in enumerate(e):
						lb[i].append(ee)
				wr.append(w)
				pr.append(p)
				lr.append(label)
				result.append((w, l, lb))
				w = []
				p = []
				l = []
				label = []
				continue
			line = line.split("\t")
			word = line[2]
			# pos = line[4]
			# lemma = line[13]
			if line[12] == "Y":
				p.append(int(line[0])-1)
			args = line[14:]

			w.append(word)
			# p.append(pos)
			# l.append(lemma)
			label.append(args)

		return wr, pr, lr

def one_hot(i, total):
	i = int(i)
	result = [0 for _ in range(total)]
	result[i] = 1
	return result
	 
def one_hot_batch(i_tensor, total):
	result = [[0] * total] * i_tensor.size()[0]
	for i, t in enumerate(i_tensor):
		result[i][t] = 1
	return result

def decode(text_seq, label_seq):
	result = ""
	ltype = None
	in_ne = False
	for t, l in zip(text_seq, label_seq):
		l = l.split("-")
		if l[0] == "B":
			if in_ne:
				result += ":%s>" % ltype
			ltype = l[1]
			result += " <%s" % t
			in_ne = True
		elif l[0] == "I":
			result += " " + t
		else:
			if in_ne:
				result += ":%s>" % ltype
			result += " " + t
			in_ne = False
	return result.strip()