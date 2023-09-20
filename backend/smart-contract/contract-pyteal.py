from pyteal import *

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

    voteLocal = Seq([
        localVote.store(App.localGet(sender, Bytes("Vote"))),
        App.localPut(sender, Bytes("Vote"), localVote.load() + Int(1)),
        Return(Int(1))
    ])

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