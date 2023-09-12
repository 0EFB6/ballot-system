from utils import *
from beaker import *
from pyteal import *
from beaker.lib.storage import BoxList, BoxMapping
import uuid
# import hashlib

# Constant Vlaues
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

#[key1: value1, key2: value2, key3: value3, key4: value4, key5: value5]
#key: P103 OR Subang
#value: Area, No, State,        Candidate No, Candidate Name, Candidate Party, Votes
#    (Subang) (103) (Selangor), (2),          (Wilson),        (Pakatan)

class ParliamentSeat:
	global_state = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Bytes("Testing"),
        descr="Global state for Parliament Seat"
    )
	seats_no = LocalStateValue(
        stack_type=TealType.bytes,
        default=Bytes(""),
        descr="The seats voter gonna vote for"
    )
	candidate_id = LocalStateValue(
		stack_type=TealType.uint64,
		default=Int(0),
		static=False,
		descr="The candidate ID which voters are voting for"
	)
	voted = LocalStateValue(
		stack_type=TealType.uint64,
		default=Int(0),
		static=False,
		descr="Value indicating voters have voted or not, 0 indicate not voted, 1 indicate voted"
	)

app = (Application("Voting Beaker", state=ParliamentSeat())
	   .apply(unconditional_create_approval, initialize_global_state=True)
	   .apply(unconditional_opt_in_approval, initialize_local_state=True))

@app.external(authorize=Authorize.opted_in())
def vote(can_id: abi.Uint8, *, output: abi.String) -> Expr:
	return If(
		And(
			can_id.get() >= Int(1),
			can_id.get() <= Int(8),
			app.state.voted[Txn.sender()].get() == Int(0),
			app.state.candidate_id[Txn.sender()].get() == Int(0),
		),
		Seq(
			app.state.candidate_id[Txn.sender()].set(can_id.get()),
			app.state.voted[Txn.sender()].increment(Int(1)),
			output.set(Bytes("You have successfully voted!"))
		),
		output.set(Bytes("Failed to vote! You may have already voten before."))
	)

@app.external
def createBox(seat: abi.String, *, output: abi.String) -> Expr:
	return Seq(
		If (
			Or(
				Len(seat.get()) == Int(4),
				Len(seat.get()) == Int(6)
			),
			Seq(
				Pop(BoxCreate(seat.get(), Int(1024))),
				output.set(Concat(Bytes("Box ["), seat.get(), Bytes("] created successfully!")))
			),
			output.set(Concat(Bytes("Failed to create box ["), seat.get(), Bytes("]")))
		)
	)

@app.external
def addSeat(seat: abi.String, area: abi.String, state: abi.String, *, output: abi.String) -> Expr:
	return Seq(
		If(
			And(
				Or(
					Len(seat.get()) == Int(4),
					Len(seat.get()) == Int(6)
				),
				Len(area.get()) > Int(0),
				Len(area.get()) <= LEN_SEAT_AREA,
				Len(state.get()) > Int(0),
				Len(state.get()) <= LEN_SEAT_STATE
			),
			Seq(
				BoxReplace(seat.get(), SEAT_NO_I, seat.get()),
				BoxReplace(seat.get(), SEAT_AREA_I, area.get()),
				BoxReplace(seat.get(), SEAT_STATE_I, state.get()),
				output.set(Concat(Bytes("Seat ["), seat.get(), Bytes("] added successfully!")))
			),
			output.set(Concat(Bytes("Failed to add seat to box ["), seat.get(), Bytes("]")))
		)
	)

@app.external
def addCandidate(seat:abi.String, name: abi.String, party: abi.String, i: abi.Uint8, *, output: abi.String) -> Expr:
	return If(
		And(
			Len(name.get()) > Int(0),
			Len(name.get()) <= LEN_CANDIDATE_NAME,
			Len(party.get()) > Int(0),
			Len(party.get()) <= LEN_PARTY
		),
		Seq(
			BoxReplace(seat.get(), CANDIDATE_NAME_1 + LEN_SUM * (i.get() - Int(1)), name.get()),
			BoxReplace(seat.get(), CANDIDATE_PARTY_1 + LEN_SUM * (i.get() - Int(1)), party.get()),
			output.set(Concat(Bytes("Candidate ["), itob(i.get()), Bytes("] added successfully to seat ["), seat.get(), Bytes("]")))
		),
		output.set(Concat(Bytes("Failed to add candidate to box ["), seat.get(), Bytes("]")))
	)

@app.external
def initVote(seat: abi.String, *, output: abi.String):
	tmp = ScratchVar(TealType.uint64)
	return Seq(
		For(
			tmp.store(CANDIDATE_VOTES_1),
			tmp.load() < (CANDIDATE_VOTES_1 + LEN_SUM * Int(8)),
			tmp.store(tmp.load() + LEN_SUM)).Do(
				BoxReplace(seat.get(), tmp.load(), Bytes("000000"))
			),
		output.set(Concat(Bytes("Initialize vote for seat ["), seat.get(), Bytes("] to '000000'")))
	)

@app.external
def updateVote(seat:abi.String, i: abi.Uint8, *, output: abi.String) -> Expr:
	current_vote_byte = BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * (i.get() - Int(1)), LEN_VOTECOUNT)
	current_vote_uint = btoi(current_vote_byte)
	new_vote_uint = current_vote_uint + Int(1)
	new_vote_byte = itob(new_vote_uint)
	idx = Int(6) - Len(new_vote_byte)
	return Seq(
			BoxReplace(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * (i.get() - Int(1)) + idx, new_vote_byte),
			output.set(Concat(Bytes("Successfully voted for candidate ["), itob(i.get()), Bytes("]")))
	)

@app.external
def readSeat(seat: abi.String, *, output: abi.String) -> Expr:
	ret = Concat(
		Bytes("[READ SEAT INFO] Seat No: "),
		BoxExtract(seat.get(), SEAT_NO_I, LEN_SEAT_NO),
		Bytes("\tArea: "),
		BoxExtract(seat.get(), SEAT_AREA_I, LEN_SEAT_AREA),
		Bytes("\tState: "),
		BoxExtract(seat.get(), SEAT_STATE_I, LEN_SEAT_STATE)
	)
	return output.set(ret)

@app.external
def readCandidate(seat:abi.String, i: abi.Uint8, *, output: abi.String) -> Expr:
	return output.set(
		Concat(
			Bytes("["),
			seat.get(),
			Bytes("] [Candidate "),
			itob(i.get()),
			Bytes("] ==> Name: "),
			BoxExtract(seat.get(), CANDIDATE_NAME_1 + LEN_SUM * (i.get() - Int(1)), LEN_CANDIDATE_NAME),
			Bytes("\t\tParty: "),
			BoxExtract(seat.get(), CANDIDATE_PARTY_1 + LEN_SUM * (i.get() - Int(1)), LEN_PARTY)
		)
	)

@app.external
def readVote1(seat: abi.String, *, output: abi.String) -> Expr:
	vote = itob(btoi(BoxExtract(seat.get(), CANDIDATE_VOTES_1, LEN_VOTECOUNT)))
	return output.set(Concat(Bytes("1: "), vote))

@app.external
def readVote2(seat: abi.String, *, output: abi.String) -> Expr:
	vote = itob(btoi(BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM, LEN_VOTECOUNT)))
	return output.set(Concat(Bytes("2: "), vote))

@app.external
def readVote3(seat: abi.String, *, output: abi.String) -> Expr:
	vote = itob(btoi(BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(2), LEN_VOTECOUNT)))
	return output.set(Concat(Bytes("3: "), vote))

@app.external
def readVote4(seat: abi.String, *, output: abi.String) -> Expr:
	vote = itob(btoi(BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(3), LEN_VOTECOUNT)))
	return output.set(Concat(Bytes("4: "), vote))

@app.external
def readVote5(seat: abi.String, *, output: abi.String) -> Expr:
	vote = itob(btoi(BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(4), LEN_VOTECOUNT)))
	return output.set(Concat(Bytes("5: "), vote))

@app.external
def readVote6(seat: abi.String, *, output: abi.String) -> Expr:
	vote = itob(btoi(BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(5), LEN_VOTECOUNT)))
	return output.set(Concat(Bytes("6: "), vote))

@app.external
def readVote7(seat: abi.String, *, output: abi.String) -> Expr:
	vote = itob(btoi(BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(6), LEN_VOTECOUNT)))
	return output.set(Concat(Bytes("7: "), vote))

@app.external
def readVote8(seat: abi.String, *, output: abi.String) -> Expr:
	vote = itob(btoi(BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(7), LEN_VOTECOUNT)))
	return output.set(Concat(Bytes("8: "), vote))

# Function to read all vote counts

#@app.external
#def readVote(seat: abi.String, *, output: abi.String) -> Expr:
#	vote1 = itob(btoi(BoxExtract(seat.get(), CANDIDATE_VOTES_1, LEN_VOTECOUNT)))
#	vote2 = itob(btoi(BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM, LEN_VOTECOUNT)))
#	ret = Concat(
#		Bytes("1: "),
#		vote1,
#		Bytes(" 2: "),
#		vote2,
#		Bytes(" 3: "),
#		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(2), LEN_VOTECOUNT),
#		Bytes(" 4: "),
#		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(3), LEN_VOTECOUNT),
#		Bytes(" 5: "),
#		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(4), LEN_VOTECOUNT),
#		Bytes(" 6: "),
#		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(5), LEN_VOTECOUNT),
#		Bytes(" 7: "),
#		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(6), LEN_VOTECOUNT),
#		Bytes(" 8: "),
#		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(7), LEN_VOTECOUNT)
#	)
#	return output.set(ret)

@app.external
def readWholeBox(seat: abi.String, *, output: abi.String) -> Expr:
	return output.set(BoxExtract(seat.get(), Int(0), Int(1000)))

# WIP
# A function to store where the voter is voting after they verify themselves at gov office
@app.external
def verify_acc_init(account: abi.Account, seats_no: abi.String, app_id: abi.Uint64) -> Expr:
    return Seq(
		# Assert(Global.creator_address() == Txn.sender()), # supposingly only gov official can add using the account that creates the app (admin acc)
        # Don't know how to auto opt in from here
        # Need add state that store verified account? 

        # Check if account is opted in, dk if necessary since if not opt in will err too cause can't read local
        Assert(App.optedIn(account.address(), app_id.get())),
	    App.localPut(account.address(), Bytes("seats_no"), seats_no.get())	
    )
	
@Subroutine(TealType.bytes)
def hash_ballot(ballot_id):
    return Sha256(ballot_id)
    # str_to_bytes = ballot_id.encode('UTF-8')
    # h = hashlib.shake_256(str_to_bytes)
    # return h.hexdigest(45)

@app.external
def get_uuid(*, output: abi.String) -> Expr:
    unique_id = Bytes(uuid.uuid4().hex)
    # How to store the uuid though, if onchain everyone can see? 
    # (solution: store the hash uuid, when verifying hash the input uuid to see if it is the same)
    #  verify account too
    # Verified account will have their seats_no updated and not empty
    return If(app.state.seats_no[Txn.sender()] == Bytes(""), 
                output.set(Bytes("Unverified Account")),
                Seq(
                    app.state.seats_no[Txn.sender()].set(Concat(app.state.seats_no[Txn.sender()], unique_id)),
                     # got ex sha256 create a base32 16 digits value Bytes("base32", "2323232323232323")
                    # output.set(abi.String.decode(Sha256(app.state.seats_no[Txn.sender()]))),
                    # If output the id without hashing is already working
                    output.set(hash_ballot(app.state.seats_no[Txn.sender()])) # dk how to decode the hash so it could be stored or do we not need to decode?
                )
            )

    










# others
@app.external
def putBoxDebug(seat: abi.String, value: abi.String, i: abi.Uint16) -> Expr:
	return BoxReplace(seat.get(), i.get(), value.get())

@app.external
def set_app_global_state_value(str: abi.String) -> Expr:
	return app.state.global_state.set(str.get())

@app.external
def readGlobal(*, output: abi.String) -> Expr:
	return output.set(app.state.global_state)

# Borken Function
'''@app.external
def updateParliamentItem(area: abi.String, state: abi.String) -> Expr:
	mr = Parliament()	
	mr.decode(app.state.par_seat[area.get()].get())

	(n_area := abi.String()).get(mr.area)
	(n_no := abi.Uint8()).set(mr.no)
	(n_states := abi.String()).set(state.get())
	(n_candidate_no := abi.Uint8()).set(mr.candidate_no)
	(n_candidate_name := abi.String()).set(mr.candidate_name)
	(n_candidate_party := abi.String()).set(mr.candidate_party)
	(n_votes := abi.Uint64()).set(mr.votes)
	ret = Seq(
		mr.set(n_area, n_no, n_states, n_candidate_no, n_candidate_name, n_candidate_party, n_votes),
		app.state.par_seat[area.get()].set(mr)
	)
	return ret'''


'''@app.external
def updateParliamentSeatVotes(area: abi.String, new_votes: abi.Uint64) -> Expr:
    current_item = ParliamentItem()
    app.state.par_seat[area.get()].store_into(current_item)


    # Store the updated item back in the Box
    ret = Seq(
        app.state.par_seat[area.get()].set(updated_item)
    )
    return ret'''

'''@app.external
def readParliamentSeat(area: abi.String, *, output: ParliamentItem) -> Expr:
	return app.state.par_seat[area.get()].store_into(output)

@app.external
def deleteParliamentSeat(area: abi.String) -> Expr:
	return Pop(app.state.par_seat[area.get()].delete())'''
