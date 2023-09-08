from beaker import *
from pyteal import *

class InitState:
	app_state = GlobalStateValue(
		stack_type=TealType.uint64,
		default=Int(69)
	)

class GlobalState:
	my_desc = GlobalStateValue(
		stack_type=TealType.bytes,
		default=Bytes("Hello, World! You funny!"),
		static=True
	)

app = Application("Beaker Calculator", state=GlobalState()).apply(
	unconditional_create_approval, initialize_global_state=True
)

@app.external
def set_app_global_state_value(str: abi.String) -> Expr:
	return app.state.my_desc.set(str.get())

@app.external
def read_app_global_state_value(*, output: abi.String) -> Expr:
	return output.set(app.state.my_desc)

@app.external
def read_state(*, output: abi.Uint64) -> Expr:
	return output.set(app.state.app_state)
