from pyteal import *

@Subroutine(TealType.bytes)
def convert_uint_to_bytes(arg):

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
def convert_bytes_to_uint(str):

    tmp_str = ScratchVar(TealType.bytes)
    tmp_str.store(str)
    num = ScratchVar(TealType.uint64)
    digit = ScratchVar(TealType.uint64)
    str_length = ScratchVar(TealType.uint64)
    str_length.store(Int(0))
    str_length.store(str_length.load() + Len(str))
    iterator = ScratchVar(TealType.uint64)

    return If(
        str == Bytes("0"),
        Int(0),
        Seq([
            num.store(Int(0)),
            For(iterator.store(Int(0)), iterator.load() < Int(1), iterator.store(iterator.load() + Int(1))).Do(
                Seq([
                    digit.store(GetByte(str, )),
                    num.store((num.load() * 10) + digit.load())
                ])
            ),
            num.load()
        ])
    )

