from utils import *
from beaker import *
from pyteal import *
from beaker.lib.storage import BoxList, BoxMapping

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

app = Application("Voting Beaker", state=ParliamentSeat())

@app.external
def createBox(seat: abi.String) -> Expr:
	return Pop(BoxCreate(seat.get(), Int(1024)))

@app.external
def readWholeBox(seat: abi.String, *, output: abi.String) -> Expr:
	return output.set(BoxExtract(seat.get(), Int(0), Int(1000)))

@app.external
def addCandidate(seat:abi.String, name: abi.String, party: abi.String, i: abi.Uint8) -> Expr:
	Seq(
		Assert(Len(name.get()) > Int(0)),
		Assert(Len(name.get()) <= LEN_CANDIDATE_NAME),
		Assert(Len(party.get()) > Int(0)),
		Assert(Len(party.get()) <= LEN_PARTY)
	)
	return Seq(
		BoxReplace(seat.get(), CANDIDATE_NAME_1 + LEN_SUM * (i.get() - Int(1)), name.get()),
		BoxReplace(seat.get(), CANDIDATE_PARTY_1 + LEN_SUM * (i.get() - Int(1)), party.get())
	)

@app.external
def readCandidate(seat:abi.String, i: abi.Uint8, *, output: abi.String) -> Expr:
	ret = Concat(
		Bytes("Name: "),
		BoxExtract(seat.get(), CANDIDATE_NAME_1 + LEN_SUM * (i.get() - Int(1)), LEN_CANDIDATE_NAME),
		Bytes("\t\tParty: "),
		BoxExtract(seat.get(), CANDIDATE_PARTY_1 + LEN_SUM * (i.get() - Int(1)), LEN_PARTY)
	)
	return output.set(ret)

@app.external
def addSeat(seat: abi.String, area: abi.String, state: abi.String) -> Expr:
	Seq(
		Assert(Len(seat.get()) > Int(0)),
		Assert(Len(seat.get()) <= LEN_SEAT_NO),
		Assert(Len(area.get()) > Int(0)),
		Assert(Len(area.get()) <= LEN_SEAT_AREA),
		Assert(Len(state.get()) > Int(0)),
		Assert(Len(state.get()) <= LEN_SEAT_STATE)
	)
	ret = Seq(
		BoxReplace(seat.get(), SEAT_NO_I, seat.get()),
		BoxReplace(seat.get(), SEAT_AREA_I, area.get()),
		BoxReplace(seat.get(), SEAT_STATE_I, state.get())
	)
	return ret

@app.external
def readSeat(seat: abi.String, *, output: abi.String) -> Expr:
	ret = Concat(
		Bytes("Seat No: "),
		BoxExtract(seat.get(), SEAT_NO_I, LEN_SEAT_NO),
		Bytes("\nArea: "),
		BoxExtract(seat.get(), SEAT_AREA_I, LEN_SEAT_AREA),
		Bytes("\nState: "),
		BoxExtract(seat.get(), SEAT_STATE_I, LEN_SEAT_STATE)
	)
	return output.set(ret)

@app.external
def initVote(seat: abi.String):
	tmp = ScratchVar(TealType.uint64)

	return Seq(
		For(tmp.store(CANDIDATE_VOTES_1),
	  tmp.load() < (CANDIDATE_VOTES_1 + LEN_SUM * Int(9) + Int(1)),
	  tmp.store(tmp.load() + LEN_SUM)).Do(
			BoxReplace(seat.get(), tmp.load(), Bytes("000000"))
		)
	)
'''
, *, output: abi.Uint64
'''
@app.external
def updateVote(seat:abi.String, i: abi.Uint8) -> Expr:
	current_vote_byte = BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * (i.get() - Int(1)), LEN_VOTECOUNT)
	current_vote_uint = btoi(current_vote_byte)
	new_vote_uint = current_vote_uint + Int(6969)
	new_vote_byte = itob(new_vote_uint)
	# nbrlen = byteLength(new_vote_byte)
	nbrlen = Len(new_vote_byte)

	idx = Int(6) - nbrlen
	#return output.set(idx)
	return BoxReplace(
				seat.get(),
				# CANDIDATE_VOTES_1 + LEN_SUM * (i.get() - Int(1)) + Int(2),
				CANDIDATE_VOTES_1 + LEN_SUM * (i.get() - Int(1)) + idx,

				new_vote_byte
			)

@app.external
def readVote(seat: abi.String, *, output: abi.String) -> Expr:
	ret = Concat(
		Bytes("1: "),
		BoxExtract(seat.get(), CANDIDATE_VOTES_1, LEN_VOTECOUNT),
		Bytes(" 2: "),
		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM, LEN_VOTECOUNT),
		Bytes(" 3: "),
		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(2), LEN_VOTECOUNT),
		Bytes(" 4: "),
		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(3), LEN_VOTECOUNT),
		Bytes(" 5: "),
		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(4), LEN_VOTECOUNT),
		Bytes(" 6: "),
		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(5), LEN_VOTECOUNT),
		Bytes(" 7: "),
		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(6), LEN_VOTECOUNT),
		Bytes(" 8: "),
		BoxExtract(seat.get(), CANDIDATE_VOTES_1 + LEN_SUM * Int(7), LEN_VOTECOUNT)
	)
	return output.set(ret)













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
