import { useState } from 'react'
import { Play, Loader2 } from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'

export default function Dashboard({ onInfluencersFound }) {
  const [loading, setLoading] = useState(false)
  const [niche, setNiche] = useState('Beauty')
  const [platform, setPlatform] = useState('YouTube')
  const [targetCount, setTargetCount] = useState(50)

  const niches = ['Beauty', 'Fashion', 'Fitness', 'Finance', 'Lifestyle', 'Education']
  const platforms = ['YouTube', 'Instagram', 'Both']

  const handleDiscover = async () => {
    setLoading(true)
    try {
      const response = await axios.post('/api/discover', {
        niche,
        platform,
        target_count: targetCount,
        country: 'India'
      })
      onInfluencersFound(response.data)
      toast.success(`Found ${response.data.length} influencers!`)
    } catch (error) {
      toast.error('Discovery failed. Using cached data.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border">
      <div className="grid grid-cols-3 gap-6 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Niche</label>
          <select
            value={niche}
            onChange={(e) => setNiche(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            {niches.map((n) => (
              <option key={n} value={n}>{n}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Platform</label>
          <select
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            {platforms.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Target Count</label>
          <input
            type="number"
            value={targetCount}
            onChange={(e) => setTargetCount(Number(e.target.value))}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
        </div>
      </div>

      <button
        onClick={handleDiscover}
        disabled={loading}
        className="flex items-center gap-2 bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors"
      >
        {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Play className="w-5 h-5" />}
        <span>{loading ? 'Discovering...' : 'Start Discovery'}</span>
      </button>
    </div>
  )
}