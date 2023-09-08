from beaker import *
from pyteal import *

app = Application("Beaker Calculator")

@app.external
def add(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64) -> Expr:
	return output.set(a.get() + b.get())
