import { useState } from 'react'

export default function MessageModal({ influencer, messageData, onClose }) {
  const [copied, setCopied] = useState(null)

  const copyToClipboard = (text, type) => {
    navigator.clipboard.writeText(text)
    setCopied(type)
    setTimeout(() => setCopied(null), 2000)
  }

  const emailPitch = messageData?.email_pitch || 'No email generated yet...'
  const dmPitch = messageData?.dm_pitch || 'No DM generated yet...'

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50" style={{ backgroundColor: 'rgba(0,0,0,0.7)' }} onClick={onClose}>
      <div className="card max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="flex justify-between items-start mb-6">
          <div>
            <h3 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>Outreach Messages</h3>
            <p style={{ color: 'var(--text-secondary)' }}>{influencer?.name} • {influencer?.handle}</p>
          </div>
          <button onClick={onClose} className="p-2 rounded-lg" style={{ backgroundColor: 'var(--bg-hover)' }}>✕</button>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-4">
          <button className="px-4 py-2 rounded-lg" style={{ backgroundColor: 'var(--accent)', color: 'white' }}>
            📧 Email Pitch
          </button>
          <button className="px-4 py-2 rounded-lg" style={{ backgroundColor: 'var(--bg-hover)', color: 'var(--text-secondary)' }}>
            📱 Instagram DM
          </button>
        </div>

        {/* Email Content */}
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>Subject: Collaboration Opportunity with Conversely AI</span>
            <button
              onClick={() => copyToClipboard(emailPitch, 'email')}
              className="text-sm px-3 py-1 rounded"
              style={{ backgroundColor: 'var(--bg-hover)', color: 'var(--accent)' }}
            >
              {copied === 'email' ? '✓ Copied!' : '📋 Copy Email'}
            </button>
          </div>
          <div className="p-4 rounded-lg" style={{ backgroundColor: 'var(--bg-hover)', whiteSpace: 'pre-wrap' }}>
            {emailPitch}
          </div>
          <div className="mt-2 text-xs" style={{ color: 'var(--text-secondary)' }}>
            {emailPitch.split(' ').length} words
          </div>
        </div>

        {/* DM Content */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>DM Message</span>
            <button
              onClick={() => copyToClipboard(dmPitch, 'dm')}
              className="text-sm px-3 py-1 rounded"
              style={{ backgroundColor: 'var(--bg-hover)', color: 'var(--accent)' }}
            >
              {copied === 'dm' ? '✓ Copied!' : '📋 Copy DM'}
            </button>
          </div>
          <div className="p-4 rounded-lg" style={{ backgroundColor: 'var(--bg-hover)', whiteSpace: 'pre-wrap' }}>
            {dmPitch}
          </div>
          <div className="mt-2 text-xs" style={{ color: 'var(--text-secondary)' }}>
            {dmPitch.split(' ').length} words
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-between items-center pt-4 border-t" style={{ borderColor: 'var(--border)' }}>
          <div>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Contact: {influencer?.contact_email}</p>
          </div>
          <a
            href={`mailto:${influencer?.contact_email}?subject=Collaboration Opportunity with Conversely AI&body=${encodeURIComponent(emailPitch)}`}
            className="btn-primary"
          >
            📤 Send via Gmail
          </a>
        </div>
      </div>
    </div>
  )
}