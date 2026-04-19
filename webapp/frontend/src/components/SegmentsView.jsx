import { useState, useEffect } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'
import ProfileCard from './ProfileCard'

const API = 'http://localhost:8001'

const segmentInfo = {
  Segment_A: { emoji: '💄', name: 'Instagram Beauty & Skincare Stars', desc: 'High engagement beauty creators' },
  Segment_B: { emoji: '🎬', name: 'YouTube Fashion Creators', desc: 'Fashion & style influencers' },
  Segment_C: { emoji: '🗣️', name: 'Hindi/Hinglish High Engagement', desc: 'Regional language creators' },
}

export default function SegmentsView({ enrichedInfluencers, onSegmentsComplete, setIsLoading }) {
  const [segments, setSegments] = useState({})
  const [expanded, setExpanded] = useState(null)
  const [selectedProfile, setSelectedProfile] = useState(null)

  useEffect(() => {
    fetchSegments()
  }, [])

  const fetchSegments = async () => {
    setIsLoading(true)
    try {
      const { data } = await axios.get(`${API}/api/segments/segments`)
      if (data.error) throw new Error(data.error)
      setSegments(data)
      onSegmentsComplete(data)
    } catch (e) {
      // Fallback: create segments from enriched data
      const fallbackSegments = {
        Segment_A: { count: 0, influencers: enrichedInfluencers?.slice(0, 15) || [] },
        Segment_B: { count: 0, influencers: enrichedInfluencers?.slice(15, 30) || [] },
        Segment_C: { count: 0, influencers: enrichedInfluencers?.slice(30, 50) || [] },
      }
      fallbackSegments.Segment_A.count = fallbackSegments.Segment_A.influencers.length
      fallbackSegments.Segment_B.count = fallbackSegments.Segment_B.influencers.length
      fallbackSegments.Segment_C.count = fallbackSegments.Segment_C.influencers.length
      setSegments(fallbackSegments)
      onSegmentsComplete(fallbackSegments)
    } finally {
      setIsLoading(false)
    }
  }

  const generateSegmentMessages = async (segmentKey) => {
    try {
      await axios.post(`${API}/api/messages/generate-all`, { priority: 'High' })
      toast.success(`Messages generated for ${segmentInfo[segmentKey]?.name || segmentKey}`)
    } catch (e) {
      toast.error('Failed to generate messages')
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6" style={{ color: 'var(--text-primary)' }}>Audience Segments</h2>

      <div className="grid grid-cols-3 gap-6 mb-8">
        {Object.entries(segments).map(([key, data]) => {
          const info = segmentInfo[key] || { emoji: '📊', name: key, desc: '' }
          const influencers = data.influencers || []

          return (
            <div key={key} className="card">
              <div className="flex items-center gap-3 mb-3">
                <span className="text-3xl">{info.emoji}</span>
                <div>
                  <h3 className="font-bold" style={{ color: 'var(--text-primary)' }}>{info.name}</h3>
                  <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>{info.desc}</p>
                </div>
              </div>

              <div className="flex items-center justify-between mb-4">
                <span className="badge badge-high">{influencers.length} influencers</span>
              </div>

              {/* Top 3 preview */}
              <div className="space-y-2 mb-4">
                {influencers.slice(0, 3).map((inf, i) => (
                  <div key={i} className="flex items-center justify-between p-2 rounded" style={{ backgroundColor: 'var(--bg-hover)' }}>
                    <span className="text-sm" style={{ color: 'var(--text-primary)' }}>{inf.name}</span>
                    <span className="text-xs" style={{ color: 'var(--text-secondary)' }}>{(inf.followers / 1000).toFixed(1)}K</span>
                  </div>
                ))}
              </div>

              <button
                onClick={() => setExpanded(expanded === key ? null : key)}
                className="text-sm mb-2"
                style={{ color: 'var(--accent)' }}
              >
                {expanded === key ? '← Collapse' : `View All ${influencers.length} →`}
              </button>

              <button onClick={() => generateSegmentMessages(key)} className="btn-primary w-full text-sm">
                ✉️ Generate Messages
              </button>
            </div>
          )
        })}
      </div>

      {expanded && segments[expanded] && (
        <div className="card mb-6">
          <h3 className="font-bold mb-4" style={{ color: 'var(--text-primary)' }}>
            {segmentInfo[expanded]?.name || expanded} - All Influencers
          </h3>
          <div className="grid grid-cols-3 gap-4">
            {segments[expanded].influencers.map((inf, i) => (
              <div
                key={i}
                className="p-4 rounded-lg cursor-pointer"
                style={{ backgroundColor: 'var(--bg-hover)' }}
                onClick={() => setSelectedProfile(inf)}
              >
                <p className="font-medium" style={{ color: 'var(--text-primary)' }}>{inf.name}</p>
                <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{inf.handle}</p>
                <p className="text-xs mt-1" style={{ color: 'var(--text-secondary)' }}>{(inf.followers / 1000).toFixed(1)}K followers</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <button onClick={() => onSegmentsComplete(segments)} className="btn-primary">
        Next: Generate Messages →
      </button>

      {selectedProfile && (
        <ProfileCard influencer={selectedProfile} onClose={() => setSelectedProfile(null)} />
      )}
    </div>
  )
}