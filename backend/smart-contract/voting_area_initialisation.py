from pyteal import *

# init_dun = State seats inforamtion (DUN, DUN number, state)
# init_dun_candidate = State seats candidate information
# 						(candidate name, party)

k_dun = Bytes("dun")
k_dun_no = Bytes("dun_no")
k_parliament = Bytes("parliament")
k_parliament_no = Bytes("parliament_no")
k_state = Bytes("state")
k_c_name = Bytes("c_name")
k_party = Bytes("party")

router = Router(
	"voting_area_initialisation",
	BareCallActions(
		no_op=OnCompleteAction.create_only(Approve()),
		opt_in=OnCompleteAction.call_only(Approve())
	)
)

@router.method
def init_dun(dun: abi.String, n: abi.Uint8, state: abi.String):
	is_valid_dun = And(
		Len(dun.get()) >= Int(0),
		Len(dun.get()) <= Int(20)
	)
	is_valid_dun_no = And(
		n.get() > Int(0),
		n.get() < Int(83)
	)
	is_valid_state = And(
		Len(state.get()) >= Int(0),
		Len(state.get()) <= Int(15)
	)
	check = And(
		is_valid_dun,
		is_valid_dun_no,
		is_valid_state
	)
	ret = If(
		check,
		Seq(
			App.localPut(Txn.sender(), k_dun, dun.get()),
			App.localPut(Txn.sender(), k_dun_no, n.get()),
			App.localPut(Txn.sender(), k_state, state.get())
		)
	)
	return ret

@router.method
def init_parliament(parliamen: abi.String, n: abi.Uint8, state: abi.String):
	is_valid_parliamen = And(
		Len(parliamen.get()) >= Int(0),
		Len(parliamen.get()) <= Int(20)
	)
	is_valid_parliamen_no = And(
		n.get() > Int(0),
		n.get() < Int(223)
	)
	is_valid_state = And(
		Len(state.get()) >= Int(0),
		Len(state.get()) <= Int(15)
	)
	check = And(
		is_valid_parliamen,
		is_valid_parliamen_no,
		is_valid_state
	)
	ret = If(
		check,
		Seq(
			App.localPut(Txn.sender(), k_parliament, parliamen.get()),
			App.localPut(Txn.sender(), k_parliament_no, n.get()),
			App.localPut(Txn.sender(), k_state, state.get())
		)
	)
	return ret

@router.method
def init_candidate(name: abi.String, party: abi.String):
	is_valid_name = And(
		Len(name.get()) >= Int(0),
		Len(name.get()) <= Int(40)
	)
	is_valid_party = And(
		Len(party.get()) >= Int(0),
		Len(party.get()) <= Int(20)
	)
	check = And(
		is_valid_name,
		is_valid_party
	)
	ret = If(
		check,
		Seq(
			App.localPut(Txn.sender(), k_c_name, name.get()),
			App.localPut(Txn.sender(), k_party, party.get())
		)
	)
	return ret

@router.method
def read_dun(*, output: abi.String):
	ret = App.localGet(Txn.sender(), k_dun)
	return output.set(ret)

@router.method
def read_dun_no(*, output: abi.Uint8):
	ret = App.localGet(Txn.sender(), k_dun_no)
	return output.set(ret)

@router.method
def read_parliament(*, output: abi.String):
	ret = App.localGet(Txn.sender(), k_parliament)
	return output.set(ret)

@router.method
def read_parliament_no(*, output: abi.Uint8):
	ret = App.localGet(Txn.sender(), k_parliament_no)
	return output.set(ret)

@router.method
def read_state(*, output: abi.String):
	ret = App.localGet(Txn.sender(), k_state)
	return output.set(ret)

@router.method
def read_c_name(*, output: abi.String):
	ret = App.localGet(Txn.sender(), k_c_name)
	return output.set(ret)

@router.method
def read_party(*, output: abi.String):
	ret = App.localGet(Txn.sender(), k_party)
	return output.set(ret)

if __name__ == "__main__":
	import os
	import json

	path = os.path.dirname(os.path.abspath(__file__))
	approval, clear, contract = router.compile_program(version=8)

	# Write out the approval & clear program
	with open(os.path.join(path, "artifacts/approval.teal"), "w") as f:
		f.write(approval)

	with open(os.path.join(path, "artifacts/clear.teal"), "w") as f:
		f.write(clear)

	# Dump out the contract as JSON to be used by any SDKs
	with open(os.path.join(path, "artifacts/contract.json"), "w") as f:
		f.write(json.dumps(contract.dictify(), indent=2))