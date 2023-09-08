from contract import (
	app,
	write_blob,
	read_blob
)
from beaker import sandbox, client

app.build().export("../artifacts/beaker-sc")

accounts = sandbox.kmd.get_accounts()
sender = accounts[0]

app_client = client.ApplicationClient(
	client=sandbox.get_algod_client(),
	app=app,
	sender=sender.address,
	signer=sender.signer
)

app_id, addr, txid = app_client.create()

print(
	f"""
App Deployed!
Txid: {txid}
App Id: {app_id}
App Address: {addr}
"""
)

app_client.call(write_blob, start=0, str="Lel!")

ret = app_client.call(read_blob).return_value
print(f"Ret => {ret}")
