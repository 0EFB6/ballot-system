from pyteal import *

NAME_I= Int(0)
NAME_LEN = Int(65)
PARTY_I = Int(65)
PARTY_LEN = Int(25)
LEN_LIMIT = Int(90)

handle_creation = Seq(
	App.globalPut(Bytes("Total Candidates"), Int(0)),
	Approve()
)

router = Router(
	"Add Candidates",
	BareCallActions(
		no_op=OnCompleteAction.create_only(handle_creation),
	),
)

@router.method
def create_par_box(par_no: abi.String):
	return Pop(App.box_create(Concat(Bytes("P"), par_no.get(), Bytes("_CANDIDATES")), LEN_LIMIT * Int(9)))

@router.method
def add_par_candidate(par_n: abi.String, name: abi.String, party: abi.String):
	Seq(
		Assert(Len(par_n.get()) > Int(0)),
		Assert(Len(par_n.get()) <= Int(3)),
		Assert(Len(name.get()) > Int(0)),
		Assert(Len(name.get()) <= Int(65)),
		Assert(Len(party.get()) > Int(0)),
		Assert(Len(party.get()) <= Int(24))
	)
	ret = Seq(
			App.box_replace(Concat(Bytes("P"), par_n.get(), Bytes("_CANDIDATES")), LEN_LIMIT * App.globalGet(Bytes("Total Candidates")),  name.get()),
			App.box_replace(Concat(Bytes("P"), par_n.get(), Bytes("_CANDIDATES")), PARTY_I + (LEN_LIMIT * App.globalGet(Bytes("Total Candidates"))), party.get()),
			App.globalPut(Bytes("Total Candidates"), App.globalGet(Bytes("Total Candidates")) + Int(1))
		)
	return ret

@router.method
def read_par_candidate_name(box_no: abi.String, candidate_id: abi.Uint8, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), box_no.get(), Bytes("_CANDIDATES")), NAME_I + LEN_LIMIT * (candidate_id.get() - Int(1)), NAME_LEN))

@router.method
def read_par_candidate_party(box_no: abi.String, candidate_id: abi.Uint8, *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), box_no.get(), Bytes("_CANDIDATES")), PARTY_I + LEN_LIMIT * (candidate_id.get() - Int(1)), PARTY_LEN))

# Debug Use Only
@router.method
def read_debug(n: abi.String, src: abi.Uint64, dst: abi.Uint64,  *, output: abi.String):
	return output.set(App.box_extract(Concat(Bytes("P"), n.get(), Bytes("_CANDIDATES")), src.get(), dst.get()))

if __name__ == "__main__":
	import os
	import json

	path = os.path.dirname(os.path.abspath(__file__))
	approval, clear, contract = router.compile_program(version=8)

	# Write out the approval & clear program
	with open(os.path.join(path, "../artifacts/candidate/approval.teal"), "w") as f:
		f.write(approval)

	with open(os.path.join(path, "../artifacts/candidate/clear.teal"), "w") as f:
		f.write(clear)

	# Dump out the contract as JSON to be used by any SDKs
	with open(os.path.join(path, "../artifacts/candidate/contract.json"), "w") as f:
		f.write(json.dumps(contract.dictify(), indent=2))