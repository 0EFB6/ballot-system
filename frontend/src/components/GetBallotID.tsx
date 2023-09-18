import * as algokit from '@algorandfoundation/algokit-utils'
import { TransactionSignerAccount } from '@algorandfoundation/algokit-utils/types/account'
import { AppDetails } from '@algorandfoundation/algokit-utils/types/app-client'
import { useWallet } from '@txnlab/use-wallet'
import { useSnackbar } from 'notistack'
import { useState } from 'react'
import { VotingAppClient } from '../contracts/VotingApp' // make sure to check import
import { getAlgodConfigFromViteEnvironment, getIndexerConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'

interface GetBallotIDInterface {
  openModal: boolean
  setModalState: (value: boolean) => void
}

const GetBallotID = ({ openModal, setModalState }: GetBallotIDInterface) => {
  const [loading, setLoading] = useState<boolean>(false)
  // const [contractInput, setContractInput] = useState<string>('')
  // my code
  // const [accInput, setAccInput] = useState<string>('')
  // const [customUIDInput, setCustomUIDInput] = useState<string>('')
  const [icNumInput, setIcNumInput] = useState<string>('')


  const algodConfig = getAlgodConfigFromViteEnvironment()
  const algodClient = algokit.getAlgoClient({
    server: algodConfig.server,
    port: algodConfig.port,
    token: algodConfig.token,
  })

  const indexerConfig = getIndexerConfigFromViteEnvironment()
  const indexer = algokit.getAlgoIndexerClient({
    server: indexerConfig.server,
    port: indexerConfig.port,
    token: indexerConfig.token,
  })

  const { enqueueSnackbar } = useSnackbar()
  const { signer, activeAddress } = useWallet()

  // const sendAppCall = async () => {
  //   setLoading(true)

  //   const appDetails = {
  //     resolveBy: 'creatorAndName',
  //     sender: { signer, addr: activeAddress } as TransactionSignerAccount,
  //     creatorAddress: activeAddress,
  //     findExistingUsing: indexer,
  //   } as AppDetails

  //   const appClient = new VotingAppClient(appDetails, algodClient)

  //   // Please note, in typical production scenarios,
  //   // you wouldn't want to use deploy directly from your frontend.
  //   // Instead, you would deploy your contract on your backend and reference it by id.
  //   // Given the simplicity of the starter contract, we are deploying it on the frontend
  //   // for demonstration purposes.
  //   const deployParams = {
  //     onSchemaBreak: 'append',
  //     onUpdate: 'append',
  //   }
  //   await appClient.deploy(deployParams).catch((e: Error) => {
  //     enqueueSnackbar(`Error deploying the contract: ${e.message}`, { variant: 'error' })
  //     setLoading(false)
  //     return
  //   })
  //   // This is where the application call is made. ContractInput is set as the input.
  //   const response = await appClient.hello({ name: contractInput }).catch((e: Error) => {
  //     enqueueSnackbar(`Error calling the contract: ${e.message}`, { variant: 'error' })
  //     setLoading(false)
  //     return
  //   })
  //   // This is where the response from the contract is displayed.
  //   enqueueSnackbar(`Response from the contract: ${response?.return}`, { variant: 'success' })
  //   setLoading(false)
  // }
  // my code

  const getBallotID = async () => {
    setLoading(true)

    const appDetails = {
      resolveBy: 'creatorAndName',
      sender: { signer, addr: activeAddress } as TransactionSignerAccount,
      creatorAddress: activeAddress,
      findExistingUsing: indexer,
    } as AppDetails

    const appClient = new VotingAppClient(appDetails, algodClient)

    // Please note, in typical production scenarios,
    // you wouldn't want to use deploy directly from your frontend.
    // Instead, you would deploy your contract on your backend and reference it by id.
    // Given the simplicity of the starter contract, we are deploying it on the frontend
    // for demonstration purposes.
    const deployParams = {
      onSchemaBreak: 'append',
      onUpdate: 'append',
    }
    await appClient.deploy(deployParams).catch((e: Error) => {
      enqueueSnackbar(`Error deploying the contract: ${e.message}`, { variant: 'error' })
      setLoading(false)
      return
    })
    // This is where the application call is made. ContractInput is set as the input.
    const response = await appClient.getUuid({ ic_num: icNumInput }).catch((e: Error) => {
      enqueueSnackbar(`Error calling the contract: ${e.message}`, { variant: 'error' })
      setLoading(false)
      return
    })
    // This is where the response from the contract is displayed.
    enqueueSnackbar(`Response from the contract: ${response?.return}`, { variant: 'success' })
    setLoading(false)
  }

  return (
    <dialog id="appcalls_modal" className={`modal ${openModal ? 'modal-open' : ''} bg-slate-200`}>
      <form method="dialog" className="modal-box">
        <h3 className="font-bold text-lg">Get Ballot</h3>
        <br />
        <input
          type="text"
          placeholder="Type in IC number"
          className="input input-bordered w-full"
          value={icNumInput}
          onChange={(e) => {
            setIcNumInput(e.target.value)
          }}
        />
        <div className="modal-action ">
          <button className="btn" onClick={() => setModalState(!openModal)}>
            Close
          </button>
          <button className={`btn`} onClick={getBallotID}>
            {loading ? <span className="loading loading-spinner" /> : 'Send application call'}
          </button>
        </div>
      </form>
    </dialog>
  )
}

export default GetBallotID