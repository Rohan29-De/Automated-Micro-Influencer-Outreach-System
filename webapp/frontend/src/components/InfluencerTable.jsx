import { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'
import ProfileCard from './ProfileCard'

const API = 'http://localhost:8001'

export default function InfluencerTable({ influencers, onEnrichComplete, setIsLoading }) {
  const [filters, setFilters] = useState({
    minEngagement: 2.0,
    minBrandFit: 5,
    niches: [],
    platforms: []
  })
  const [enrichedData, setEnrichedData] = useState(null)
  const [selectedProfile, setSelectedProfile] = useState(null)

  const handleEnrich = async () => {
    setIsLoading(true)
    try {
      const { data } = await axios.post(`${API}/api/enrich/enrich`, {
        min_engagement: filters.minEngagement,
        max_engagement: 10,
        min_brand_fit: filters.minBrandFit,
        niches: filters.niches,
        platforms: filters.platforms
      })
      setEnrichedData(data)
      toast.success(`${data.total} profiles enriched!`)
      onEnrichComplete(data.influencers)
    } catch (e) {
      toast.error('Enrichment failed')
    } finally {
      setIsLoading(false)
    }
  }

  const formatFollowers = (num) => {
    if (!num) return '0'
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
    return num
  }

  const getEngagementColor = (rate) => {
    if (rate >= 4) return 'var(--success)'
    if (rate >= 2) return 'var(--warning)'
    return 'var(--danger)'
  }

  const getPriorityBadge = (p) => {
    if (p === 'High') return 'badge-high'
    if (p === 'Medium') return 'badge-medium'
    return 'badge-low'
  }

  const getNicheBadge = (niche) => {
    const n = niche?.toLowerCase()
    if (n?.includes('beauty')) return 'badge-beauty'
    if (n?.includes('fashion')) return 'badge-fashion'
    if (n?.includes('skincare')) return 'badge-skincare'
    if (n?.includes('makeup')) return 'badge-makeup'
    return 'badge-high'
  }

  const displayData = enrichedData?.influencers || influencers

  return (
    <div>
      <div className="card mb-6">
        <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--text-primary)' }}>Filter & Enrich Profiles</h2>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          {[
            { label: 'Total', value: displayData.length },
            { label: 'Avg Engagement', value: displayData.length ? (displayData.reduce((a, b) => a + (b.engagement_rate || 0), 0) / displayData.length).toFixed(1) + '%' : '0%' },
            { label: 'Avg Brand Fit', value: displayData.length ? Math.round(displayData.reduce((a, b) => a + (b.brand_fit_score || 0), 0) / displayData.length) : 0 },
            { label: 'Platforms', value: [...new Set(displayData.map(i => i.platform))].length },
          ].map(stat => (
            <div key={stat.label} className="p-4 rounded-lg" style={{ backgroundColor: 'var(--bg-hover)' }}>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{stat.label}</p>
              <p className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>{stat.value}</p>
            </div>
          ))}
        </div>

        {/* Filters */}
        <div className="flex gap-6 mb-6">
          <div className="flex-1">
            <label className="block text-sm mb-2" style={{ color: 'var(--text-secondary)' }}>Min Engagement: {filters.minEngagement}</label>
            <input
              type="range"
              min="1"
              max="8"
              step="0.5"
              value={filters.minEngagement}
              onChange={e => setFilters({ ...filters, minEngagement: Number(e.target.value) })}
              className="w-full"
              style={{ accentColor: 'var(--accent)' }}
            />
          </div>
          <div className="flex-1">
            <label className="block text-sm mb-2" style={{ color: 'var(--text-secondary)' }}>Min Brand Fit: {filters.minBrandFit}</label>
            <input
              type="range"
              min="1"
              max="10"
              value={filters.minBrandFit}
              onChange={e => setFilters({ ...filters, minBrandFit: Number(e.target.value) })}
              className="w-full"
              style={{ accentColor: 'var(--accent)' }}
            />
          </div>
        </div>

        <button onClick={handleEnrich} className="btn-primary">
          ⚡ Enrich Profiles
        </button>
      </div>

      {/* Table */}
      <div className="card overflow-hidden" style={{ padding: 0 }}>
        <table className="w-full">
          <thead>
            <tr style={{ backgroundColor: 'var(--bg-hover)' }}>
              {['#', 'Name', 'Platform', 'Followers', 'Engagement', 'Niche', 'City', 'Brand Fit', 'Priority'].map(h => (
                <th key={h} className="px-4 py-3 text-left text-sm" style={{ color: 'var(--text-secondary)' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {displayData.slice(0, 20).map((inf, i) => (
              <tr key={inf.id || i} className="border-t" style={{ borderColor: 'var(--border)' }}>
                <td className="px-4 py-3" style={{ color: 'var(--text-secondary)' }}>{i + 1}</td>
                <td className="px-4 py-3">
                  <p className="font-medium" style={{ color: 'var(--text-primary)' }}>{inf.name}</p>
                  <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{inf.handle}</p>
                </td>
                <td className="px-4 py-3">
                  <span className="badge" style={{ backgroundColor: 'rgba(239,68,68,0.15)', color: '#ef4444' }}>{inf.platform}</span>
                </td>
                <td className="px-4 py-3" style={{ color: 'var(--text-primary)' }}>{formatFollowers(inf.followers)}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-16 h-2 rounded" style={{ backgroundColor: 'var(--bg-hover)' }}>
                      <div className="h-2 rounded" style={{ width: `${(inf.engagement_rate / 8) * 100}%`, backgroundColor: getEngagementColor(inf.engagement_rate) }} />
                    </div>
                    <span className="text-sm" style={{ color: 'var(--text-primary)' }}>{inf.engagement_rate}%</span>
                  </div>
                </td>
                <td className="px-4 py-3">
                  <span className={`badge ${getNicheBadge(inf.niche)}`}>{inf.niche}</span>
                </td>
                <td className="px-4 py-3" style={{ color: 'var(--text-primary)' }}>{inf.city}</td>
                <td className="px-4 py-3" style={{ color: 'var(--text-primary)' }}>{inf.brand_fit_score}</td>
                <td className="px-4 py-3">
                  <span className={`badge ${getPriorityBadge(inf.outreach_priority)}`}>{inf.outreach_priority || 'N/A'}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedProfile && (
        <ProfileCard influencer={selectedProfile} onClose={() => setSelectedProfile(null)} />
      )}
    </div>
  )
}