from pyteal import *

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

def approval_program():
    handle_creation = Seq([
        App.globalPut(Bytes("Vote"), Int(0)),
        App.globalPut(Bytes("Voteid"), Int(0)),
        Return(Int(1))
    ])

    handle_optin = Return(Int(1))
    handle_closeout = Return(Int(0))
    handle_update = Return(Int(0))
    handle_deleteion = Return(Int(0))

    sender = Txn.sender()
    scratchVote = ScratchVar(TealType.uint64)
    localVote = ScratchVar(TealType.uint64)

    #def voteLocal():
    #    Seq([
    #        #scratchVote.store(Btoi(Txn.application_args[1])),
    #        localVote.store(App.localGet(sender, Bytes("Vote"))),
    #        App.localPut(sender, Bytes("Vote"), localVote.load() + Int(1)),
    #        Return(Int(1))
    #    ])

    voteLocal = Seq([
        localVote.store(btoi(Txn.application_args[1])),
        #localVote.store(App.localGet(sender, Bytes("Vote"))),
        App.localPut(sender, Bytes("Vote"), localVote.load() + Int(2)),
        Return(Int(1))
    ])
    #oteLocal = voteLocal()
    # voteGlobal = voteLocal()
    voteGlobal = Seq([
        
        scratchVote.store(App.globalGet(Bytes("Vote"))),
        App.globalPut(Bytes("Vote"), scratchVote.load() + Int(3)),
        Return(Int(1))
    ])

    handle_noop = Seq(
        Assert(Global.group_size() == Int(1)), 
        Cond(
            [Txn.application_args[0] == Bytes("Voting"), voteLocal],
            [Txn.application_args[0] == Bytes("VotingGlobal"), voteGlobal]
        )
    )

    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_update],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteion],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )
    return compileTeal(program, Mode.Application, version=5)

def clear_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=5)

app = open('../artifacts/approval.teal', 'w')
app.write(approval_program())
app.close()
clear = open('../artifacts/clear.teal', 'w')
clear.write(clear_program())
clear.close()
print("Compiled successfully")