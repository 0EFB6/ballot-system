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
const appIndex = 377463127;

// connect to the algorand node
const algod = new algosdk.Algodv2('','https://testnet-api.algonode.cloud', 443);

function App() {
  const [accountAddress, setAccountAddress] = useState(null);
  const [currentCount, setCurrentCount] = useState(null);
  const [localCount, setLocalCount] = useState(null);
  const [can1VoteCount, setCan1VoteCount] = useState(null);
  const [can2VoteCount, setCan2VoteCount] = useState(null);
  const [can3VoteCount, setCan3VoteCount] = useState(null);
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
      <h1> Ballot System</h1>
      <Row>
        <Col><Button className="btn-wallet"
      onClick={
        isConnectedToPeraWallet ? handleDisconnectWalletClick : handleConnectWalletClick
      }>
      {isConnectedToPeraWallet ? "Disconnect Wallet" : "Connect Wallet"}
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
        <input id='seat' type='text' placeholder='Seat'></input>
        <input id='area' type='text' placeholder='Area'></input>
        <input id='state' type='text' placeholder='State'></input>
      <Col>
      <Button className="btn-add-local"
     onClick={
        () => callCounterApplication('InitParliamentSeatDemo1')
        //document.getElementById("seat").value,
      }>
      Init Parliament Seat Demo 1
    </Button>

    <Button className="btn-add-local"
     onClick={
        () => callCounterApplication('InitParliamentSeatDemo2')
      }>
      Init Parliament Seat Demo 2
    </Button>
    </Col>

    <Col>
    <h3>Local Count</h3>
    <span className='local-counter-text'>{localCount}</span>
    </Col>
    
    <Col>
          <Button className="btn-dec-local" 
     onClick={
      // add the local deduct method
      () => callCounterApplication('InitStateSeatDemo1')
      }>
      Init State Seat Demo 1
    </Button>
    <Button className="btn-dec-local" 
     onClick={
      // add the local deduct method
      () => callCounterApplication('InitStateSeatDemo2')
      }>
      Init State Seat Demo 2
    </Button>
    </Col>

    
    <Button className="btn-dec-local" 
     onClick={
      // add the local deduct method
      () => callCounterApplication('VoteCandidate1')
      }>
      Vote Candidate 1
    </Button>
    <span className='local-counter-text'>{can1VoteCount}</span>
    <Button className="btn-dec-local" 
     onClick={
      // add the local deduct method
      () => callCounterApplication('VoteCandidate2')
      }>
      Vote Candidate 2
    </Button>
    <span className='local-counter-text'>{can2VoteCount}</span>
    <Button className="btn-dec-local" 
     onClick={
      // add the local deduct method
      () => callCounterApplication('VoteCandidate3')
      }>
      Vote Candidate 3
    </Button>

    <Button className="btn-dec-local" 
     onClick={
      // add the local deduct method
      () => callCounterApplication('GetSeatNo')
      }>
      Get Seat No
    </Button>

    <Button className="btn-dec-local" 
     onClick={
      // add the local deduct method
      () => callCounterApplication('GetSeatArea')
      }>
      Get Seat Area
    </Button>

    <Button className="btn-dec-local" 
     onClick={
      // add the local deduct method
      () => callCounterApplication('GetSeatState')
      }>
      Get Seat State
    </Button>
    <span className='local-counter-text'>{can3VoteCount}</span>
        </Row>
        <Row>
          <Col><Button className="btn-add-global"
     onClick={
      // add the global add function
        () => callCounterApplication('DebugGlobal')
      }>
      DEBUG global
    </Button></Col>
    <Col>
    <h3>Global Count</h3>
    <span className='counter-text'>{currentCount}</span>
    </Col>
          <Col><Button className="btn-dec-global" 
     onClick={
      // add the deduct global function
      () => callCounterApplication('DebugLocal')
      }>
      DEBUG local
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

    async function printSeatidState() {
      try {
        const counter = await algod.getApplicationByID(appIndex).do();
        console.log(counter)
        if (!counter.params['global-state'][0].value.uint) {
          const decodedString = Buffer.from(counter.params['global-state'][0].value.bytes, 'base64').toString();
          setCurrentCount(decodedString);
        } else {
          setCurrentCount(0);
        }
      } catch (e) {
        console.error('There was an error connecting to the algorand node: ', e)
      }
    }
    async function checkVoteCountState() {
      try {
        const counter = await algod.getApplicationByID(appIndex).do();
        console.log(counter)
        if (!!counter.params['global-state'][5].value.uint) {
          setCan1VoteCount(counter.params['global-state'][5].value.uint);
        } else {
          setCan1VoteCount(69);
        }
        if (!!counter.params['global-state'][8].value.uint) {
          setCan2VoteCount(counter.params['global-state'][8].value.uint);
        } else {
          setCan2VoteCount(6969);
        }
        if (!!counter.params['global-state'][11].value.uint) {
          setCan3VoteCount(counter.params['global-state'][11].value.uint);
        } else {
          setCan3VoteCount(6996);
        }
      } catch (e) {
        console.error('There was an error connecting to the algorand node: ', e)
      }
    }

    async function checkCounterState() {
      try {
        const counter = await algod.getApplicationByID(appIndex).do();
        console.log(counter)
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
        console.log(accountInfo);
      } catch (e) {
        console.error('There was an error connecting to the algorand node: ', e)
      }
    }

    async function callCounterApplication(action) {
      try {
        // get suggested params
        const suggestedParams = await algod.getTransactionParams().do();
        const appArgs = [new Uint8Array(Buffer.from(action)),];
                        //new Uint8Array(Buffer.from(arg1)),
                        //new Uint8Array(Buffer.from(arg2)),
                        //new Uint8Array(Buffer.from(arg3))];
        
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
        checkVoteCountState();
        printSeatidState();
        //checkCounterState();
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
