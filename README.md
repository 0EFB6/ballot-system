# Ballot Voting System

Welcome to the Ballot Voting System GitHub repository, which acts as a codebase for the Algorand Blockchain Hackathon(Malaysia). Ballot is your trusted voting platform that allows you to easily and securely cast your vote in various elections from the comfort of your own home. This README.md file provides essential information about the platform, its features, and a guide for running a demo of the platform for both Parliament and State elections.

## Table of Contents
- [About Ballot](#about-ballot)
- [Key Features](#key-features)
  - [Connect Your Pera Wallet](#connect-your-pera-wallet-to-get-started)
  - [Election Results](#election-results)
  - [Security and Privacy](#security-and-privacy)
  - [Support](#support)
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

## Data on The Blockchain

## Data Off The Blockchain

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

To run a demo of the State election on the Ballot platform, please navigate to `archive` branch, compile the smart contract located at [`backend -> smart-contract -> contract_state.py`](https://raw.githubusercontent.com/0EFB6/ballot-system/main/backend/smart-contract/contract_state.py), then deploy the smart contract in your preferred way.

Modified the App ID in these two files (located in `archive` branch, `frontend-state->src->components` folder):
- App.js
- Dashboard.js

Then run `npm i` and `npm start` in the `frontend-state` directory to test the Election Voting dApp.

## License

Ballot© 2023. All rights reserved. By Malaysians, for Malaysians.

For more information about Ballot and its features, please contact our support team. Thank you for choosing Ballot as your trusted voting platform!

**Made with love, Ballot© 2023. All rights reserved. By Malaysians, for Malaysians.**