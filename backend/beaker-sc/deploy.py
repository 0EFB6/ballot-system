from contract import app, read_app_global_state_value, set_app_global_state_value
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

try:
	app_client.call(set_app_global_state_value, str="Lel!")
except:
	print("Error! State is static")

ret = app_client.call(read_app_global_state_value).return_value
print(f"Ret => {ret}")
