from pyteal import *
from utils import *

# 9 Global Bytes
# 3 Global Ints
# 0 Local Bytes
# 1 Local Ints

# Constant Values
LEN_SEAT_NO 		= Int(4)
LEN_SEAT_AREA 		= Int(26)
LEN_SEAT_STATE 		= Int(15)
LEN_CANDIDATE_NAME 	= Int(65)
LEN_PARTY 			= Int(25)
LEN_VOTECOUNT 		= Int(6)
LEN_SUM 			= LEN_CANDIDATE_NAME + LEN_PARTY + LEN_VOTECOUNT
SEAT_NO_I 			= Int(0)
SEAT_AREA_I 		= Int(4)
SEAT_STATE_I 		= Int(30)
CANDIDATE_NAME_1 	= Int(45)
CANDIDATE_PARTY_1 	= Int(110)
CANDIDATE_VOTES_1 	= Int(135)

K_VOTE = Bytes("Votes")
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
CAN1_NAME = Bytes("Brendon")
CAN1_PARTY = Bytes("Perpaduan")
CAN2_NAME = Bytes("Luis")
CAN2_PARTY = Bytes("Madani")
CAN3_NAME = Bytes("Zack")
CAN3_PARTY = Bytes("Nasional")

sender = Txn.sender()

#key = Txn.application_args[1] # Address
#seat = Txn.application_args[1] # P106
#area = Txn.application_args[2] # Subang
#state = Txn.application_args[3] # Selangor
#name = Txn.application_args[4] # Brandon
#party = Txn.application_args[5] # Harapan
#i = Txn.application_args[6] # Candidate ID

def init_parliament_seat():
    return Seq([
        App.globalPut(K_SEAT_NO, Bytes("P110")),
        App.globalPut(K_SEAT_AREA, Bytes("Klang")),
        App.globalPut(K_SEAT_STATE, Bytes("Selangor")),
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

def init_state_seat():
    return Seq([
        App.globalPut(K_SEAT_NO, Bytes("N31")),
        App.globalPut(K_SEAT_AREA, Bytes("Subang Jaya")),
        App.globalPut(K_SEAT_STATE, Bytes("Selangor")),
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
    currentVoteCount = App.globalGet(K_C2_VOTES)
    isVoted = App.localGet(sender, K_VOTE)
    return Seq([
        If(
            isVoted == Int(0),
            Seq(
                App.globalPut(K_C2_VOTES, currentVoteCount + Int(1)),
                App.localPut(sender, K_VOTE, isVoted + Int(1))
            )
        ),
        Return(Int(1))
    ])

def voteCandidate3():
    currentVoteCount = App.globalGet(K_C3_VOTES)
    isVoted = App.localGet(sender, K_VOTE)
    return Seq([
        If(
            isVoted == Int(0),
            Seq(
                App.globalPut(K_C3_VOTES, currentVoteCount + Int(1)),
                App.localPut(sender, K_VOTE, isVoted + Int(1))
            )
        ),
        Return(Int(1))
    ])

def debugLocal():
    localVote = ScratchVar(TealType.uint64)
    return Seq([
        localVote.store(btoi(Txn.application_args[1])),
        #localVote.store(App.localGet(sender, Bytes("Vote"))),
        App.localPut(sender, K_VOTE, localVote.load() + Int(2)),
        Return(Int(1))
    ])

def debugGlobal():
    return Seq([
        App.globalPut(Bytes("Vote"), App.globalGet(Bytes("Vote")) + Int(3)),
        Return(Int(1))
    ])

def approval_program():
    handle_creation = Seq([
        App.globalPut(K_SEAT_NO, Bytes("NULL")),
        App.globalPut(K_SEAT_AREA, Bytes("NULL")),
        App.globalPut(K_SEAT_STATE, Bytes("NULL")),
        App.globalPut(K_C1_NAME, Bytes("NULL")),
        App.globalPut(K_C1_PARTY, Bytes("NULL")),
        App.globalPut(K_C1_VOTES, Int(0)),
        App.globalPut(K_C2_NAME, Bytes("NULL")),
        App.globalPut(K_C2_PARTY, Bytes("NULL")),
        App.globalPut(K_C2_VOTES, Int(0)),
        App.globalPut(K_C3_NAME, Bytes("NULL")),
        App.globalPut(K_C3_PARTY, Bytes("NULL")),
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
            [Txn.application_args[0] == Bytes("DebugLocal"), debugLocal()],
            [Txn.application_args[0] == Bytes("DebugGlobal"), debugGlobal()],
            [Txn.application_args[0] == Bytes("InitParliamentSeat"), init_parliament_seat()],
            [Txn.application_args[0] == Bytes("InitStateSeat"), init_state_seat()],
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