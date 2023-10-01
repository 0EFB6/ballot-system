# Ballot (Election Voting System)

Welcome to the Ballot Voting System GitHub repository, which acts as a codebase for the Algorand Blockchain Hackathon(Malaysia). Ballot is your trusted voting platform that allows you to easily and securely cast your vote in various elections from the comfort of your own home. This README.md file provides essential information about the platform, its features, and a guide for running a demo of the platform for both Parliament and State elections.

## Table of Contents
- [About Ballot](#about-ballot)
- [Key Features](#key-features)
  - [Connect Your Pera Wallet](#connect-your-pera-wallet-to-get-started)
  - [Election Results](#election-results)
  - [Security and Privacy](#security-and-privacy)
  - [Support](#support)
- [Existing Problems](#existing-problems)
  - [Fraud and Tampering](#fraud-and-tampering)
  - [Costly and Environmentally Unfriendly](#costly-and-environmentally-unfriendly)
  - [Voter Accessibility](#voter-accessibility)
  - [Queue Time](#queue-time)
  - [Limited Participation](#limited-participation)
   - [Delay of Results Announcement](#delay-of-results-announcement)
- [Our Solutions](#our-solutions)
- [Data on The Blockchain](#data-on-the-blockchain)
- [Data Off The Blockchain](#data-off-the-blockchain)
- [Demo Guide](#demo-guide)
  - [Parliament Election](#parliament-election-demo)
  - [State Election](#state-election-demo)
- [License](#license)

## About Ballot

Ballot is a trusted voting platform designed to streamline the voting process, allowing users to cast their votes securely and conveniently from their own homes.

## Key Features
### Connect Your Pera Wallet to Get Started

To begin using Ballot, you need to connect your Pera Wallet, which is the wallet for participating in elections. This wallet ensures the security and integrity of your vote based on Algorand Blockchain, and it's your gateway to participating in various elections.

### Election Results

Stay informed about election results with Ballot. The platform promises to announce the outcomes shortly after the voting period concludes, ensuring transparency and trust in the process, all using Blockchain Technology.

### Security and Privacy

Your privacy and the security of your vote are top priorities for Ballot. The platform employs advanced encryption and security measures to protect your data and maintain the integrity of the voting process, ensuring that your vote remains confidential and secure.

### Support

For any additional support or concerns, please reach out to our dedicated support team. We are committed to providing lightning-fast support and will assist you as soon as possible to address any issues or questions you may have.

## Existing Problems

### Fraud and Tampering

Paper-based systems are vulnerable to voter fraud, ballot stuffing and tampering. These activities may be caught by authorities but for those who are not caught, the consequences **undermine the integrity of elections** and lead to inaccurate results. Manipulation by existing parties from the government may happen and affect election results which affects the democracy of a country.

### Costly and Environmentally Unfriendly

Traditional elections consist of printing, distributing and storing **paper ballots, indelible ink, hiring and training poll workers**. These cost the Malaysia Government to spend hundreds of million (in MYR) on each election held once every 5 years. In 2018, it costs RM500 million for GE14 and in 2022, it costs more than RM1 billion for GE15. Moreover, voters need to travel to the polling station to cast their vote, which is not environmentally friendly as most of them drive to the polling station.

### Voter Accessibility

Traditional voting system requires voters to physically visit a polling station on a specific day, this may be inconvenient for people with disabilities (OKU), the elderly , those who are busy working and those who are abroad. Online voting system is not secure (due to cybersecurity risk issues etc.) if implemented and yet, traditional voting system is far better than voting online.

### Queue Time

During peak voting hours, especially in the morning, voters tend to spend more time queuing and affect their daily schedule. Voters can also be discouraged to come out and vote if it is crowded, leading to reduced partition and voting rate.

### Limited Participation

Voters who are abroad temporarily or permanently may not be able to cast their vote during the voting day.

### Delay of Results Announcement

Typical traditional voting system requires manual counting of paper ballots and always leads to delays in announcing election results. Normally, it takes at least 7 hours to 16 hours for the result to be finalised. Apart from that, these delays can create uncertainty and raise concerns about the validity of the results.

## Our Solutions

#### Issue 1
- Fraud and Tampering

Blockchain technology is used to ensure the integrity of the voting process and prevent fraud. Blockchain is a distributed ledger technology that is immutable, transparent and secure. It is immutable because once a transaction is recorded on the blockchain, it cannot be altered. It is transparent because all transactions are recorded on the blockchain and can be viewed by anyone. It is secure because all transactions are encrypted and linked to each other. Blockchain technology is used to ensure the integrity of the voting process. Blockchain is a distributed ledger technology that is immutable, transparent and secure. It is immutable because once a transaction is recorded on the blockchain, it cannot be altered. It is transparent because all transactions are recorded on the blockchain and can be viewed by anyone. It is secure because all transactions are encrypted and linked to each other.

#### Issue 2
- Costly and Environmentally Unfriendly
- Voter Accessibility
- Queue Time
- Limited Participation

Voters cast their vote using their own devices (smartphone, tablet, laptop, etc.) from the comfort of their own home. This reduces the cost of printing, distributing and storing paper ballots, indelible ink, hiring and training poll workers. Voters do not need to travel to the polling station to cast their vote, which is environmentally friendly as most of them drive to the polling station. Since voter can vote from anywhere, there is ZERO queuing time which also leads to increasing voting rate and participation.

#### Issue 3
- Delay of Results Announcement

Voting results are announced shortly after the voting period concludes, ensuring transparency and trust in the process, all using Blockchain Technology. This reduces the delay of results announcement and creates certainty and trust in the results. Thus, it only takes less than 1 hour to finalise the result as all the result are open and transparent.

## Data on The Blockchain

### Voter
- Vote Status (Have Voted / Have Not Voted)
- Address of voter

### Global State
- Candidate's Name
- Candidate's Party
- Candidate's Vote Count
- Seat Details (Seat No, Seat Area, Seat State)

## Data Off The Blockchain
- Voter's Details (For e-KYC verification purposes)

## Demo Guide

Below, you'll find a guide for running a demo of the Ballot platform for both Parliament and State elections. **Node and npm is required** for this dApp to run.

### Parliament Election Demo

Note: App ID (testnet) used for Parliament Election Demo is `396413856`, it is already deployed and had been used for the purpose of demo recording (to be included in Video Submission). 

To run a demo of the Parliament election on the Ballot platform, follow these steps:

1. Clone this GitHub repository to your local machine.

   ```shell
   git clone https://github.com/0EFB6/ballot-system.git
   ```

2. Navigate to the `frontend-parliament` directory.

   ```shell
   cd frontend
   ```

3. Install necessary dependencies.

   ```shell
   npm i
   ```

4. Start the Election Voting dApp.

   ```shell
   npm start
   ```

### State Election Demo

Note: State Election Demo is not included in the Video Submission, feel free to try it out manually. 

To run a demo of the State election on the Ballot platform, please navigate to `archive` branch, compile the smart contract located at [`backend -> smart-contract -> contract_state.py`](https://raw.githubusercontent.com/0EFB6/ballot-system/archive/backend/smart-contract/contract_state.py), then deploy the smart contract in your preferred way.

Modified the App ID in these two files (located in `archive` branch, `frontend-state->src->components` folder):
- App.js
- Dashboard.js

Then run `npm i` and `npm start` in the `frontend-state` directory to test the Election Voting dApp.

## License

Ballot© 2023. All rights reserved. By Malaysians, for Malaysians.

For more information about Ballot and its features, please contact our support team. Thank you for choosing Ballot as your trusted voting platform!

**Made with love, Ballot© 2023. All rights reserved. By Malaysians, for Malaysians.**