import sys

ASMTREE = {
	"valid_opcodes": ["spush", "spop", "sclr", "scall", "sjz"],
	"valid_scalls": ["exit", "putchar"],
	"opcodes": {
		"spush": 0x10,
		"spop": 0x11,
		"sclr": 0x12,
		"scall": 0x1F,
		"sjz": 0x20
	},
	"scalls": {
		"exit": 0x0F,
		"putchar": 0x10
	}
}
DEBUG = False

def mnemonic_to_opcode(arg: str) -> list:
	mnop = arg.split(" ")[0]
	if mnop in ASMTREE["valid_opcodes"]:
		result: list = []
		result.append(ASMTREE["opcodes"][mnop])
		if mnop in ["sclr"]:
			if DEBUG: print(f"VERBOSE: {mnop} -> {result}")
		else:
			mnarg = arg.split(' ')[1]
			flag_processed: bool = False
			if mnop in ["scall"]:
				if mnarg in ASMTREE["valid_scalls"]:
					result.append(ASMTREE["scalls"][mnarg])
					flag_processed = True
			if (mnarg.startswith("0x") or mnarg.endswith("h")) and not flag_processed == True:
				result.append(int(mnarg.replace("0x", "").replace("h", ""), 16))
			elif (mnarg.startswith("'") and mnarg.endswith("'")) and not flag_processed == True:
				result.append(ord(mnarg.replace("'", "")))
			elif not flag_processed == True:
				result.append(int(mnarg))
			if DEBUG: print(f"VERBOSE: {mnop} {arg.split(' ')[1]} -> {result}")
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
		for line in source:
			result.append(mnemonic_to_opcode(line))

		with open(sys.argv[1] + ".bin", "w") as outfile:
			for res1 in result:
				for res2 in res1:
					outfile.write(chr(res2))
			outfile.close()
	except FileNotFoundError:
		print(f"ERROR: {argv[1]} - No such file or directory")
		exit(2)
	exit(0)