from contract import *
from beaker import sandbox, client, localnet
from beaker.consts import *

app.build().export("../artifacts/beaker-sc")
print("\nApp successfully exported to artifacts directory!")

accounts = sandbox.kmd.get_accounts()
sender = accounts[0]
print(f"Account 1: {accounts[0].address}")
print(f"Account 2: {accounts[1].address}")
print(f"Account 3: {accounts[2].address}")

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

app_client.fund(5 * algo)
print("Funded 5 ALGO to app!")
'''
app_client1 = app_client.prepare(signer=accounts[0].signer)
app_client2 = app_client.prepare(signer=accounts[1].signer)
app_client3 = app_client.prepare(signer=accounts[2].signer)

app_client1.call(addVote, boxes=[(app_client.app_id, "vote_list")])
app_client2.call(addVote, boxes=[(app_client.app_id, "vote_list")])
app_client3.call(addVote, boxes=[(app_client.app_id, "vote_list")])


ret = app_client.call(readGlobal)
print(f"Global => {ret.return_value}")'''


'''app_client.opt_in()
print("Opted in to app!")'''


'''
app_client.call(increase_local_state, v=1)

ret = app_client.call(get_local_state).return_value
print(f"Ret => {ret}")
'''