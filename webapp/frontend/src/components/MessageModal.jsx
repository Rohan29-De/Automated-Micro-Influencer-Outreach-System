import { X, Copy, Check } from 'lucide-react'
import { useState } from 'react'

export default function MessageModal({ influencer, onClose }) {
  const [copied, setCopied] = useState(null)

  if (!influencer) return null

  const copyToClipboard = (text, type) => {
    navigator.clipboard.writeText(text)
    setCopied(type)
    setTimeout(() => setCopied(null), 2000)
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-2xl p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="flex justify-between items-start mb-6">
          <div>
            <h3 className="text-xl font-bold">Outreach Messages</h3>
            <p className="text-gray-500">{influencer.name} • {influencer.handle}</p>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-6">
          <div>
            <div className="flex justify-between items-center mb-2">
              <h4 className="font-medium">Email Pitch</h4>
              <button
                onClick={() => copyToClipboard(influencer.email_pitch || 'Sample email', 'email')}
                className="flex items-center gap-1 text-sm text-purple-600 hover:text-purple-700"
              >
                {copied === 'email' ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                Copy
              </button>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg text-sm text-gray-700 whitespace-pre-wrap">
              {influencer.email_pitch || 'Email pitch will appear here after generation...'}
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center mb-2">
              <h4 className="font-medium">DM Pitch</h4>
              <button
                onClick={() => copyToClipboard(influencer.dm_pitch || 'Sample DM', 'dm')}
                className="flex items-center gap-1 text-sm text-purple-600 hover:text-purple-700"
              >
                {copied === 'dm' ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                Copy
              </button>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg text-sm text-gray-700 whitespace-pre-wrap">
              {influencer.dm_pitch || 'DM pitch will appear here after generation...'}
            </div>
          </div>
        </div>

        <div className="mt-6 flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 bg-gray-100 text-gray-700 py-2 rounded-lg hover:bg-gray-200"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}