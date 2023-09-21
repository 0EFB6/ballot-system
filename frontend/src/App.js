import './App.css';
import {PeraWalletConnect} from '@perawallet/connect';
import algosdk, { waitForConfirmation } from 'algosdk';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useEffect, useState } from 'react';

// Create the PeraWalletConnect instance outside the component
const peraWallet = new PeraWalletConnect();

// The app ID on testnet
const appIndex = 368627424;

// connect to the algorand node
const algod = new algosdk.Algodv2('','https://testnet-api.algonode.cloud', 443);

function App() {
  const [accountAddress, setAccountAddress] = useState(null);
  const [currentCount, setCurrentCount] = useState(null);
  const [localCount, setLocalCount] = useState(null);
  const isConnectedToPeraWallet = !!accountAddress;

  useEffect(() => {
    checkCounterState();
    checkLocalCounterState();
    // reconnect to session when the component is mounted
    peraWallet.reconnectSession().then((accounts) => {
      // Setup disconnect event listener
      peraWallet.connector?.on('disconnect', handleDisconnectWalletClick);

      if (accounts.length) {
        setAccountAddress(accounts[0]);
      }
    })

  },[]);
  
  return (
    <Container className='App-header'>
      <meta name="name" content="Modified Counter App" />
      <h1> AlgoHUB - Lab 3</h1>
      <Row>
        <Col><Button className="btn-wallet"
      onClick={
        isConnectedToPeraWallet ? handleDisconnectWalletClick : handleConnectWalletClick
      }>
      {isConnectedToPeraWallet ? "Disconnect" : "Connect to Pera Wallet"}
    </Button></Col>
    <Col><Button className="btn-wallet"
      onClick={
        () => optInToApp()
      }>
      Opt-in
    </Button></Col>
      </Row>
        
        
      <Container>
        <Row>
          <Col><Button className="btn-add-local"
     onClick={
      // add the method for the local add
        () => callCounterApplication('Voting', '69')
      }>
      Votelocal
    </Button>
    <input id="receiver"></input>

    <Button className="btn-dec-local" 
     onClick={
      // add the local deduct method
      () => sendPaymentTxn()
      }>
      Send payment
    </Button>

    </Col>
    <Col>
    <h3>Local Count</h3>
    <span className='local-counter-text'>{localCount}</span>
    </Col>
          <Col><Button className="btn-dec-local" 
     onClick={
      // add the local deduct method
      () => callCounterApplication('Deduct_Local')
      }>
      Decrease
    </Button></Col>
        </Row>
        <Row>
          <Col><Button className="btn-add-global"
     onClick={
      // add the global add function
        () => callCounterApplication('VotingGlobal', '2')
      }>
      Vote global
    </Button></Col>
    <Col>
    <h3>Global Count</h3>
    <span className='counter-text'>{currentCount}</span>
    </Col>
          <Col><Button className="btn-dec-global" 
     onClick={
      // add the deduct global function
      () => callCounterApplication('Deduct_Global')
      }>
      Decrease
    </Button></Col>
        </Row>
      </Container>
    </Container>
  );

  function handleConnectWalletClick() {
    peraWallet.connect().then((newAccounts) => {
      // setup the disconnect event listener
      peraWallet.connector?.on('disconnect', handleDisconnectWalletClick);

      setAccountAddress(newAccounts[0]);
    });
  }

    function handleDisconnectWalletClick() {
      peraWallet.disconnect();
      setAccountAddress(null);
    }

    async function optInToApp() {
      const suggestedParams = await algod.getTransactionParams().do();
      const optInTxn = algosdk.makeApplicationOptInTxn(
        accountAddress,
        suggestedParams,
        appIndex
      );

      const optInTxGroup = [{txn: optInTxn, signers: [accountAddress]}];

        const signedTx = await peraWallet.signTransaction([optInTxGroup]);
        console.log(signedTx);
        const { txId } = await algod.sendRawTransaction(signedTx).do();
        const result = await waitForConfirmation(algod, txId, 2);
    }

    async function checkCounterState() {
      try {
        const counter = await algod.getApplicationByID(appIndex).do();
        if (!!counter.params['global-state'][0].value.uint) {
          setCurrentCount(counter.params['global-state'][0].value.uint);
        } else {
          setCurrentCount(0);
        }
      } catch (e) {
        console.error('There was an error connecting to the algorand node: ', e)
      }
    }

    async function checkLocalCounterState() {
      try {
        const accountInfo = await algod.accountApplicationInformation(accountAddress,appIndex).do();
        if (!!accountInfo['app-local-state']['key-value'][0].value.uint) {
          setLocalCount(accountInfo['app-local-state']['key-value'][0].value.uint);
        } else {
          setLocalCount(0);
        }
        console.log(accountInfo['app-local-state']['key-value'][0].value.uint);
      } catch (e) {
        console.error('There was an error connecting to the algorand node: ', e)
      }
    }

    async function callCounterApplication(action, arg) {
      try {
        // get suggested params
        const suggestedParams = await algod.getTransactionParams().do();
        const appArgs = [new Uint8Array(Buffer.from(action)), new Uint8Array(Buffer.from(arg))];
        
        const actionTx = algosdk.makeApplicationNoOpTxn(
          accountAddress,
          suggestedParams,
          appIndex,
          appArgs
          );

        const actionTxGroup = [{txn: actionTx, signers: [accountAddress]}];

        const signedTx = await peraWallet.signTransaction([actionTxGroup]);
        console.log(signedTx);
        const { txId } = await algod.sendRawTransaction(signedTx).do();
        const result = await waitForConfirmation(algod, txId, 2);
        checkCounterState();
        checkLocalCounterState();
      
      } catch (e) {
        console.error(`There was an error calling the counter app: ${e}`);
      }
    }

    async function sendPaymentTxn() {
      try {
        //const suggestedParams = await algod.getTransactionParams().do();
        const receiver = document.getElementById("receiver").value
      
        const txn = {
          type: 'pay',
          accountAddress: accountAddress,
          to: receiver,
          amount: 100,
        }
      
        const signedTxn = await peraWallet.signTransaction(txn);
        console.log(signedTxn);
        const { txId } = await algod.sendPaymentTxn(signedTxn).do();
        const result = await waitForConfirmation(algod, txId, 2);
      } catch (e) {
        console.error(`There was an error sending the payment: ${e}`);
      }
    }
}

export default App;
