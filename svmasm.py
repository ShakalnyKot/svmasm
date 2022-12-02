import sys

ASMTREE = {
	"valid_opcodes": ["spush", "spop", "sclr", "scall", "sjz", "prvs"],
	"valid_scalls": ["exit", "putchar"],
	"opcodes": {
		"spush": 0x10,
		"spop": 0x11,
		"sclr": 0x12,
		"scall": 0x1F,
		"sjz": 0x20,
		"prvs": 0x20
	},
	"scalls": {
		"exit": 0x0F,
		"putchar": 0x10
	}
}
DEBUG = False

def marg_to_int(arg: str) -> int:
	if arg.startswith("0x") or arg.endswith("h"):
		return int(arg.replace("0x", "").replace("h", ""), 16)
	elif arg.startswith("'") and arg.endswith("'"):
		return int(ord(arg.replace("'", "")))
	else:
		return int(arg)

def mnemonic_to_opcode(op: str) -> list:
	mnop = op.split(" ")[0]
	if mnop in ASMTREE["valid_opcodes"]:
		result: list = []
		result.append(ASMTREE["opcodes"][mnop])
		if mnop in ["sclr"]:
			if DEBUG: print(f"VERBOSE: {mnop} -> {result}, size: {len(result)}")
		else:
			mnarg = op.split(' ')[1]
			flag_processed: bool = False
			if mnop in ["scall"]:
				if mnarg in ASMTREE["valid_scalls"]:
					result.append(ASMTREE["scalls"][mnarg])
					flag_processed = True
			if not flag_processed == True:
				if mnop in ["sjz", "prvs"]:
					result.append(marg_to_int(mnarg) & 0xFF000000)
					result.append(marg_to_int(mnarg) & 0x00FF0000)
					result.append(marg_to_int(mnarg) & 0x0000FF00)
					result.append(marg_to_int(mnarg) & 0x000000FF)
				else:
					result.append(marg_to_int(mnarg))
			if DEBUG: print(f"VERBOSE: {mnop} {op.split(' ')[1]} -> {result}, size: {len(result)}")
		return result
	else:
		print(f"WARNING: invalid opcode - {mnop}")
		return [0, 0]

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} <FILENAME>")
		exit(1)
	try:
		with open(sys.argv[1], "r") as file:
			source = file.read().split("\n")
			file.close()
		result: list = []
		counter: int = 0
		labels: dict = {}

		for line in source:
			line = line.strip()
			if line.endswith(":"):
				labels[line.replace(":", "")] = counter
				if DEBUG: print("VERBOSE: labels:", labels, "counter:", counter)
				continue
			if line.endswith(tuple(labels.keys())):
				if DEBUG: print("VERBOSE: label", line.split(" ")[0] + " " + str(labels[line.split(" ")[1]]))
				resop = mnemonic_to_opcode(line.split(" ")[0] + " " + str(labels[line.split(" ")[1]]))
				if resop[0] in [0x12]:
					counter += len(resop)
				else:
					counter += len(resop) - 1
				result.append(resop)
				continue
			resop = mnemonic_to_opcode(line)
			result.append(resop)
			if resop[0] in [0x12]:
				counter += len(resop)
			else:
				counter += len(resop) - 1

		with open(sys.argv[1] + ".bin", "w") as outfile:
			for res1 in result:
				for res2 in res1:
					outfile.write(chr(res2))
			outfile.close()
	except FileNotFoundError:
		print(f"ERROR: {sys.argv[1]} - No such file or directory")
		exit(2)
	exit(0)