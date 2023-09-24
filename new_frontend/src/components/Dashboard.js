import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

export default function Dashboard({optInToApp, isOptIn}) {
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

        {/* Latest Results 1*/}
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
                <td className='border-2 border-slate-500 p-2'>69</td>
              </tr>
              <tr>
                <td className='border-2 border-slate-500 p-2'>AH PANG</td>
                <td className='border-2 border-slate-500 p-2'>BARISAN NASIONAL (BN)<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/BN.png' alt='Barisan Nasional'/></td>
                <td className='border-2 border-slate-500 p-2'>29642</td>
              </tr>
              <tr>
                <td className='border-2 border-slate-500 p-2'>STEVEN KOH</td>
                <td className='border-2 border-slate-500 p-2'>PERIKATAN NASIONAL (PN)<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/PN.png' alt='Perikatan Nasional'/></td>
                <td className='border-2 border-slate-500 p-2'>48283</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Latest Results 2*/}
        <div>
          <h2 className='ml-8 mt-4'>DEWAN NEGERI SELANGOR N.34 BUKIT GASING</h2>
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
                <td className='border-2 border-slate-500 p-2'>RAJIV RISHYAKARAN</td>
                <td className='border-2 border-slate-500 p-2'>PAKATAN HARAPAN (PH)<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/PH_aCpmiWX717.png' alt='Pakatan Harapan'/></td>
                <td className='border-2 border-slate-500 p-2'>28227</td>
              </tr>
              <tr>
                <td className='border-2 border-slate-500 p-2'>NALLAN DHANABALAN</td>
                <td className='border-2 border-slate-500 p-2'>PERIKATAN NASIONAL (PN)<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/PN.png' alt='Perikatan Nasional'/></td>
                <td className='border-2 border-slate-500 p-2'>3255</td>
              </tr>
              <tr>
                <td className='border-2 border-slate-500 p-2'>VKK RAJA</td>
                <td className='border-2 border-slate-500 p-2'>MUDA<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/MUDA.png' alt='MUDA'/></td>
                <td className='border-2 border-slate-500 p-2'>1390</td>
              </tr>
            </tbody>
          </table>
        </div>
  </Container>
)}