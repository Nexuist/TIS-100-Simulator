class CPU():

    def __init__(self, instructions):
        self.instructions = instructions
        if len(self.instructions) <= 0:
            raise Exception("No instructions to execute!")
        self.labels = {line[1]: ip - 1 for ip, line in enumerate(instructions) if line[0] == "lbl"}
        self.ip = 0
        self.input = list(xrange(2))
        self.regs = {
            "dbg": 0,
            "acc": 0,
            "bak": 0,
            "in": None
        }

    def src_val(self, src):
        return self.regs[src] if src in self.regs else int(src)

    def mov(self, args):
        src = args[0]
        dst = args[1]
        if src == "bak" or src == "out": raise Exception("Can't directly read bak or out!")
        if dst == "bak" or dst == "in": raise Exception("Can't directly write to bak or in!")
        if src == "in":
            self.regs["in"] = self.input.pop()
            print("STDIN: " + str(self.regs["in"]))
        if dst == "out":
            print("STDOUT: " + str(self.src_val(src)))
            return
        self.regs[dst] = self.src_val(src)


    def add(self, args):
        self.regs["acc"] += self.src_val(args[0])

    def sub(self, args):
        self.regs["acc"] -= self.src_val(args[0])

    def neg(self, args):
        self.regs["acc"] *= -1

    def sav(self, args):
        self.regs["bak"] = self.regs["acc"]

    def swp(self, args):
        old_acc = self.regs["acc"]
        self.regs["acc"] = self.regs["bak"]
        self.regs["bak"] = old_acc

    def hcf(self, args):
        self.ip = len(self.instructions)

    def lbl(self, args):
        pass

    def nop(self, args):
        pass

    def dbg(self, args):
        self.regs["dbg"] = self.src_val(args[0])
        dbg = bool(self.regs["dbg"])
        print("%d: DEBUG %s" % (self.ip, ("ON" if dbg else "OFF")))

    def jmp(self, args):
        lbl = args[0]
        if not lbl in self.labels: raise Exception("Label %s doesn't exist!" % lbl)
        self.ip = self.labels[lbl]

    def jez(self, args):
        if self.regs["acc"] == 0: self.jmp(args)

    def jnz(self, args):
        if self.regs["acc"] != 0: self.jmp(args)

    def jgz(self, args):
        if self.regs["acc"] > 0: self.jmp(args)

    def jlz(self, args):
        if self.regs["acc"] < 0: self.jmp(args)

    def jro(self, args):
        self.ip += self.src_val(args[0]) - 1 # Because 1 will be added to ip after this command executes
        if self.ip < 0: raise Exception("Jumped to null IP: %d" % self.ip)

    def finished(self):
        return self.ip >= len(self.instructions)

    def line(self):
        return self.instructions[self.ip]

    def process(self):
        debug = bool(self.regs["dbg"])
        line = self.line()
        str_line = " ".join(line)
        if debug: print("%d: %s" % (self.ip, str_line))
        def invalid_command(args):
            raise Exception("Invalid command: " + line[0])
        command = getattr(self, line[0], invalid_command)
        args = line[1:]
        command(args)
        if debug: print("DEBUG: %s" % str(self.regs))
        self.ip += 1
        if len(self.input) == 0:
            self.hcf(None)
