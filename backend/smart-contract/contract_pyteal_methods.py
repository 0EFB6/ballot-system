from pyteal import *
from utils import *

# 9 Global Bytes
# 3 Global Ints
# 0 Local Bytes
# 1 Local Ints

# Constant Values
K_VOTE = Bytes("Votes")
K_SEAT_NO = Bytes("SeatNo")
K_SEAT_AREA = Bytes("SeatArea")
K_SEAT_STATE = Bytes("SeatState")
K_C1_NAME = Bytes("C1Name")
K_C1_PARTY = Bytes("C1Party")
K_C1_VOTES = Bytes("C1Votes")
K_C2_NAME = Bytes("C2Name")
K_C2_PARTY = Bytes("C2Party")
K_C2_VOTES = Bytes("C2Votes")
K_C3_NAME = Bytes("C3Name")
K_C3_PARTY = Bytes("C3Party")
K_C3_VOTES = Bytes("C3Votes")
CAN1_NAME = Bytes("Brendon")
CAN1_PARTY = Bytes("Perpaduan")
CAN2_NAME = Bytes("Luis")
CAN2_PARTY = Bytes("Madani")
CAN3_NAME = Bytes("Zack")
CAN3_PARTY = Bytes("Nasional")
CAN4_NAME = Bytes("Amir")
CAN4_PARTY = Bytes("Nasional")
CAN5_NAME = Bytes("Norazlina")
CAN5_PARTY = Bytes("Harapan")
CAN6_NAME = Bytes("Lee Sin Loo")
CAN6_PARTY = Bytes("Perpaduan")

sender = Txn.sender()

def init_parliament_seat_demo1():
    return Seq([
        App.globalPut(K_SEAT_NO, Bytes("P110")),
        App.globalPut(K_SEAT_AREA, Bytes("Klang")),
        App.globalPut(K_SEAT_STATE, Bytes("Selangor")),
        App.globalPut(K_C1_NAME, CAN1_NAME),
        App.globalPut(K_C1_PARTY, CAN1_PARTY),
        App.globalPut(K_C1_VOTES, Int(0)),
        App.globalPut(K_C2_NAME, CAN2_NAME),
        App.globalPut(K_C2_PARTY, CAN2_PARTY),
        App.globalPut(K_C2_VOTES, Int(0)),
        App.globalPut(K_C3_NAME, CAN3_NAME),
        App.globalPut(K_C3_PARTY, CAN3_PARTY),
        App.globalPut(K_C3_VOTES, Int(0)),
        Return(Int(1))
    ])

def init_parliament_seat_demo2():
    return Seq([
        App.globalPut(K_SEAT_NO, Bytes("P045")),
        App.globalPut(K_SEAT_AREA, Bytes("Bukit Mertajam")),
        App.globalPut(K_SEAT_STATE, Bytes("Pulau Pinang")),
        App.globalPut(K_C1_NAME, CAN4_NAME),
        App.globalPut(K_C1_PARTY, CAN4_PARTY),
        App.globalPut(K_C1_VOTES, Int(0)),
        App.globalPut(K_C2_NAME, CAN5_NAME),
        App.globalPut(K_C2_PARTY, CAN5_PARTY),
        App.globalPut(K_C2_VOTES, Int(0)),
        App.globalPut(K_C3_NAME, CAN6_NAME),
        App.globalPut(K_C3_PARTY, CAN6_PARTY),
        App.globalPut(K_C3_VOTES, Int(0)),
        Return(Int(1))
    ])

def init_state_seat_demo1():
    return Seq([
        App.globalPut(K_SEAT_NO, Bytes("N31")),
        App.globalPut(K_SEAT_AREA, Bytes("Subang Jaya")),
        App.globalPut(K_SEAT_STATE, Bytes("Selangor")),
        App.globalPut(K_C1_NAME, CAN1_NAME),
        App.globalPut(K_C1_PARTY, CAN1_PARTY),
        App.globalPut(K_C1_VOTES, Int(0)),
        App.globalPut(K_C2_NAME, CAN2_NAME),
        App.globalPut(K_C2_PARTY, CAN2_PARTY),
        App.globalPut(K_C2_VOTES, Int(0)),
        App.globalPut(K_C3_NAME, CAN3_NAME),
        App.globalPut(K_C3_PARTY, CAN3_PARTY),
        App.globalPut(K_C3_VOTES, Int(0)),
        Return(Int(1))
    ])

def init_state_seat_demo2():
    return Seq([
        App.globalPut(K_SEAT_NO, Bytes("N10")),
        App.globalPut(K_SEAT_AREA, Bytes("Seberang Jaya")),
        App.globalPut(K_SEAT_STATE, Bytes("Pulau Pinang")),
        App.globalPut(K_C1_NAME, CAN4_NAME),
        App.globalPut(K_C1_PARTY, CAN4_PARTY),
        App.globalPut(K_C1_VOTES, Int(0)),
        App.globalPut(K_C2_NAME, CAN5_NAME),
        App.globalPut(K_C2_PARTY, CAN5_PARTY),
        App.globalPut(K_C2_VOTES, Int(0)),
        App.globalPut(K_C3_NAME, CAN6_NAME),
        App.globalPut(K_C3_PARTY, CAN6_PARTY),
        App.globalPut(K_C3_VOTES, Int(0)),
        Return(Int(1))
    ])

def voteCandidate1():
    return Seq([
        If(
            App.localGet(sender, K_VOTE)  == Int(0),
            Seq(
                App.globalPut(K_C1_VOTES, App.globalGet(K_C1_VOTES) + Int(1)),
                App.localPut(sender, K_VOTE, Int(1))
            )
        ),
        Return(Int(1))
    ])

def voteCandidate2():
    currentVoteCount = App.globalGet(K_C2_VOTES)
    isVoted = App.localGet(sender, K_VOTE)
    return Seq([
        If(
            isVoted == Int(0),
            Seq(
                App.globalPut(K_C2_VOTES, currentVoteCount + Int(1)),
                App.localPut(sender, K_VOTE, isVoted + Int(1))
            )
        ),
        Return(Int(1))
    ])

def voteCandidate3():
    currentVoteCount = App.globalGet(K_C3_VOTES)
    isVoted = App.localGet(sender, K_VOTE)
    return Seq([
        If(
            isVoted == Int(0),
            Seq(
                App.globalPut(K_C3_VOTES, currentVoteCount + Int(1)),
                App.localPut(sender, K_VOTE, isVoted + Int(1))
            )
        ),
        Return(Int(1))
    ])

def getSeatNo():
    return Seq([
        Return(App.globalGet(K_SEAT_NO))
    ])

def getSeatArea():
    return Seq([
        Return(App.globalGet(K_SEAT_AREA))
    ])

def getSeatState():
    return Seq([
        Return(App.globalGet(K_SEAT_STATE))
    ])