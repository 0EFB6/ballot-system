from beaker import *
from pyteal import *

# Global State Value
class InitState:
	app_state = GlobalStateValue(
		stack_type=TealType.uint64,
		default=Int(69)
	)
@app.external
def read_state(*, output: abi.Uint64) -> Expr:
	return output.set(app.state.app_state)


# Global State Blob
class BlobState:
	global_blob = GlobalStateBlob(
		keys=1
	)
@app.external
def write_blob(start: abi.Uint64, str: abi.String) -> Expr:
	return app.state.global_blob.write(start.get(), str.get())

@app.external
def read_blob(*, output: abi.String) -> Expr:
	return output.set(
		app.state.global_blob.read(
			Int(0), app.state.global_blob.blob.max_bytes - Int(1)
		)
	)

# Global Static Value (Immutable)
class GlobalState:
	my_desc = GlobalStateValue(
		stack_type=TealType.bytes,
		default=Bytes("Hello, World! You funny!"),
		static=False
	)

@app.external
def set_app_global_state_value(str: abi.String) -> Expr:
	return app.state.my_desc.set(str.get())
@app.external
def read_app_global_state_value(*, output: abi.String) -> Expr:
	return output.set(app.state.my_desc)

# Reserved Global State Value
class ReservedState:
	names = ReservedGlobalStateValue(
		stack_type=TealType.bytes,
		max_keys=64,
		descr="Dictionary of names with 64 possible keys"
	)
@app.external
def set_app_reserved_global_state_value(k: abi.Uint64, str: abi.String) -> Expr:
	return app.state.names[k].set(str.get())
@app.external
def read_app_reserved_global_state_value(k: abi.Uint64, *, output: abi.String) -> Expr:
	return output.set(app.state.names[k])

# Local State Value
class LocalState:
	count = LocalStateValue(
		stack_type=TealType.uint64,
		default=Int(1),
		descr="A counter that keeps track  of counts"
	)
@app.external
def increase_local_state(v: abi.Uint64) -> Expr:
	return app.state.count[Txn.sender()].increment(v.get())

@app.external
def get_local_state(*, output: abi.Uint64) -> Expr:
	return output.set(app.state.count[Txn.sender()])


# Reserved Local State Value
class ReservedLocalState:
	food = ReservedLocalStateValue(
		stack_type=TealType.bytes,
		max_keys=8,
		descr="8 key value pairs of different foods"
	)

@app.external
def set_res_ls(k: abi.Uint8, v: abi.String) -> Expr:
	return app.state.food[k][Txn.sender()].set(v.get())

@app.external(read_only=True)
def read_res_ls(k: abi.Uint8, *, output: abi.String) -> Expr:
	return output.set(app.state.food[k][Txn.sender()])


# Local State Blob
class LocalStateBlob:
	blob = LocalStateBlob(
		keys=2,
		descr="A blob of 254 bytes"
	)
@app.external(authorize=Authorize.opted_in())
def write_blob(v: abi.String) -> Expr:
	return app.state.blob.write(Int(0), v.get())

@app.external
def read_local_blob(*, output: abi.String) -> Expr:
	return output.set(
		app.state.blob.read(
			Int(0), app.state.blob.blob.max_bytes - Int(1)
		)
	)

app = Application("LocalState Blob", state=LocalStateBlob()).apply(
	unconditional_opt_in_approval, initialize_local_state=True
)

'''
@app.opt_in
def opt_in() -> Expr:
	return Approve()

@app.close_out
def close_out() -> Expr:
	return Reject()

@app.clear_state
def clear_state() -> Expr:
	return Approve()
'''
