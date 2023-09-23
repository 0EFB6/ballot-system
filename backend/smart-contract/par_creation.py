from pyteal import *

NO_I = Int(0)
NO_LEN = Int(4)
AREA_I= Int(5)
AREA_LEN = Int(25)
STATE_I = Int(31)
STATE_LEN = Int(15)

is_creator = Txn.sender() == Global.creator_address()

handle_creation = Seq(
	Approve()
)

router = Router(
	"Create Parliament Seat",
	BareCallActions(
		no_op=OnCompleteAction.create_only(handle_creation),
		
	),
)

@router.method
def create_par_box(par_no: abi.String):
	return Pop(App.box_create(Concat(Bytes("P"), par_no.get()), Int(50)))

@router.method
def create_par_seat(par_n: abi.String, area: abi.String, state: abi.String):
	Seq(
		Assert(Len(par_n.get()) > Int(0)),
		Assert(Len(par_n.get()) <= Int(3)),
		Assert(Len(area.get()) > Int(0)),
		Assert(Len(area.get()) <= Int(25)),
		Assert(Len(state.get()) > Int(0)),
		Assert(Len(state.get()) <= Int(15))
	)
	ret = Seq(
			App.box_replace(Concat(Bytes("P"), par_n.get()), NO_I, Concat(Bytes("P"), par_n.get())),
			App.box_replace(Concat(Bytes("P"), par_n.get()), AREA_I, area.get()),
			App.box_replace(Concat(Bytes("P"), par_n.get()), STATE_I, state.get()),
		)
	return ret

@router.method
def read_par_no(box_no: abi.String, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), box_no.get()), NO_I, NO_LEN))

@router.method
def read_par_area(box_no: abi.String, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), box_no.get()), AREA_I, AREA_LEN))

@router.method
def read_par_state(box_no: abi.String, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), box_no.get()), STATE_I, STATE_LEN))

# Debug Use Only
@router.method
def read_debug(n: abi.String, src: abi.Uint64, dst: abi.Uint64,  *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), n.get()), src.get(), dst.get()))

if __name__ == "__main__":
	import os
	import json

	path = os.path.dirname(os.path.abspath(__file__))
	approval, clear, contract = router.compile_program(version=8)

	# Write out the approval & clear program
	with open(os.path.join(path, "../artifacts/par_creation/approval.teal"), "w") as f:
		f.write(approval)

	with open(os.path.join(path, "../artifacts/par_creation/clear.teal"), "w") as f:
		f.write(clear)

	# Dump out the contract as JSON to be used by any SDKs
	with open(os.path.join(path, "../artifacts/par_creation/contract.json"), "w") as f:
		f.write(json.dumps(contract.dictify(), indent=2))