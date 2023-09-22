#samplecontract.py
# This file is from the Algorand documentation - https://developer.algorand.org/docs/get-details/dapps/pyteal/#final-product
from pyteal import *

## 1. Update App Name
"""Wilson Counter Application"""

def approval_program():
    handle_creation = Seq([
        App.globalPut(Bytes("Count"), Int(0)),
        Return(Int(1))
    ])

    # 2. Change handle_optin to return 1
    handle_optin = Return(Int(1))
    handle_closeout = Return(Int(0))
    handle_updateapp = Return(Int(0))
    handle_deleteapp = Return(Int(0))
    scratchCount = ScratchVar(TealType.uint64)
    # 3 - add local scratch var
    localCount = ScratchVar(TealType.uint64)

    # 4 - rename add and deduct to add_global and deduct_global
    add_global = Seq([
        scratchCount.store(App.globalGet(Bytes("Count"))),
        App.globalPut(Bytes("Count"), scratchCount.load() + Int(1)),
        Return(Int(1))
    ])

    deduct_global = Seq([
        scratchCount.store(App.globalGet(Bytes("Count"))),
        App.globalPut(Bytes("Count"), scratchCount.load() - Int(1)),
        Return(Int(1))
    ])

    # 5 - create a local version of add and deduct
    add_local = Seq([
        localCount.store(App.localGet(Txn.sender(), Bytes("Count"))),
        App.localPut(Txn.sender(), Bytes("Count"), localCount.load() + Int(1)),
        Return(Int(1))
    ])

    deduct_local = Seq([
        localCount.store(App.localGet(Txn.sender(), Bytes("Count"))),
        If(localCount.load() > Int(0),
            App.localPut(Txn.sender(), Bytes("Count"), localCount.load() - Int(1)),
        ),
        Return(Int(1))
    ])

    # 6 -Update the handle_noop conditions to use global and add local options
    handle_noop = Seq(
        Assert(Global.group_size() == Int(1)), 
        Cond(
            [Txn.application_args[0] == Bytes("Add_Global"), add_global], 
            [Txn.application_args[0] == Bytes("Deduct_Global"), deduct_global],
            [Txn.application_args[0] == Bytes("Add_Local"), add_local], 
            [Txn.application_args[0] == Bytes("Deduct_Local"), deduct_local]
        )
    )


    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )

    return compileTeal(program, Mode.Application, version=5)


def clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=5)

# 7 - update the file to 
# print out the results
#print(approval_program())
#print(clear_state_program())

appFile = open('../artifacts/approval.teal', 'w')
appFile.write(approval_program())
appFile.close()

clearFile = open('../artifacts/clear.teal', 'w')
clearFile.write(clear_state_program())
clearFile.close()

print("Done")