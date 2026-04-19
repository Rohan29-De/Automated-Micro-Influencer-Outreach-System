import { Search, Zap, FolderOpen, Mail, Rocket } from 'lucide-react'

const steps = [
  { id: 1, name: 'Discovery', icon: Search, desc: 'Find influencers' },
  { id: 2, name: 'Enrich & Filter', icon: Zap, desc: 'Profile data' },
  { id: 3, name: 'Segments', icon: FolderOpen, desc: 'Group & filter' },
  { id: 4, name: 'Messages', icon: Mail, desc: 'Generate outreach' },
  { id: 5, name: 'Campaign', icon: Rocket, desc: 'Send & track' },
]

export default function Sidebar({ currentStep, onStepClick }) {
  return (
    <aside className="fixed left-0 top-0 h-full w-60 p-4 flex flex-col" style={{ backgroundColor: 'var(--bg-card)', borderRight: '1px solid var(--border)' }}>
      <div className="flex items-center gap-2 mb-8 pt-4">
        <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: 'linear-gradient(135deg, var(--accent), #ec4899)' }}>
          <span className="text-xl">🎯</span>
        </div>
        <div>
          <h2 className="font-bold" style={{ color: 'var(--text-primary)' }}>InfluenceIQ</h2>
        </div>
      </div>

      <nav className="flex-1 space-y-2">
        {steps.map((step, index) => {
          const Icon = step.icon
          const isComplete = currentStep > step.id
          const isCurrent = currentStep === step.id

          return (
            <div key={step.id}>
              <button
                onClick={() => onStepClick(step.id)}
                className="w-full flex items-center gap-3 px-3 py-3 rounded-lg transition-all"
                style={{
                  backgroundColor: isCurrent ? 'var(--accent)' : 'transparent',
                  color: isCurrent ? 'white' : isComplete ? 'var(--success)' : 'var(--text-secondary)',
                }}
              >
                <div
                  className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
                  style={{
                    backgroundColor: isCurrent ? 'rgba(255,255,255,0.2)' : isComplete ? 'var(--success)' : 'var(--bg-hover)',
                  }}
                >
                  {isComplete ? '✓' : step.id}
                </div>
                <div className="text-left">
                  <p className="font-medium text-sm">{step.name}</p>
                  <p className="text-xs opacity-60">{step.desc}</p>
                </div>
              </button>
              {index < steps.length - 1 && (
                <div
                  className="w-0.5 mx-4 my-1"
                  style={{ backgroundColor: isComplete ? 'var(--success)' : 'var(--border)' }}
                />
              )}
            </div>
          )
        })}
      </nav>

      <div className="pt-4 border-t" style={{ borderColor: 'var(--border)' }}>
        <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>v1.0</p>
        <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>Powered by Groq + YouTube API</p>
      </div>
    </aside>
  )
}