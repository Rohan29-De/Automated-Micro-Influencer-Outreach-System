export default function ProfileCard({ influencer, onClose, onGenerateMessage }) {
  if (!influencer) return null

  const getInitials = (name) => {
    return name?.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || '??'
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50" style={{ backgroundColor: 'rgba(0,0,0,0.7)' }} onClick={onClose}>
      <div className="card max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="flex items-start gap-4 mb-4">
          <div
            className="w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold"
            style={{ background: 'linear-gradient(135deg, var(--accent), #ec4899)' }}
          >
            {getInitials(influencer.name)}
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>{influencer.name}</h3>
            <p style={{ color: 'var(--text-secondary)' }}>{influencer.handle}</p>
          </div>
          <button onClick={onClose} className="p-2 rounded-lg" style={{ backgroundColor: 'var(--bg-hover)' }}>✕</button>
        </div>

        <div className="space-y-3 mb-4">
          <div className="flex justify-between">
            <span style={{ color: 'var(--text-secondary)' }}>Platform</span>
            <span style={{ color: 'var(--text-primary)' }}>{influencer.platform}</span>
          </div>
          <div className="flex justify-between">
            <span style={{ color: 'var(--text-secondary)' }}>Followers</span>
            <span style={{ color: 'var(--text-primary)' }}>{(influencer.followers || 0).toLocaleString()}</span>
          </div>
          <div className="flex justify-between">
            <span style={{ color: 'var(--text-secondary)' }}>Engagement</span>
            <span style={{ color: 'var(--text-primary)' }}>{influencer.engagement_rate}%</span>
          </div>
          <div className="flex justify-between">
            <span style={{ color: 'var(--text-secondary)' }}>City</span>
            <span style={{ color: 'var(--text-primary)' }}>{influencer.city}</span>
          </div>
          <div className="flex justify-between">
            <span style={{ color: 'var(--text-secondary)' }}>Brand Fit</span>
            <span style={{ color: 'var(--text-primary)' }}>{influencer.brand_fit_score}/10</span>
          </div>
        </div>

        {influencer.content_themes && (
          <div className="mb-4">
            <p className="text-sm mb-2" style={{ color: 'var(--text-secondary)' }}>Content Themes</p>
            <div className="flex flex-wrap gap-2">
              {influencer.content_themes.map((theme, i) => (
                <span key={i} className="px-2 py-1 rounded text-xs" style={{ backgroundColor: 'var(--bg-hover)', color: 'var(--text-secondary)' }}>
                  {theme}
                </span>
              ))}
            </div>
          </div>
        )}

        {influencer.recent_post_topic && (
          <div className="mb-4 p-3 rounded-lg" style={{ backgroundColor: 'var(--bg-hover)' }}>
            <p className="text-xs mb-1" style={{ color: 'var(--text-secondary)' }}>Recent Post</p>
            <p className="text-sm" style={{ color: 'var(--text-primary)' }}>{influencer.recent_post_topic.slice(0, 60)}...</p>
          </div>
        )}

        <button onClick={() => onGenerateMessage?.(influencer)} className="btn-primary w-full">
          ✉️ Generate Message
        </button>
      </div>
    </div>
  )
}