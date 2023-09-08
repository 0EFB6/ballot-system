from beaker import *
from pyteal import *

class InitState:
	app_state = GlobalStateValue(
		stack_type=TealType.uint64,
		default=Int(69)
	)

class BlobState:
	global_blob = GlobalStateBlob(
		keys=1
	)

class GlobalState:
	my_desc = GlobalStateValue(
		stack_type=TealType.bytes,
		default=Bytes("Hello, World! You funny!"),
		static=False
	)

class ReservedState:
	names = ReservedGlobalStateValue(
		stack_type=TealType.bytes,
		max_keys=64,
		descr="Dictionary of names with 64 possible keys"
	)

app = Application("Beaker Calculator", state=BlobState()).apply(
	unconditional_create_approval, initialize_global_state=True
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

#@app.external
#def set_app_reserved_global_state_value(k: abi.Uint64, str: abi.String) -> Expr:
#	return app.state.names[k].set(str.get())
#
#@app.external
#def read_app_reserved_global_state_value(k: abi.Uint64, *, output: abi.String) -> Expr:
#	return output.set(app.state.names[k])

#@app.external
#def set_app_global_state_value(str: abi.String) -> Expr:
#	return app.state.my_desc.set(str.get())
#
#@app.external
#def read_app_global_state_value(*, output: abi.String) -> Expr:
#	return output.set(app.state.my_desc)

#@app.external
#def read_state(*, output: abi.Uint64) -> Expr:
#	return output.set(app.state.app_state)
