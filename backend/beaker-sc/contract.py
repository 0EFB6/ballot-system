from beaker import *
from pyteal import *
from beaker.lib.storage import BoxList, BoxMapping

class Parliament(abi.NamedTuple):
	area: abi.Field[abi.String]
	no: abi.Field[abi.Uint8]
	state: abi.Field[abi.String]
	candidate_no: abi.Field[abi.Uint8]
	candidate_name: abi.Field[abi.String]
	candidate_party: abi.Field[abi.String]
	votes: abi.Field[abi.Uint64]

#[key1: value1, key2: value2, key3: value3, key4: value4, key5: value5]

#key: P103 OR Subang
#value: Area, No, State,        Candidate No, Candidate Name, Candidate Party, Votes
#    (Subang) (103) (Selangor), (2),          (Wilson),        (Pakatan)

class ParliamentItem:
	votes = GlobalStateValue(
		stack_type=TealType.uint64, default=Int(0), descr="Number of votes"
	)
	addr_list = BoxList(abi.Address, 10)
	par_seat = BoxMapping(abi.String, Parliament)

app = Application("Parliament Item", state=ParliamentItem())

@app.external
def bootstrap() -> Expr:
	return Seq(
		Pop(app.state.addr_list.create()),
		app.initialize_global_state()
	)

@app.external
def vote(addr: abi.Address) -> Expr:
	return Seq(app.state.addr_list[app.state.votes].set(addr), app.state.votes.increment())

@app.external
def readVote(vote: abi.Uint64, *, output: abi.Address) -> Expr:
	return app.state.addr_list[vote.get()].store_into(output)

@app.external
def readGlobal(*, output: abi.Uint64) -> Expr:
	return output.set(app.state.votes.get())


@app.external
def addParliamentSeat(area: abi.String, no: abi.Uint8, state: abi.String, candidate_no: abi.Uint8,
					  candidate_name: abi.String, candidate_party: abi.String, votes: abi.Uint64) -> Expr:
	box_tuple = Parliament()
	ret = Seq(
		box_tuple.set(area, no, state, candidate_no, candidate_name, candidate_party, votes),
		app.state.par_seat[area.get()].set(box_tuple)
	)
	return ret

@app.external
def readParliamentItemState(area: abi.String, *, output: Parliament) -> Expr:
	return app.state.par_seat[area.get()].store_into(output)
    #ret = output.set(app.state.par_seat[area.get()].get())
    #return ret

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
