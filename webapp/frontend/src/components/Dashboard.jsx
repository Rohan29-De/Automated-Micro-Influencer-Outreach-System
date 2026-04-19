import { useState } from 'react'
import Sidebar from './Sidebar'
import StepWizard from './StepWizard'
import InfluencerTable from './InfluencerTable'
import SegmentsView from './SegmentsView'
import CampaignView from './CampaignView'

export default function Dashboard() {
  const [currentStep, setCurrentStep] = useState(1)
  const [discoveryConfig, setDiscoveryConfig] = useState({ niche: '', platform: '' })
  const [influencers, setInfluencers] = useState([])
  const [enrichedInfluencers, setEnrichedInfluencers] = useState([])
  const [segments, setSegments] = useState({})
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleDiscoveryComplete = (data) => {
    setInfluencers(data)
    setCurrentStep(2)
  }

  const handleEnrichComplete = (data) => {
    setEnrichedInfluencers(data)
    setCurrentStep(3)
  }

  const handleSegmentsComplete = (segData) => {
    setSegments(segData)
    setCurrentStep(4)
  }

  const handleMessagesComplete = (msgData) => {
    setMessages(msgData)
    setCurrentStep(5)
  }

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <StepWizard
            onDiscoveryComplete={handleDiscoveryComplete}
            setIsLoading={setIsLoading}
            config={discoveryConfig}
            setConfig={setDiscoveryConfig}
          />
        )
      case 2:
        return (
          <InfluencerTable
            influencers={influencers}
            onEnrichComplete={handleEnrichComplete}
            setIsLoading={setIsLoading}
          />
        )
      case 3:
        return (
          <SegmentsView
            enrichedInfluencers={enrichedInfluencers}
            onSegmentsComplete={handleSegmentsComplete}
            setIsLoading={setIsLoading}
          />
        )
      case 4:
      case 5:
        return (
          <CampaignView
            enrichedInfluencers={enrichedInfluencers}
            onMessagesComplete={handleMessagesComplete}
            messages={messages}
            setIsLoading={setIsLoading}
          />
        )
      default:
        return null
    }
  }

  return (
    <div className="flex min-h-screen" style={{ backgroundColor: 'var(--bg-primary)' }}>
      <Sidebar currentStep={currentStep} onStepClick={setCurrentStep} />

      <main className="flex-1 ml-60 p-8">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold" style={{ color: 'var(--text-primary)' }}>
              🎯 InfluenceIQ
            </h1>
            <p style={{ color: 'var(--text-secondary)', marginTop: 4 }}>
              Micro-Influencer Outreach System
            </p>
          </div>
          <div className="px-4 py-2 rounded-lg" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border)' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Step </span>
            <span style={{ color: 'var(--accent)', fontWeight: 'bold' }}>{currentStep}</span>
            <span style={{ color: 'var(--text-secondary)' }}> of 5</span>
          </div>
        </header>

        {isLoading && (
          <div className="mb-4 p-3 rounded-lg" style={{ backgroundColor: 'rgba(124, 58, 237, 0.1)', border: '1px solid var(--accent)' }}>
            <span style={{ color: 'var(--accent-light)' }}>⏳ Loading...</span>
          </div>
        )}

        {renderStep()}
      </main>
    </div>
  )
}