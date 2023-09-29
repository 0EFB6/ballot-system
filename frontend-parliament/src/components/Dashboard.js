import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import { useEffect, useState } from 'react';
import algosdk, { waitForConfirmation } from 'algosdk';

const appIndex = 396310465;
const algod = new algosdk.Algodv2('','https://testnet-api.algonode.cloud', 443);

export default function Dashboard({optInToApp, isOptIn}) { 
  const [can1VoteCount, setCan1VoteCount] = useState(null);
  const [can2VoteCount, setCan2VoteCount] = useState(null);
  const [can3VoteCount, setCan3VoteCount] = useState(null);

  async function checkVoteCountState() {
    try
    {
      const counter = await algod.getApplicationByID(appIndex).do();
      let can1Index = -1;
      let can2Index = -1;
      let can3Index = -1;
  
      for (let i = 0; i < counter.params['global-state'].length; i++) {
        if (counter.params['global-state'][i].key == "QzFWb3Rlcw==") can1Index = i;
        else if (counter.params['global-state'][i].key == "QzJWb3Rlcw==") can2Index = i;
        else if (counter.params['global-state'][i].key == "QzNWb3Rlcw==") can3Index = i;
      }

      if (can1Index !== -1) setCan1VoteCount(counter.params['global-state'][can1Index].value.uint);
      else setCan1VoteCount(69);
      if (can2Index !== -1) setCan2VoteCount(counter.params['global-state'][can2Index].value.uint);
      else setCan2VoteCount(6969);
      if (can3Index !== -1) setCan3VoteCount(counter.params['global-state'][can3Index].value.uint);
      else setCan3VoteCount(6996);
    }
    catch (e)
    {
      console.error('There was an error connecting to the algorand node: ', e);
    }
  }

  checkVoteCountState();

    return (
    <Container className='text-white min-h-screen'>
        <h1 className='text-4xl text-white m-4 font-semibold'>Welcome back,</h1>

        {/* Opt in to App notification */}
        {isOptIn ?
        <div className='border-2 border-cyan-500 p-4 rounded-xl m-8 relative'>
          Opt in successful.
        </div>
        :
        <div className='border-2 border-cyan-500 p-4 rounded-xl m-8 relative'>
          <h1 className='inline text-xl mr-4'>You have yet to opt in to Ballot.</h1>
          <Button className="rounded-full inline"
            onClick={
            () => optInToApp()
            }>
            Opt-in
          </Button>
        </div>}

        {/* eKYC notification */}
        <div className='border-2 border-cyan-500 p-4 rounded-xl m-8 relative'>
          <h1 className='inline text-xl mr-4'>You have yet to perform e-KYC.</h1>
          <Button className="rounded-full inline">
            Perform e-KYC
          </Button>
        </div>

        {/* Latest Results*/}
        <div>
          <h1 className='text-3xl font-bold'>Latest Results</h1>
          <h2 className='ml-8 mt-4'>PARLIMEN P.045 BUKIT MERTAJAM</h2>
          <h2 className='ml-8'>28 SEPTEMBER 2023</h2>
          <table class="table-auto w-full border-collapse border-2 border-slate-500 border-spacing-2 m-4 rounded-lg">
            <thead>
              <tr>
                <th className='border-2 border-slate-500 p-2'>Candidate</th>
                <th className='border-2 border-slate-500 p-2'>Party</th>
                <th className='border-2 border-slate-500 p-2'>Number of Votes</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className='border-2 border-slate-500 p-2'>STEVEN SIM CHEE KEONG</td>
                <td className='border-2 border-slate-500 p-2'>PAKATAN HARAPAN (PH)<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/PH_aCpmiWX717.png' alt='Pakatan Harapan'/></td>
                <td className='border-2 border-slate-500 p-2'>{can1VoteCount}</td>
              </tr>
              <tr>
                <td className='border-2 border-slate-500 p-2'>AH PANG</td>
                <td className='border-2 border-slate-500 p-2'>BARISAN NASIONAL (BN)<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/BN.png' alt='Barisan Nasional'/></td>
                <td className='border-2 border-slate-500 p-2'>{can2VoteCount}</td>
              </tr>
              <tr>
                <td className='border-2 border-slate-500 p-2'>STEVEN KOH</td>
                <td className='border-2 border-slate-500 p-2'>PERIKATAN NASIONAL (PN)<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/PN.png' alt='Perikatan Nasional'/></td>
                <td className='border-2 border-slate-500 p-2'>{can3VoteCount}</td>
              </tr>
            </tbody>
          </table>
        </div>
  </Container>
)}