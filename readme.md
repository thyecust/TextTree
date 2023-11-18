# TextTree

This is a python implementation of [clang::TextTreeStructure](https://clang.llvm.org/doxygen/classclang_1_1TextTreeStructure.html).

That class is used to dump a ClangAST:

```clang-check --ast-dump ~/hello.c    ✔ 
...
Running without flags.
TranslationUnitDecl 0x5596a4bf0bb8 <<invalid sloc>> <invalid sloc>
|-TypedefDecl 0x5596a4bf13e0 <<invalid sloc>> <invalid sloc> implicit __int128_t '__int128'
| `-BuiltinType 0x5596a4bf1180 '__int128'
|-TypedefDecl 0x5596a4bf1450 <<invalid sloc>> <invalid sloc> implicit __uint128_t 'unsigned __int128'
| `-BuiltinType 0x5596a4bf11a0 'unsigned __int128'
|-TypedefDecl 0x5596a4bf1758 <<invalid sloc>> <invalid sloc> implicit __NSConstantString 'struct __NSConstantString_tag'
| `-RecordType 0x5596a4bf1530 'struct __NSConstantString_tag'
|   `-Record 0x5596a4bf14a8 '__NSConstantString_tag'
|-TypedefDecl 0x5596a4bf17f0 <<invalid sloc>> <invalid sloc> implicit __builtin_ms_va_list 'char *'
| `-PointerType 0x5596a4bf17b0 'char *'
|   `-BuiltinType 0x5596a4bf0c60 'char'
|-TypedefDecl 0x5596a4bf1ae8 <<invalid sloc>> <invalid sloc> implicit __builtin_va_list 'struct __va_list_tag[1]'
| `-ConstantArrayType 0x5596a4bf1a90 'struct __va_list_tag[1]' 1 
|   `-RecordType 0x5596a4bf18d0 'struct __va_list_tag'
|     `-Record 0x5596a4bf1848 '__va_list_tag'
`-FunctionDecl 0x5596a4c4ca50 </home/tianhaoyu/hello.c:1:1, line:3:1> line:1:5 main 'int ()'
  `-CompoundStmt 0x5596a4c4cb70 <col:12, line:3:1>
    `-ReturnStmt 0x5596a4c4cb60 <line:2:2, col:9>
      `-IntegerLiteral 0x5596a4c4cb40 <col:9> 'int' 1
```

See main.py:

```python
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
```

Run it:

```
first
|-2:second
| |-3:forth
| | `-fifth
| `-3:sixth
`-2:third
```
