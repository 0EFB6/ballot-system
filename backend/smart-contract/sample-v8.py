from pyteal import *

is_creator = Txn.sender() == Global.creator_address()

handle_creation = Seq(
    App.globalPut(Bytes("Count"), Int(3)),
	Approve()
)

handle_optin = Seq(
	App.localPut(Txn.sender(), Bytes("Count"), Int(69)),
	Approve()
)

router = Router(
	"Election Voting App",
	BareCallActions(
		no_op=OnCompleteAction.create_only(handle_creation),
        opt_in=OnCompleteAction.call_only(handle_optin),
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
    return Seq(
        App.globalPut(Bytes("Count"), App.globalGet(Bytes("Count")) + Int(1)),
    )

@router.method
def deduct_global():
    count = App.globalGet(Bytes("Count"))
    return Seq(
        If(count > Int(0),
            App.globalPut(Bytes("Count"), count - Int(1)),
        )
    )

if __name__ == "__main__":
	import os
	import json
	path = os.path.dirname(os.path.abspath(__file__))
	approval, clear, contract = router.compile_program(version=8)
	with open(os.path.join(path, "../artifacts/approval.teal"), "w") as f:
		f.write(approval)
	with open(os.path.join(path, "../artifacts/clear.teal"), "w") as f:
		f.write(clear)
	with open(os.path.join(path, "../artifacts/contract.json"), "w") as f:
		f.write(json.dumps(contract.dictify(), indent=2))
	print("Successfully compiled!")