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
app_client.fund(100000 * algo)
print(
	f"""
App Deployed!

Txid        : {txid}
App Id      : {app_id}
App Address : {addr}

Funded 100 ALGO to app!")
"""
)

app_client1 = app_client.prepare(signer=accounts[0].signer)
app_client2 = app_client.prepare(signer=accounts[1].signer)
app_client3 = app_client.prepare(signer=accounts[2].signer)

SUBANG = "P102"
PUCHONG = "P103"
AMPANG = "P106"

#app_client.call(set_app_global_state_value, str="Hello World!")
#ret = app_client.call(readGlobal)
#print(f"Global State Value=> {ret.return_value}")

print(f"HH: {app_client1.call(createBox, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
app_client2.call(createBox, seat=PUCHONG, boxes=[(app_client.app_id, PUCHONG)])
app_client3.call(createBox, seat=SUBANG, boxes=[(app_client.app_id, SUBANG)])
#app_client1.call(putbox_votecount, seat=AMPANG, value="012345", i=0, boxes=[(app_client.app_id, AMPANG)])
app_client2.call(putBoxDebug, seat=PUCHONG, value="666999", i=0, boxes=[(app_client.app_id, PUCHONG)])
app_client3.call(putBoxDebug, seat=SUBANG, value="777333", i=0, boxes=[(app_client.app_id, SUBANG)])
#app_client1.call(putbox_votecount, seat=AMPANG, value="Wilson", i=6, boxes=[(app_client.app_id, AMPANG)])

ret = app_client1.call(readWholeBox, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)])
print(f"Ret 1 => {ret.return_value}")
ret = app_client2.call(readWholeBox, seat=PUCHONG, boxes=[(app_client.app_id, PUCHONG)])
print(f"Ret 2 => {ret.return_value}")
ret = app_client3.call(readWholeBox, seat=SUBANG, boxes=[(app_client.app_id, SUBANG)])
print(f"Ret 3 => {ret.return_value}")


app_client1.call(initVote, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)])

app_client1.call(addSeat, seat=AMPANG, area="Ampang", state="Selangor", boxes=[(app_client.app_id, AMPANG)])
ret = app_client1.call(readSeat, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value
print(f"Seat 1 => \n{ret}\n")


app_client1.call(addCandidate, seat=AMPANG, name="Brian", party="Testingg", i=1, boxes=[(app_client.app_id, AMPANG)])
app_client1.call(addCandidate, seat=AMPANG, name="Wilson", party="Perpaduan", i=2, boxes=[(app_client.app_id, AMPANG)])
app_client1.call(addCandidate, seat=AMPANG, name="Hao", party="Nasional", i=3, boxes=[(app_client.app_id, AMPANG)])
app_client1.call(addCandidate, seat=AMPANG, name="Dunno", party="Harapan", i=4, boxes=[(app_client.app_id, AMPANG)])

ret = app_client1.call(readCandidate, seat=AMPANG, i=1, boxes=[(app_client.app_id, AMPANG)]).return_value
print(f"Candidate 1 => {ret}")
ret = app_client1.call(readCandidate, seat=AMPANG, i=2, boxes=[(app_client.app_id, AMPANG)]).return_value
print(f"Candidate 2 => {ret}")
ret = app_client1.call(readCandidate, seat=AMPANG, i=3, boxes=[(app_client.app_id, AMPANG)]).return_value
print(f"Candidate 3 => {ret}")
ret = app_client1.call(readCandidate, seat=AMPANG, i=4, boxes=[(app_client.app_id, AMPANG)]).return_value
print(f"Candidate 4 => {ret}")
ret = app_client1.call(readCandidate, seat=AMPANG, i=5, boxes=[(app_client.app_id, AMPANG)]).return_value
print(f"Candidate 5 => {ret}\n")

print(f"Vote (BEFORE) ==>\n")
print(f"{app_client1.call(readVote1, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote2, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote3, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote4, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote5, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote6, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote7, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote8, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")

app_client1.call(updateVote, seat=AMPANG, i=2, boxes=[(app_client.app_id, AMPANG)])
app_client1.call(updateVote, seat=AMPANG, i=3, boxes=[(app_client.app_id, AMPANG)])
app_client1.call(updateVote, seat=AMPANG, i=1, boxes=[(app_client.app_id, AMPANG)])
app_client1.call(updateVote, seat=AMPANG, i=4, boxes=[(app_client.app_id, AMPANG)])
app_client1.call(updateVote, seat=AMPANG, i=2, boxes=[(app_client.app_id, AMPANG)])
app_client1.call(updateVote, seat=AMPANG, i=2, boxes=[(app_client.app_id, AMPANG)])

print(f"Vote (AFTER) ==>")
print(f"{app_client1.call(readVote1, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote2, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote3, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote4, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote5, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote6, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote7, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")
print(f"{app_client1.call(readVote8, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")

print(f"{app_client1.call(readWholeBox, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")

#print(f"\n{app_client1.call(readVote, seat=AMPANG, boxes=[(app_client.app_id, AMPANG)]).return_value}")



'''app_client.opt_in()
print("Opted in to app!")'''


'''
app_client.call(increase_local_state, v=1)

ret = app_client.call(get_local_state).return_value
print(f"Ret => {ret}")
'''