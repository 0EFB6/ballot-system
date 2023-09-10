from pyteal import *

@Subroutine(TealType.bytes)
def itob(arg):

    string = ScratchVar(TealType.bytes)
    num = ScratchVar(TealType.uint64)
    digit = ScratchVar(TealType.uint64)

    return If(
        arg == Int(0),
        Bytes("0"),
        Seq([
            string.store(Bytes("")),
            For(num.store(arg), num.load() > Int(0), num.store(num.load() / Int(10))).Do(
                Seq([
                    digit.store(num.load() % Int(10)),
                    string.store(
                        Concat(
                            Substring(
                                Bytes('0123456789'),
                                digit.load(),
                                digit.load() + Int(1)
                            ),
                            string.load()
                        )
                    )
                ])

            ),
            string.load()
        ])
    )

@Subroutine(TealType.uint64)
def btoi(str):

    num = ScratchVar(TealType.uint64)
    digit = ScratchVar(TealType.uint64)
    ascii = ScratchVar(TealType.uint64)
    str_length = ScratchVar(TealType.uint64)
    iterator = ScratchVar(TealType.uint64)
    # 48-57 (0...789)
    return If(
        str == Bytes("0"),
        Int(0),
        Seq([
            num.store(Int(0)),
            str_length.store(Len(str)),
            For(iterator.store(Int(0)), iterator.load() < str_length.load(), iterator.store(iterator.load() + Int(1))).Do(
                Seq([
                    ascii.store(GetByte(str, iterator.load())),
                    digit.store(ascii.load() - Int(48)),
                    num.store(num.load() * Int(10) + digit.load())
                ])
            ),
            num.load()
        ])
    )
