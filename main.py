def OS(*arg, **kw):
    print(*arg, sep="", end="")
    return True

class Tree:
    Toplevel = True
    FisrtChild = True
    Pending = []
    Prefix = ""

    def AddChild(self, Fn):
        self.AddChildL("", Fn)
    
    def AddChildL(self, Label, Fn):
        if self.Toplevel:
            self.Toplevel = False
            Fn()
            while len(self.Pending) != 0:
                self.Pending[-1](True)
                self.Pending = self.Pending[:-1]
            self.Prefix = ""
            OS("\n")
            self.Toplevel = True
            return
        
        D = lambda IsLastChild: self.DumpWithPrefix(Label, Fn, IsLastChild)
        if self.FisrtChild:
            self.Pending.append(D)
        else:
            self.Pending[-1](False)
            self.Pending[-1] = D
        self.FisrtChild = False

    def DumpWithPrefix(self, Label, Fn, IsLastChild):
        OS("\n", self.Prefix, "`" if IsLastChild else "|", "-")
        if Label != "":
            OS(Label, ":")
        self.Prefix += "  " if IsLastChild else "| "

        self.FisrtChild = True
        Depth = len(self.Pending)
        Fn()
        if Depth < len(self.Pending):
            self.Pending[-1](True)
            self.Pending = self.Pending[:-1]
        self.Prefix = self.Prefix[:-2]

if __name__ == "__main__":
    tree = Tree()
    tree.AddChild(lambda: (
        OS("first"),
        tree.AddChildL(2, lambda: (
            OS("second"),
            tree.AddChildL(3, lambda: (
                OS("forth"),
                tree.AddChild(lambda: (
                    OS("fifth")
                )),
            )),
            tree.AddChildL(3, lambda: (
                OS("sixth")
            ))
        )),
        tree.AddChildL(2, lambda: (
            OS("third")
        )),
    ))

