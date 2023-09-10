from candidate import NAME_I, LEN_LIMIT, NAME_LEN, PARTY_I, PARTY_LEN
from pyteal import *
from utils import convert_uint_to_bytes, convert_bytes_to_uint, get_uuid


N_I = Int(0)
N_LEN = Int(4)
AREA_I= Int(5)
AREA_LEN = Int(25)
STATE_I = Int(31)
STATE_LEN = Int(15)
k_i = Bytes("index")

# box = ""
#BOX = "011Subang Jaya Selangor"
# BOX2 = "Selangor Melaka"
# BOX_SELANGOR = "Subang P104\nPetaling Jaya"
# BOX_SUBANG_P104 = "Can1 Party1\nCan2 Party2"
# BOX_MELAKA = "Melaka Tengah\nAlor Gajah"

handle_creation = Seq(
	App.globalPut(k_i, Int(0)),
	App.globalPut(Bytes("can1_votes"), Int(0)),
	App.globalPut(Bytes("can2_votes"), Int(0)),
	Approve()
)

router = Router(
	"testingg",
	BareCallActions(
		no_op=OnCompleteAction.create_only(handle_creation),
	),
)

NAME_LIMIT = Int(30)

@router.method
def create_votes_box(candidate_name: abi.String):
	return Seq(
		# Assert(Len(candidate_name.get()) <= NAME_LIMIT),
		Pop(App.box_create(candidate_name.get(), NAME_LIMIT)),
    ) 

@router.method
def add_candidate_votes(candidate_name: abi.String):
	return Seq(
		# Assert(Len(candidate_name.get()) <= NAME_LIMIT),
        App.box_replace(candidate_name.get(), Int(0),  Bytes("0")),
    )


# @router.method
# def vote(box_no: abi.String, candidate_id: abi.Uint8, *, output: abi.String):
# 	return Seq(
# 		If(candidate_id.get() == Int(1), App.globalPut(Bytes("can1_votes"), App.globalGet(Bytes("can1_votes")) + Int(1)), App.globalPut(Bytes("can2_votes"), App.globalGet(Bytes("can2_votes")) + Int(1))),
# 		output.set(Bytes("Successfully voted"))
# 	)

@router.method
def read_vote(*, output: abi.String):
	can1_votes = convert_uint_to_bytes(App.globalGet(Bytes("can1_votes")))
	can2_votes = convert_uint_to_bytes(App.globalGet(Bytes("can2_votes")))
	
	return output.set(Concat(Bytes("Can1 votes: "), can1_votes, Bytes(", Can2 votes: "), can2_votes))


@router.method
def create_par_box(n: abi.String):
	return Seq(
		Pop(App.box_create(Concat(Bytes("P"), n.get()), Int(50)))
	)

@router.method
def add_par_box(par_n: abi.String, area: abi.String, state: abi.String):
	return Seq(
		App.box_replace(Concat(Bytes("P"), par_n.get()), N_I, Concat(Bytes("P"), par_n.get())),
		App.box_replace(Concat(Bytes("P"), par_n.get()), AREA_I, area.get()),
		App.box_replace(Concat(Bytes("P"), par_n.get()), STATE_I, state.get()),
	)

@router.method
def read_par_no(box_no: abi.String, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), box_no.get()), N_I, N_LEN))

@router.method
def read_par_area(box_no: abi.String, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), box_no.get()), AREA_I, AREA_LEN))

@router.method
def read_par_state(box_no: abi.String, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), box_no.get()), STATE_I, STATE_LEN))

@router.method
def read_debug(n: abi.String, src: abi.Uint64, dst: abi.Uint64,  *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), n.get()), src.get(), dst.get()))

@router.method
def read_index(*, output: abi.Uint64):
	return output.set(App.globalGet(k_i))

@router.method
def increment():
	scratchCount = ScratchVar(TealType.uint64)
	return Seq(
		scratchCount.store(App.globalGet(Bytes("count"))),
		App.globalPut(Bytes("count"), scratchCount.load() + Int(1)),
	)

@router.method
def decrement():
	scratchCount = ScratchVar(TealType.uint64)
	return Seq(
		Assert(Global.group_size() == Int(1)),
		scratchCount.store(App.globalGet(Bytes("count"))),
		If(
			scratchCount.load() > Int(0),
			App.globalPut(Bytes("count"), scratchCount.load() - Int(1)),
		),	
	)

@router.method
def read_count(*, output:abi.Uint64):
	return output.set(App.globalGet(Bytes("count")))

if __name__ == "__main__":
	import os
	import json

	path = os.path.dirname(os.path.abspath(__file__))
	approval, clear, contract = router.compile_program(version=8)

	# Write out the approval & clear program
	with open(os.path.join(path, "../artifacts/approval.teal"), "w") as f:
		f.write(approval)

	with open(os.path.join(path, "../artifacts/clear.teal"), "w") as f:
		f.write(clear)

	# Dump out the contract as JSON to be used by any SDKs
	with open(os.path.join(path, "../artifacts/contract.json"), "w") as f:
		f.write(json.dumps(contract.dictify(), indent=2))