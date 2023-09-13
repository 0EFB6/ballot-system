from utils import *
from beaker import *
from pyteal import *
from beaker.lib.storage import BoxList, BoxMapping
import uuid
import hashlib

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

class ElectionVotingSystem:
	global_state = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Bytes("Testing"),
        descr="Global state for Parliament Seat"
    )
	custom_uid = LocalStateValue(
        stack_type=TealType.bytes,
        default=Bytes(""),
        descr="The custom part of the uid, eg. 0311000010810"
    )
	collected_ballot = LocalStateValue(
		stack_type=TealType.uint64,
		default=Int(0),
		static=False,
		descr="Value indicating voter collected ballot id or not, 0 indicate haven't collected, 1 indicate collected"
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

app = (Application("Voting Beaker", state=ElectionVotingSystem())
	   .apply(unconditional_create_approval, initialize_global_state=True)
	   .apply(unconditional_opt_in_approval, initialize_local_state=True))

sender = Txn.sender()

# Voting part, a bit messy
@app.external(authorize=Authorize.opted_in())
def setSeatNo(seat: abi.String) -> Expr:
	return app.state.custom_uid[sender].set(seat.get())

@app.external(authorize=Authorize.opted_in())
def vote(can_id: abi.Uint8, *, output: abi.String) -> Expr:
	seat_no = app.state.custom_uid[sender]
	# Fak this is not working!!!
	current_vote_byte = BoxExtract(seat_no, CANDIDATE_VOTES_1 + LEN_SUM * (can_id.get() - Int(1)), LEN_VOTECOUNT)
	current_vote_uint = btoi(current_vote_byte)
	new_vote_uint = current_vote_uint + Int(1)
	new_vote_byte = itob(new_vote_uint)
	idx = Int(6) - Len(new_vote_byte)
	#############################

	return If(
		And(
			can_id.get() >= Int(1),
			can_id.get() <= Int(8),
			app.state.voted[sender].get() == Int(0),
			app.state.candidate_id[sender].get() == Int(0),
		),
		Seq(
			app.state.candidate_id[sender].set(can_id.get()),
			app.state.voted[sender].increment(Int(1)),
			#BoxReplace(seat_no, CANDIDATE_VOTES_1 + LEN_SUM * (can_id.get() - Int(1)) + idx, new_vote_byte),
			output.set(Concat(
					Bytes("You have successfully voted!"),seat_no
				)
			)
		),
		output.set(Bytes("Failed to vote! You may have already voten before."))
	)

@app.external(authorize=Authorize.opted_in())
def updateVote(seat:abi.String, can_id: abi.Uint8, *, output: abi.String) -> Expr:
	current_vote_byte = BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * (can_id.get() - Int(1)), LEN_VOTECOUNT)
	current_vote_uint = btoi(current_vote_byte)
	new_vote_uint = current_vote_uint + Int(1)
	new_vote_byte = itob(new_vote_uint)
	idx = Int(6) - Len(new_vote_byte)
	return Seq(
			BoxReplace(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * (can_id.get() - Int(1)) + idx, new_vote_byte),
			output.set(Concat(Bytes("Successfully voted for candidate ["), itob(can_id.get()), Bytes("]")))
	)

@app.external(authorize=Authorize.opted_in())
def getLocalSeatNo(*, output: abi.String):
	return output.set(app.state.custom_uid[sender].get())

@app.external(authorize=Authorize.opted_in())
def getLocalCandidateId(*, output: abi.Uint8):
	return output.set(app.state.candidate_id[sender].get())

@app.external(authorize=Authorize.opted_in())
def getVoted(*, output: abi.Uint8):
	return output.set(app.state.voted[sender].get())
############################

@app.external
def createBox(seat: abi.String, *, output: abi.String) -> Expr:
	return If (
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



# Wilson: modified the decorator to only allow opted in account to run this method, ignore non-opted in user with standard error.
#		  I don't think we need to handle error for non-opted in account, just let it be what it is
#		  Removed 'Assert(App.optedIn(account.address(), app_id.get()))' (Ok nice: ZH)

# A function to store where the voter is voting after they verify themselves at gov office
@app.external(authorize=Authorize.opted_in())
def verify_acc_init(account: abi.Account, custom_uid: abi.String) -> Expr:
    return Seq(
		# Assert(Global.creator_address() == sender), # supposingly only gov official can add using the account that creates the app (admin acc)

        # Need add state that store verified account? 
		app.state.collected_ballot[account.address()].set(Int(0)),
		app.state.custom_uid[account.address()].set(custom_uid.get())
    )
	
@app.external
def createBoxUuid(name: abi.String, *, output: abi.String) -> Expr:
	return If(
		Len(name.get()) == Int(32),
		Seq(
			Pop(BoxCreate(name.get(), Int(32))),
			output.set(Concat(Bytes("Box ["), name.get(), Bytes("] created successfully!")))
		),
		output.set(Concat(Bytes("Failed to create box ["), name.get(), Bytes("]")))
	)
# How to store the uuid though, if onchain everyone can see? 
# (solution: store the hash uuid, when verifying hash the input uuid to see if it is the same)

@app.external
def get_uuid(*, output: abi.String) -> Expr:
    uid = uuid.uuid4().hex
    id_str_to_bytes = uid.encode('UTF-8')
    h = hashlib.shake_256(id_str_to_bytes)
	# return a 32digits hexadecimal hash
    hash_uid = Bytes(h.hexdigest(16))

    # Verified account will have their custom_uid updated and not empty
    return If(app.state.custom_uid[sender] == Bytes(""), 
                output.set(Bytes("Unverified Account")),
                # shows actual id but store hash id
                If(app.state.collected_ballot[sender] == Int(1),
                    output.set(Bytes("Collected Ballot")),
                    Seq(
						app.state.collected_ballot[sender].set(Int(1)),
                        output.set(Bytes(uid)),

						# Wilson: Where is the boc created?
                        # BoxPut(hash_uid, hash_uid)

                        # app.state.custom_uid[sender].set(Concat(app.state.custom_uid[sender], hash_uuid)), 
                    )
                ),
            )

# WIP
# maybe use pyteal Sha256 here then up there use sha256 from hashlib
#@app.external
#def show_hashid(uid: abi.String, *, output: abi.String):
#	# use during testing only
#    # return output.set(uid[1])
#    id_str_to_bytes = abi.String.encode(uid)
#    h = hashlib.shake_256(id_str_to_bytes)
#	# return a 32digits hexadecimal hash
#    hash_uid = Bytes(h.hexdigest(16))
#    return output.set(BoxExtract(hash_uid, Int(0), Int(32)))
	
@app.external
def check_uuid(uid: abi.String, *, output: abi.String) -> Expr:
    return If(
		BoxCreate(uid.get(), Int(32)),
		output.set(Bytes("Can't Vote")),
		output.set(Bytes("Can Vote"))
	)


# def bytes_to_str(bytes):
#     str = bytes.decode("utf-8")
#     str = []
#     str.append(bytes)
#     str.append("b")
#     str = "".join(str)
#     print(str)









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

if __name__ == '__main__':
    app.build().export("../artifacts/beaker-sc")
    print("Success")

