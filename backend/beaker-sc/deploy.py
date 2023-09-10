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

app_client1 = app_client.prepare(signer=accounts[0].signer)
app_client2 = app_client.prepare(signer=accounts[1].signer)
app_client3 = app_client.prepare(signer=accounts[2].signer)

SUBANG = "P102"
PUCHONG = "P103"
AMPANG = "P106"

app_client.call(set_app_global_state_value, str="Hello World!")
ret = app_client.call(readGlobal)
print(f"Global State Value=> {ret.return_value}")

app_client1.call(createbox_votecount, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)])
app_client2.call(createbox_votecount, seat=PUCHONG, boxes=[(app_client.app_id, PUCHONG)])
app_client3.call(createbox_votecount, seat=SUBANG, boxes=[(app_client.app_id, SUBANG)])
app_client1.call(putbox_votecount, seat=AMPANG, value="012345", i=0, boxes=[(app_client.app_id, AMPANG)])
app_client2.call(putbox_votecount, seat=PUCHONG, value="666999", i=0, boxes=[(app_client.app_id, PUCHONG)])
app_client3.call(putbox_votecount, seat=SUBANG, value="777333", i=0, boxes=[(app_client.app_id, SUBANG)])
app_client1.call(putbox_votecount, seat=AMPANG, value="Wilson", i=6, boxes=[(app_client.app_id, AMPANG)])

ret = app_client1.call(readbox_votecount, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)])
print(f"Ret 1 => {ret.return_value}")
ret = app_client2.call(readbox_votecount, seat=PUCHONG, boxes=[(app_client.app_id, PUCHONG)])
print(f"Ret 2 => {ret.return_value}")
ret = app_client3.call(readbox_votecount, seat=SUBANG, boxes=[(app_client.app_id, SUBANG)])
print(f"Ret 3 => {ret.return_value}")
'''app_client.opt_in()
print("Opted in to app!")'''


'''
app_client.call(increase_local_state, v=1)

ret = app_client.call(get_local_state).return_value
print(f"Ret => {ret}")
'''