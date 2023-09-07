from pyteal import *

NO_I = Int(0)
NO_LEN = Int(3)
AREA_I= Int(4)
AREA_LEN = Int(25)
STATE_I = Int(30)
STATE_LEN = Int(15)

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
def create_par_box(state_no: abi.String):
	return Pop(App.box_create(Concat(Bytes("N"), state_no.get()), Int(50)))

@router.method
def create_par_seat(state_n: abi.String, area: abi.String, state: abi.String):
	Seq(
		Assert(Len(state_n.get()) > Int(0)),
		Assert(Len(state_n.get()) <= Int(2)),
		Assert(Len(area.get()) > Int(0)),
		Assert(Len(area.get()) <= Int(25)),
		Assert(Len(state.get()) > Int(0)),
		Assert(Len(state.get()) <= Int(15))
	)
	ret = Seq(
			App.box_replace(Concat(Bytes("N"), state_n.get()), NO_I, Concat(Bytes("N"), state_n.get())),
			App.box_replace(Concat(Bytes("N"), state_n.get()), AREA_I, area.get()),
			App.box_replace(Concat(Bytes("N"), state_n.get()), STATE_I, state.get()),
		)
	return ret

@router.method
def read_state_no(box_no: abi.String, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("N"), box_no.get()), NO_I, NO_LEN))

@router.method
def read_state_area(box_no: abi.String, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("N"), box_no.get()), AREA_I, AREA_LEN))

@router.method
def read_par_state(box_no: abi.String, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("N"), box_no.get()), STATE_I, STATE_LEN))

# Debug Use Only
@router.method
def read_debug(n: abi.String, src: abi.Uint64, dst: abi.Uint64,  *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("N"), n.get()), src.get(), dst.get()))

if __name__ == "__main__":
	import os
	import json

	path = os.path.dirname(os.path.abspath(__file__))
	approval, clear, contract = router.compile_program(version=8)

	# Write out the approval & clear program
	with open(os.path.join(path, "../artifacts/state_creation/approval.teal"), "w") as f:
		f.write(approval)

	with open(os.path.join(path, "../artifacts/state_creation/clear.teal"), "w") as f:
		f.write(clear)

	# Dump out the contract as JSON to be used by any SDKs
	with open(os.path.join(path, "../artifacts/state_creation/contract.json"), "w") as f:
		f.write(json.dumps(contract.dictify(), indent=2))