import {PeraWalletConnect} from '@perawallet/connect';
import algosdk, { waitForConfirmation } from 'algosdk';
import { useEffect, useState } from 'react';
import Header from './Header';
import Dashboard from './Dashboard';
import LandingPage from './LandingPage';
import State from './State';
import { Routes, Route } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import General from './General';

// Create the PeraWalletConnect instance outside the component
const peraWallet = new PeraWalletConnect();

// The app ID on testnet
const appIndex = 385332013;

// connect to the algorand node
const algod = new algosdk.Algodv2('','https://testnet-api.algonode.cloud', 443);

function App() {
  const [accountAddress, setAccountAddress] = useState(null);
  const [currentCount, setCurrentCount] = useState(null);
  const [localCount, setLocalCount] = useState(null);
  const isConnectedToPeraWallet = !!accountAddress;
  const [isOptIn, setIsOptIn] = useState(null);

  useEffect(() => {
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
    <Container className='m-0 p-0 min-w-full bg-slate-900 min-h-screen'>
      <meta name="Ballot" content="Ballot" title='Ballot'/>
      <Header isConnectedToPeraWallet={isConnectedToPeraWallet} handleConnectWalletClick={handleConnectWalletClick} handleDisconnectWalletClick={handleDisconnectWalletClick}/>
      
      {isConnectedToPeraWallet 
        ? <Routes>
            <Route path='/' element={<Dashboard optInToApp={optInToApp} isOptIn={isOptIn}/>}/>
            <Route path='/state' element={<State callCounterApplication={callCounterApplication} isOptIn={isOptIn} isConnectedToPeraWallet={isConnectedToPeraWallet}/>}/>
            <Route path='/general' element={<General callCounterApplication={callCounterApplication} isOptIn={isOptIn} isConnectedToPeraWallet={isConnectedToPeraWallet}/>}/>
          </Routes>
        : 
        <Routes>
            <Route path='/' element={<LandingPage handleConnectWalletClick={handleConnectWalletClick} handleDisconnectWalletClick={handleDisconnectWalletClick}/>}/>
            <Route path='/state' element={<State callCounterApplication={callCounterApplication} isOptIn={isOptIn} isConnectedToPeraWallet={isConnectedToPeraWallet}/>}/>
            <Route path='/general' element={<General callCounterApplication={callCounterApplication} isOptIn={isOptIn} isConnectedToPeraWallet={isConnectedToPeraWallet}/>}/>
          </Routes>}

      {/* Footer */} 
      <section className='bg-black p-4 text-white'>
          <h1 className='font-bold text-xl'>Ballot.</h1>
          <h2>{App.can3VoteCount}</h2>
          <p>Made with love, Ballot&copy; {new Date().getFullYear()}. All rights reserved. By Malaysians, for Malaysians.</p>
      </section>
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
    setIsOptIn(true);
  }

  async function callCounterApplication(action) {
    try {
      // get suggested params
      const suggestedParams = await algod.getTransactionParams().do();
      const appArgs = [new Uint8Array(Buffer.from(action))];
      
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
    
    } catch (e) {
      console.error(`There was an error calling the counter app: ${e}`);
    }
  }
}

export default App;
