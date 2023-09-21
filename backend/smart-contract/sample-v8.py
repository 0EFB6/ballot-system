from pyteal import *

is_creator = Txn.sender() == Global.creator_address()

handle_creation = Seq(
    App.globalPut(Bytes("Count"), Int(0)),
	Approve()
)

router = Router(
	"Election Voting App",
	BareCallActions(
		no_op=OnCompleteAction.create_only(handle_creation),
        opt_in=OnCompleteAction.call_only(Approve()),
	),
)

@router.method
def add_local():
    localCount = ScratchVar(TealType.uint64)
    return Seq(
        localCount.store(App.localGet(Txn.sender(), Bytes("Count"))),
        App.localPut(Txn.sender(), Bytes("Count"), localCount.load() + Int(1))
    )

@router.method
def deduct_local():
    localCount = ScratchVar(TealType.uint64)
    return Seq(
        localCount.store(App.localGet(Txn.sender(), Bytes("Count"))),
        If(localCount.load() > Int(0),
            App.localPut(Txn.sender(), Bytes("Count"), localCount.load() - Int(1)),
        )
    )

@router.method
def add_global():
    scratchCount = ScratchVar(TealType.uint64)
    return Seq(
        scratchCount.store(App.globalGet(Bytes("Count"))),
        App.globalPut(Bytes("Count"), scratchCount.load() + Int(1))
    )

@router.method
def deduct_global():
    scratchCount = ScratchVar(TealType.uint64)
    return Seq(
        scratchCount.store(App.globalGet(Bytes("Count"))),
        If(scratchCount.load() > Int(0),
            App.globalPut(Bytes("Count"), scratchCount.load() - Int(1)),
        )
    )

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