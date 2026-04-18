import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Dashboard from './components/Dashboard'
import StepWizard from './components/StepWizard'
import InfluencerTable from './components/InfluencerTable'
import MessageModal from './components/MessageModal'

function App() {
  const [currentStep, setCurrentStep] = useState(1)
  const [influencers, setInfluencers] = useState([])
  const [segments, setSegments] = useState({})
  const [selectedInfluencer, setSelectedInfluencer] = useState(null)

  const steps = [
    { id: 1, name: 'Discovery', description: 'Find influencers' },
    { id: 2, name: 'Enrichment', description: 'Add profile data' },
    { id: 3, name: 'Segments', description: 'Filter & group' },
    { id: 4, name: 'Messages', description: 'Generate outreach' },
  ]

  return (
    <div className="flex min-h-screen">
      <Sidebar currentStep={currentStep} onStepClick={setCurrentStep} />

      <main className="flex-1 ml-64 p-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Micro-Influencer Outreach</h1>
          <p className="text-gray-600 mt-1">Discover, enrich, and connect with Indian creators</p>
        </header>

        <StepWizard steps={steps} currentStep={currentStep} onStepClick={setCurrentStep} />

        <div className="mt-8">
          {currentStep === 1 && (
            <Dashboard onInfluencersFound={setInfluencers} />
          )}
          {currentStep === 2 && (
            <Dashboard onInfluencersFound={setInfluencers} />
          )}
          {currentStep === 3 && (
            <InfluencerTable influencers={influencers} segments={segments} onSelect={setSelectedInfluencer} />
          )}
          {currentStep === 4 && (
            <InfluencerTable influencers={influencers} segments={segments} onSelect={setSelectedInfluencer} />
          )}
        </div>

        {selectedInfluencer && (
          <MessageModal
            influencer={selectedInfluencer}
            onClose={() => setSelectedInfluencer(null)}
          />
        )}
      </main>
    </div>
  )
}

export default App