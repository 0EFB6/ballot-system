from beaker import *
from pyteal import *

class InitState:
	app_state = GlobalStateValue(
		stack_type=TealType.uint64,
		default=Int(69)
	)

app = Application("Beaker Calculator", state=InitState()).apply(
	unconditional_create_approval, initialize_global_state=True
)

@app.external
def read_state(*, output: abi.Uint64) -> Expr:
	return output.set(app.state.app_state)
