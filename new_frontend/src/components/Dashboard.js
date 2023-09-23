import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

export default function Dashboard({optInToApp}) {
    return (
    <Container className='text-white min-h-screen'>
        <h1 className='text-4xl text-white m-4 font-semibold'>Welcome back,</h1>

        {/* Opt in to App notification */}
        <div className='border-2 border-cyan-500 p-4 rounded-xl m-8 relative'>
          <h1 className='inline text-xl mr-4'>You have yet to opt in to Ballot.</h1>
          <Button className="rounded-full inline"
            onClick={
            () => optInToApp()
            }>
            Opt-in
          </Button>
        </div>

        {/* eKYC notification */}
        <div className='border-2 border-cyan-500 p-4 rounded-xl m-8 relative'>
          <h1 className='inline text-xl mr-4'>You have yet to perform e-KYC.</h1>
          <Button className="rounded-full inline">
            Perform e-KYC
          </Button>
        </div>

        {/* Latest Results */}
        <div>
          <h1 className='text-3xl font-bold'>Latest Results</h1>
          <h2 className='ml-8 mt-4'>PRK PARLIMEN P.161 PULAI</h2>
          <h2 className='ml-8'>9 SEPTEMBER 2023</h2>
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
                <td className='border-2 border-slate-500 p-2'>SAMSUDIN PKPKL</td>
                <td className='border-2 border-slate-500 p-2'>BEBAS (KUNCI)<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/KUNCI.png'/></td>
                <td className='border-2 border-slate-500 p-2'>528</td>
              </tr>
              <tr>
                <td className='border-2 border-slate-500 p-2'>ZULKIFLI JAAFAR</td>
                <td className='border-2 border-slate-500 p-2'>PERIKATAN NASIONAL (PN)<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/PN.png'/></td>
                <td className='border-2 border-slate-500 p-2'>29,642</td>
              </tr>
              <tr>
                <td className='border-2 border-slate-500 p-2'>SUHAIZAN KAYAT</td>
                <td className='border-2 border-slate-500 p-2'>PAKATAN HARAPAN (PH)<img className='aspect-video' src='https://mysprsemak.spr.gov.my/storage/logo_parti/PH_aCpmiWX717.png'/></td>
                <td className='border-2 border-slate-500 p-2'>48,283</td>
              </tr>
            </tbody>
          </table>
        </div>
  </Container>
)}