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

app_client.call(
	bootstrap,
	boxes=[(app_client.app_id, "addr_list")]
)

app_client1 = app_client.prepare(signer=accounts[0].signer)
app_client2 = app_client.prepare(signer=accounts[1].signer)
app_client3 = app_client.prepare(signer=accounts[2].signer)

app_client1.call(vote, addr=accounts[0].address, boxes=[(app_client.app_id, "addr_list")])
app_client2.call(vote, addr=accounts[1].address, boxes=[(app_client.app_id, "addr_list")])
app_client3.call(vote, addr=accounts[2].address, boxes=[(app_client.app_id, "addr_list")])

global_state = app_client.get_global_state()
i = int(global_state["votes"])

for x in range(i):
	value = app_client.call(
		readVote,
		vote=x,
		boxes=[(app_client.app_id, "addr_list")]
	)
	print("  - ", value.return_value)

ret = app_client.call(readGlobal)
print(f"Global => {ret.return_value}")

app_client1.call(addParliamentSeat, area="Puchong", no=101, state="Selangor", candidate_no=2,
				 candidate_name="Wilson", candidate_party="Harapan", votes=0, boxes=[(app_client.app_id, "Puchong")])
ret = app_client1.call(readParliamentItemState, area="Puchong", boxes=[(app_client.app_id, "Puchong")]).return_value
print(f"Ret => {ret}")

ret = app_client1.call(updateParliamentItem, area="Puchong", state="Melaka", boxes=[(app_client.app_id, "Puchong")]).return_value
print(f"Ret => {ret}")

ret = app_client1.call(readParliamentItemState, area="Puchong", boxes=[(app_client.app_id, "Puchong")]).return_value
print(f"Ret => {ret}")
'''app_client.opt_in()
print("Opted in to app!")'''


'''
app_client.call(increase_local_state, v=1)

ret = app_client.call(get_local_state).return_value
print(f"Ret => {ret}")
'''