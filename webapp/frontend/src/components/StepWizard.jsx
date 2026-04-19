import { useState, useEffect } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

const API = 'http://localhost:8001'

const niches = [
  { id: 'Beauty', icon: '💄', label: 'Beauty' },
  { id: 'Fashion', icon: '👗', label: 'Fashion' },
  { id: 'Fitness', icon: '💪', label: 'Fitness' },
  { id: 'Finance', icon: '💰', label: 'Finance' },
  { id: 'Lifestyle', icon: '🌟', label: 'Lifestyle' },
  { id: 'Education', icon: '📚', label: 'Education' },
]

const platforms = [
  { id: 'YouTube', icon: '▶️', label: 'YouTube' },
  { id: 'Instagram', icon: '📸', label: 'Instagram' },
  { id: 'Both', icon: '🔀', label: 'Both' },
]

export default function StepWizard({ onDiscoveryComplete, setIsLoading, config, setConfig }) {
  const [targetCount, setTargetCount] = useState(50)
  const [isPolling, setIsPolling] = useState(false)
  const [progress, setProgress] = useState(0)
  const [statusMsg, setStatusMsg] = useState('')

  const canStart = config.niche && config.platform

  const startDiscovery = async () => {
    if (!canStart) return

    setIsLoading(true)
    setIsPolling(true)
    setProgress(10)
    setStatusMsg('Starting discovery...')

    try {
      await axios.post(`${API}/api/discover`, {
        niche: config.niche,
        platform: config.platform,
        target_count: targetCount
      })

      const poll = setInterval(async () => {
        try {
          const { data } = await axios.get(`${API}/api/discover/status`)
          setProgress(data.progress)
          setStatusMsg(data.message)

          if (data.status === 'complete') {
            clearInterval(poll)
            setIsPolling(false)

            const results = await axios.get(`${API}/api/discover/results`)
            onDiscoveryComplete(results.data.influencers || [])
            toast.success(`Found ${results.data.count} influencers!`)
          } else if (data.status === 'error') {
            clearInterval(poll)
            setIsPolling(false)
            toast.error(data.message || 'Discovery failed')
          }
        } catch (e) {
          clearInterval(poll)
          setIsPolling(false)
        }
      }, 2000)

    } catch (e) {
      toast.error('Failed to start discovery')
      setIsPolling(false)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--text-primary)' }}>Discover Influencers</h2>
      <p className="mb-6" style={{ color: 'var(--text-secondary)' }}>Find real Indian micro-influencers</p>

      {/* Niche Selection */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-secondary)' }}>Choose Niche</h3>
        <div className="grid grid-cols-3 gap-3">
          {niches.map(n => (
            <button
              key={n.id}
              onClick={() => setConfig({ ...config, niche: n.id })}
              className="p-4 rounded-lg border-2 transition-all"
              style={{
                borderColor: config.niche === n.id ? 'var(--accent)' : 'var(--border)',
                backgroundColor: config.niche === n.id ? 'rgba(124, 58, 237, 0.1)' : 'var(--bg-hover)',
                boxShadow: config.niche === n.id ? '0 0 20px var(--accent-glow)' : 'none',
              }}
            >
              <span className="text-2xl">{n.icon}</span>
              <span className="block mt-2 font-medium">{n.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Platform Selection */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-secondary)' }}>Choose Platform</h3>
        <div className="grid grid-cols-3 gap-3">
          {platforms.map(p => (
            <button
              key={p.id}
              onClick={() => setConfig({ ...config, platform: p.id })}
              className="p-4 rounded-lg border-2 transition-all"
              style={{
                borderColor: config.platform === p.id ? 'var(--accent)' : 'var(--border)',
                backgroundColor: config.platform === p.id ? 'rgba(124, 58, 237, 0.1)' : 'var(--bg-hover)',
                boxShadow: config.platform === p.id ? '0 0 20px var(--accent-glow)' : 'none',
              }}
            >
              <span className="text-2xl">{p.icon}</span>
              <span className="block mt-2 font-medium">{p.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Target Count */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-secondary)' }}>
          Target Influencers: {targetCount}
        </h3>
        <input
          type="range"
          min="10"
          max="100"
          step="10"
          value={targetCount}
          onChange={e => setTargetCount(Number(e.target.value))}
          className="w-full"
          style={{ accentColor: 'var(--accent)' }}
        />
      </div>

      {/* Progress */}
      {isPolling && (
        <div className="mb-6">
          <div className="h-2 rounded-full" style={{ backgroundColor: 'var(--bg-hover)' }}>
            <div
              className="h-2 rounded-full transition-all duration-500"
              style={{ width: `${progress}%`, backgroundColor: 'var(--accent)' }}
            />
          </div>
          <p className="mt-2 text-sm" style={{ color: 'var(--text-secondary)' }}>{statusMsg}</p>
        </div>
      )}

      {/* Start Button */}
      <button
        onClick={startDiscovery}
        disabled={!canStart || isPolling}
        className="btn-primary w-full py-3 text-lg"
      >
        {isPolling ? '⏳ Discovering...' : '🚀 Start Discovery'}
      </button>
    </div>
  )
}