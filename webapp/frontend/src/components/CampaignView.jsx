import { useState, useEffect } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'
import ProfileCard from './ProfileCard'
import MessageModal from './MessageModal'

const API = 'http://localhost:8001'

export default function CampaignView({ enrichedInfluencers, onMessagesComplete, messages, setIsLoading }) {
  const [generatedMessages, setGeneratedMessages] = useState([])
  const [priorityFilter, setPriorityFilter] = useState('All')
  const [selectedInfluencer, setSelectedInfluencer] = useState(null)
  const [messageData, setMessageData] = useState(null)

  const filterByPriority = (msgs) => {
    if (priorityFilter === 'All') return msgs
    return msgs.filter(m => m.outreach_priority === priorityFilter)
  }

  const generateAllMessages = async () => {
    setIsLoading(true)
    try {
      const { data } = await axios.post(`${API}/api/messages/generate-all`, { priority: priorityFilter })
      setGeneratedMessages(data.messages || [])
      toast.success(`${data.generated} messages generated!`)
      onMessagesComplete(data.messages)
    } catch (e) {
      toast.error('Failed to generate messages')
    } finally {
      setIsLoading(false)
    }
  }

  const viewMessage = async (inf) => {
    setSelectedInfluencer(inf)
    setIsLoading(true)
    try {
      const { data } = await axios.post(`${API}/api/messages/generate-one`, {
        influencer_id: inf.id,
        collaboration_type: 'Paid Sponsorship',
        brand_name: 'Conversely AI Private Limited'
      })
      setMessageData(data)
    } catch (e) {
      toast.error('Failed to generate message')
    } finally {
      setIsLoading(false)
    }
  }

  const totalReach = enrichedInfluencers?.reduce((a, b) => a + (b.estimated_reach || b.followers || 0), 0) || 0

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6" style={{ color: 'var(--text-primary)' }}>Campaign & Messages</h2>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Total Outreach', value: enrichedInfluencers?.length || 0 },
          { label: 'Emails Ready', value: generatedMessages.length },
          { label: 'DMs Ready', value: generatedMessages.length },
          { label: 'Est. Total Reach', value: (totalReach / 1000000).toFixed(1) + 'M' },
        ].map(stat => (
          <div key={stat.label} className="p-4 rounded-lg" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border)' }}>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{stat.label}</p>
            <p className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Priority Filter */}
      <div className="flex gap-2 mb-6">
        {['All', 'High', 'Medium', 'Low'].map(p => (
          <button
            key={p}
            onClick={() => setPriorityFilter(p)}
            className="px-4 py-2 rounded-lg"
            style={{
              backgroundColor: priorityFilter === p ? 'var(--accent)' : 'var(--bg-card)',
              color: priorityFilter === p ? 'white' : 'var(--text-secondary)',
              border: '1px solid var(--border)',
            }}
          >
            {p} Priority
          </button>
        ))}
        <button onClick={generateAllMessages} className="btn-primary ml-auto">
          ✉️ Generate All Messages
        </button>
      </div>

      {/* Message Cards */}
      {generatedMessages.length > 0 && (
        <div className="grid grid-cols-3 gap-4 mb-8">
          {filterByPriority(generatedMessages).slice(0, 9).map((msg, i) => (
            <div key={i} className="card">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 rounded-full flex items-center justify-center" style={{ background: 'var(--bg-hover)' }}>
                  {msg.name?.charAt(0)}
                </div>
                <div>
                  <p className="font-medium" style={{ color: 'var(--text-primary)' }}>{msg.name}</p>
                  <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>{msg.handle}</p>
                </div>
              </div>
              <button onClick={() => viewMessage(msg)} className="text-sm w-full py-2 rounded" style={{ backgroundColor: 'var(--bg-hover)', color: 'var(--accent)' }}>
                View Message 📩
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Workflow Explanation */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="card">
          <h3 className="font-bold mb-4" style={{ color: 'var(--text-primary)' }}>📧 Email Workflow</h3>
          <div className="space-y-2">
            {['1. Load influencer data', '2. Generate personalized pitch', '3. Format with template', '4. Validate email addresses', '5. Send via SendGrid API', '6. Track delivery status'].map((step, i) => (
              <div key={i} className="flex items-center gap-3">
                <span className="w-6 h-6 rounded-full flex items-center justify-center text-xs" style={{ backgroundColor: 'var(--accent)', color: 'white' }}>{i + 1}</span>
                <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>{step}</span>
              </div>
            ))}
          </div>
          <div className="mt-4">
            <span className="badge" style={{ backgroundColor: 'rgba(124,58,237,0.15)', color: 'var(--accent-light)' }}>SendGrid API</span>
          </div>
        </div>

        <div className="card">
          <h3 className="font-bold mb-4" style={{ color: 'var(--text-primary)' }}>📱 Instagram DM Workflow</h3>
          <div className="space-y-2">
            {['1. Load influencer handle', '2. Generate DM copy', '3. Format for DM length', '4. Prepare Instagram Graph API', '5. Send via Meta API', '6. Track sent status'].map((step, i) => (
              <div key={i} className="flex items-center gap-3">
                <span className="w-6 h-6 rounded-full flex items-center justify-center text-xs" style={{ backgroundColor: 'var(--accent)', color: 'white' }}>{i + 1}</span>
                <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>{step}</span>
              </div>
            ))}
          </div>
          <div className="mt-4">
            <span className="badge" style={{ backgroundColor: 'rgba(20,184,166,0.15)', color: '#2dd4bf' }}>Meta Graph API</span>
          </div>
        </div>
      </div>

      {/* Export */}
      <button className="btn-primary">
        📥 Export Campaign CSV
      </button>

      {selectedInfluencer && messageData && (
        <MessageModal
          influencer={selectedInfluencer}
          messageData={messageData}
          onClose={() => { setSelectedInfluencer(null); setMessageData(null); }}
        />
      )}
    </div>
  )
}