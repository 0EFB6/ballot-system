from pyteal import *
from utils import *

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

sender = Txn.sender()

def vote_local():
    localVote = ScratchVar(TealType.uint64)

    return Seq([
        localVote.store(btoi(Txn.application_args[1])),
        #localVote.store(App.localGet(sender, Bytes("Vote"))),
        App.localPut(sender, Bytes("Vote"), localVote.load() + Int(2)),
        Return(Int(1))
    ])


seat = Txn.application_args[2] # P106
area = Txn.application_args[3] # Subang
state = Txn.application_args[4] # Selangor
name = Txn.application_args[5] # Brandon
party = Txn.application_args[6] # Harapan
i = Txn.application_args[7] # Candidate ID

def createBox():
	return Seq([
        If (
		    Or(
			    Len(seat) == Int(4),
			    Len(seat) == Int(6)
		    ),
			Pop(App.box_create(seat, Int(1024))),
			#output.set(Concat(Bytes("Box ["), seat.get(), Bytes("] created successfully!")))
		#output.set(Concat(Bytes("Failed to create box ["), seat.get(), Bytes("]")))
	    ),
        Return(Int(1))
    ])

def addCandidate():
	return Seq([
		If(
		    And(
		    	Len(name) > Int(0),
		    	Len(name) <= LEN_CANDIDATE_NAME,
		    	Len(party) > Int(0),
		    	Len(party) <= LEN_PARTY,
                Or(
                    Len(seat) == Int(4),
                    Len(seat) == Int(6)
                )
		    ),
		    Seq(
		    	App.box_replace(seat,
                       CANDIDATE_NAME_1 + LEN_SUM * (btoi(i) - Int(1)),
                       name),
		    	App.box_replace(seat,
                       CANDIDATE_PARTY_1 + LEN_SUM * (btoi(i) - Int(1)),
                       party),
		    	#output.set(Concat(Bytes("Candidate ["), itob(i.get()), Bytes("] added successfully to seat ["), seat.get(), Bytes("]")))
		    )
		    #output.set(Concat(Bytes("Failed to add candidate to box ["), seat.get(), Bytes("]")))
	    )
    ])

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

    
    scratchVote = ScratchVar(TealType.uint64)
    localVote = ScratchVar(TealType.uint64)

    #def voteLocal():
    #    Seq([
    #        #scratchVote.store(Btoi(Txn.application_args[1])),
    #        localVote.store(App.localGet(sender, Bytes("Vote"))),
    #        App.localPut(sender, Bytes("Vote"), localVote.load() + Int(1)),
    #        Return(Int(1))
    #    ])

    
    voteLocal = vote_local()
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
            [Txn.application_args[0] == Bytes("VotingGlobal"), voteGlobal],
            [Txn.application_args[0] == Bytes("CreateBox"), createBox()],
            [Txn.application_args[0] == Bytes("AddCandidate"), addCandidate()]
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