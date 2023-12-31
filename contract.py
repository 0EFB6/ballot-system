from pyteal import *

# 9 Global Bytes
# 3 Global Ints
# 0 Local Bytes
# 1 Local Ints

# Constant Values
K_VOTE = Bytes("Voted")
K_SEAT_NO = Bytes("SeatNo")
K_SEAT_AREA = Bytes("SeatArea")
K_SEAT_STATE = Bytes("SeatState")
K_C1_NAME = Bytes("C1Name")
K_C1_PARTY = Bytes("C1Party")
K_C1_VOTES = Bytes("C1Votes")
K_C2_NAME = Bytes("C2Name")
K_C2_PARTY = Bytes("C2Party")
K_C2_VOTES = Bytes("C2Votes")
K_C3_NAME = Bytes("C3Name")
K_C3_PARTY = Bytes("C3Party")
K_C3_VOTES = Bytes("C3Votes")
CAN1_NAME = Bytes("Steven Sim Chee Keong")
CAN1_PARTY = Bytes("Pakatan Harapan")
CAN2_NAME = Bytes("Ah Pang")
CAN2_PARTY = Bytes("Barisan Nasiional")
CAN3_NAME = Bytes("Steven Koh")
CAN3_PARTY = Bytes("Perikatan Nasional")

sender = Txn.sender()

def voteCandidate1():
    return Seq([
        If(
            App.localGet(sender, K_VOTE)  == Int(0),
            Seq(
                App.globalPut(K_C1_VOTES, App.globalGet(K_C1_VOTES) + Int(1)),
                App.localPut(sender, K_VOTE, Int(1))
            )
        ),
        Return(Int(1))
    ])

def voteCandidate2():
    return Seq([
        If(
            App.localGet(sender, K_VOTE) == Int(0),
            Seq(
                App.globalPut(K_C2_VOTES, App.globalGet(K_C2_VOTES) + Int(1)),
                App.localPut(sender, K_VOTE, Int(1))
            )
        ),
        Return(Int(1))
    ])

def voteCandidate3():
    return Seq([
        If(
            App.localGet(sender, K_VOTE) == Int(0),
            Seq(
                App.globalPut(K_C3_VOTES, App.globalGet(K_C3_VOTES) + Int(1)),
                App.localPut(sender, K_VOTE, Int(1))
            )
        ),
        Return(Int(1))
    ])

def approval_program():
    handle_creation = Seq([
        App.globalPut(K_SEAT_NO, Bytes("P045")),
        App.globalPut(K_SEAT_AREA, Bytes("Bukit Mertajam")),
        App.globalPut(K_SEAT_STATE, Bytes("Pulau Pinang")),
        App.globalPut(K_C1_NAME, CAN1_NAME),
        App.globalPut(K_C1_PARTY, CAN1_PARTY),
        App.globalPut(K_C1_VOTES, Int(0)),
        App.globalPut(K_C2_NAME, CAN2_NAME),
        App.globalPut(K_C2_PARTY, CAN2_PARTY),
        App.globalPut(K_C2_VOTES, Int(0)),
        App.globalPut(K_C3_NAME, CAN3_NAME),
        App.globalPut(K_C3_PARTY, CAN3_PARTY),
        App.globalPut(K_C3_VOTES, Int(0)),
        Return(Int(1))
    ])
    handle_optin = Seq([
        App.localPut(sender, K_VOTE, Int(0)),
        Return(Int(1))
    ])
    handle_closeout = Return(Int(0))
    handle_update = Return(Int(0))
    handle_deleteion = Return(Int(0))
    handle_noop = Seq(
        Assert(Global.group_size() == Int(1)), 
        Cond(
            [Txn.application_args[0] == Bytes("VoteCandidate1"), voteCandidate1()],
            [Txn.application_args[0] == Bytes("VoteCandidate2"), voteCandidate2()],
            [Txn.application_args[0] == Bytes("VoteCandidate3"), voteCandidate3()],
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

    # Compile the approval program
    return compileTeal(program, Mode.Application, version=5)

def clear_program():
    program = Return(Int(1))

    # Compile the clear program
    return compileTeal(program, Mode.Application, version=5)


# Write the compiled program to disk
app = open('./approval-parliament.teal', 'w')
app.write(approval_program())
app.close()
clear = open('./clear-parliament.teal', 'w')
clear.write(clear_program())
clear.close()
print("Smart contract compiled successfully, you may proceed to deploy the dApp")