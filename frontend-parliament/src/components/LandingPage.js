import Button from 'react-bootstrap/Button';

export default function LandingPage({handleConnectWalletClick, handleDisconnectWalletClick}) {
    return(
    <div className="mt-8 text-white">
        <section className="mx-[15%] grid grid-cols-2">
            <div className="m-8 mt-40">
                <h1 className="text-5xl font-bold text-white mb-8">Ballot.</h1>
                <p className="text-white text-xl text-justify">
                Welcome to Ballot, your trusted voting platform. With Ballot, 
                you can easily and securely cast your vote in various elections from the comfort of your own home. 
                All without leaving your home.
                </p>
                <h2 className="font-bold text-2xl mt-12">Connect Your Pera Wallet to Get Started</h2>
                <Button className="text-white rounded-full mt-3"
                    onClick={handleConnectWalletClick}>
                    Connect to Pera Wallet
                </Button>
            </div>
            <img src="map_of_malaysia.png" alt="Map of Malaysia" className="aspect-video object-cover"/>
        </section>
        <section className='bg-slate-700 mt-40 w-full'>
            <div className='grid grid-cols-3 gap-4'>
                <div className='justify-self-center	m-12 mb-20'>
                <svg className='w-28 fill-white mx-auto my-8' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M96 80c0-26.5 21.5-48 48-48H432c26.5 0 48 21.5 48 48V384H96V80zm313 47c-9.4-9.4-24.6-9.4-33.9 0l-111 111-47-47c-9.4-9.4-24.6-9.4-33.9 0s-9.4 24.6 0 33.9l64 64c9.4 9.4 24.6 9.4 33.9 0L409 161c9.4-9.4 9.4-24.6 0-33.9zM0 336c0-26.5 21.5-48 48-48H64V416H512V288h16c26.5 0 48 21.5 48 48v96c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V336z"/></svg>
                    <h2 className='font-bold text-2xl'>Election Results on Ballot</h2>
                    <p className='text-justify'>
                        Stay informed about election results with Ballot. We will announce the outcomes shortly after 
                        the voting period concludes, ensuring transparency and trust in the process.
                    </p>
                </div>
                <div className='justify-self-center	m-12 mb-20'>
                <svg className='w-24 fill-white mx-auto my-8' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><style></style><path d="M256 0c4.6 0 9.2 1 13.4 2.9L457.7 82.8c22 9.3 38.4 31 38.3 57.2c-.5 99.2-41.3 280.7-213.6 363.2c-16.7 8-36.1 8-52.8 0C57.3 420.7 16.5 239.2 16 140c-.1-26.2 16.3-47.9 38.3-57.2L242.7 2.9C246.8 1 251.4 0 256 0zm0 66.8V444.8C394 378 431.1 230.1 432 141.4L256 66.8l0 0z"/></svg>
                    <h2 className='font-bold text-2xl'>Security and Privacy with Ballot</h2>
                    <p className='text-justify'>
                        Your privacy and the security of your vote are our top priorities. Ballot employs advanced 
                        encryption and security measures to protect your data and maintain the integrity of the voting process.
                    </p>
                </div>
                <div className='justify-self-center	m-12 mb-20'>
                <svg className='w-20 fill-white mx-auto my-8' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><style></style><path d="M0 256L28.5 28c2-16 15.6-28 31.8-28H228.9c15 0 27.1 12.1 27.1 27.1c0 3.2-.6 6.5-1.7 9.5L208 160H347.3c20.2 0 36.7 16.4 36.7 36.7c0 7.4-2.2 14.6-6.4 20.7l-192.2 281c-5.9 8.6-15.6 13.7-25.9 13.7h-2.9c-15.7 0-28.5-12.8-28.5-28.5c0-2.3 .3-4.6 .9-6.9L176 288H32c-17.7 0-32-14.3-32-32z"/></svg>
                    <h2 className='font-bold text-2xl'>Lightning-fast Support</h2>
                    <p className='text-justify'>
                        For additional support or any concerns, please reach out to our dedicated team and we will come to support you as soon as possible.
                    </p>
                </div>
            </div>
        </section>
    </div>
)}