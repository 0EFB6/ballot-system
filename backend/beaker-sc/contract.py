from beaker import *
from pyteal import *
from beaker.lib.storage import BoxList, BoxMapping

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
def createbox_votecount(seat: abi.String) -> Expr:
	return Pop(BoxCreate(seat.get(), Int(15)))

@app.external
def putbox_votecount(seat: abi.String, value: abi.String, i: abi.Uint16) -> Expr:
	return BoxReplace(seat.get(), i.get(), value.get())

@app.external
def readbox_votecount(seat: abi.String, *, output: abi.String) -> Expr:
	return output.set(BoxExtract(seat.get(), Int(0), Int(15)))


NO_I = Int(0)
NO_LEN = Int(4)
AREA_I= Int(5)
AREA_LEN = Int(25)
STATE_I = Int(31)
STATE_LEN = Int(15)

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
