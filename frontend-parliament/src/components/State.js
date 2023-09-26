import { Container } from "react-bootstrap";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from 'react-bootstrap/Button';

export default function State({callCounterApplication, isConnectedToPeraWallet, isOptIn}){
    const Area = "Bukit Gasing"
    const Number = "N34"
    const State = "Selangor"
    const Candidates = [
        {name:'RAJIV RISHYAKARAN', party:'PAKATAN HARAPAN (PH)', partyFlag:'https://mysprsemak.spr.gov.my/storage/logo_parti/PH_aCpmiWX717.png',img:'https://pbs.twimg.com/media/F1x-x83aAAAvjqw?format=jpg&name=large' },
        {name:'NALLAN DHANABALAN', party:'PERIKATAN NASIONAL (PN)', partyFlag:'https://mysprsemak.spr.gov.my/storage/logo_parti/PN.png', img:'https://malaysiagazette.com/wp-content/uploads/2021/06/B2CC8077-90D7-473F-AE39-BA5CB025636E.jpeg.webp'},
        {name:'VKK RAJA', party:'MUDA', partyFlag:'https://mysprsemak.spr.gov.my/storage/logo_parti/MUDA.png', img:'https://apicms.thestar.com.my/uploads/images/2023/08/03/2212404.jpg'}
    ]
    return ((!isConnectedToPeraWallet) ? <div className="text-5xl font-bold min-h-screen text-white">You have yet to connect to Pera Wallet or opt in to Ballot.</div> 
    :<Container className="text-white min-h-screen">
      <div className="m-8 text-3xl font-bold">
        <h1 className="text-5l">General Election - Dewan Negeri Selangor Ke-15</h1>
        <h1>{Area} ({Number})</h1>
        <h1>{State}</h1>
      </div>
      <Row className="m-8">
        {Candidates.map((item, index) => (
            <Col className="relative" key={index}>
                <img className="aspect-square w-full justify-content-center object-cover rounded-t-lg" alt={item.name} src={item.img}/>
                <div className='border-2 border-slate-500 p-2 rounded-b-lg text-xl'>
                <h1>{item.name}</h1>
                <h1>{item.party}</h1>
                <img className='aspect-video m-2 mx-auto' src={item.partyFlag} alt={item.party}/>
            </div>
            <Button className="m-4 text-xl font-semibold rounded-full px-4 absolute left-[50%] translate-x-[-75%]" onClick={() => callCounterApplication(`VoteCandidate${index + 1}`)}>Vote</Button>
            </Col>
        ))}
      </Row>
    </Container>
    )
}


/* 
    HARDCODED ALTERNATIVE

    <Row className="m-8">
    <Col className="relative">
        <img className="aspect-square w-full justify-content-center object-cover rounded-t-lg" alt="" src="https://scontent.fkul8-3.fna.fbcdn.net/v/t39.30808-6/312231048_680968926727300_7318896265877536756_n.jpg?stp=dst-jpg_p526x296&_nc_cat=104&ccb=1-7&_nc_sid=813123&_nc_ohc=SQkoKwWUSUAAX8EgFpN&_nc_ht=scontent.fkul8-3.fna&oh=00_AfAwzRVOqSSyLwS5H2NepbTT3zuK04WBDwFcFs_zuAHPhw&oe=6512F934"/>
        <div className='border-2 border-slate-500 p-2 rounded-b-lg text-xl'>
        <h1>STEVEN SIM CHEE KEONG</h1>
        <h1>PAKATAN HARAPAN (PH)</h1>
        <img className='aspect-video m-2 mx-auto' src='https://mysprsemak.spr.gov.my/storage/logo_parti/PH_aCpmiWX717.png' alt='Harapan'/>
        </div>

        <Button className="m-4 text-xl font-semibold rounded-full px-4 absolute left-[50%] translate-x-[-75%]" onClick={() => callCounterApplication()}>Vote</Button>
    </Col>
    <Col className="relative">
        <img className="aspect-square w-full justify-content-center object-cover rounded-t-lg" src="https://img.astroawani.com/2022-11/61668486362_TBtanyangpeng.jpg"/>
        <div className='border-2 border-slate-500 p-2 rounded-b-lg text-xl'>
        <h1>AH PANG</h1>
        <h1>BARISAN NASIONAL OF MALAYSIA (BN)</h1>
        <img className='aspect-video m-2 mx-auto' src='https://mysprsemak.spr.gov.my/storage/logo_parti/BN.png' alt='Barisan'/>
        </div>

        <Button className="m-4 text-xl font-semibold rounded-full px-4 absolute left-[50%] translate-x-[-75%]" onClick={() => callCounterApplication()}>Vote</Button>
    </Col>
    <Col className="relative">
        <img className="aspect-square w-full justify-content-center object-cover rounded-t-lg" src="https://scontent.fkul8-1.fna.fbcdn.net/v/t39.30808-6/364165315_258115340445733_2823740976136437526_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=a2f6c7&_nc_ohc=yflh_Dw242AAX-NuVGK&_nc_ht=scontent.fkul8-1.fna&oh=00_AfD_7XKhbtp-EJQupQxOvOlAmzuv0EHVopfQT-tNiXEHhg&oe=65138973"/>
        <div className='border-2 border-slate-500 p-2 rounded-b-lg text-xl'>
        <h1>STEVEN KOH</h1>
        <h1>PERIKATAN NASIONAL (PN)</h1>
        <img className='aspect-video m-2 mx-auto' src='https://mysprsemak.spr.gov.my/storage/logo_parti/PN.png' alt='Perikatan'/>
        </div>

        <Button className="m-4 text-xl font-semibold rounded-full px-4 absolute left-[50%] translate-x-[-75%]" onClick={() => callCounterApplication()}>Vote</Button>
    </Col>
    </Row>
*/