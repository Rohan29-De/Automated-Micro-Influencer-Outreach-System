import { Eye, Mail, Star } from 'lucide-react'

export default function InfluencerTable({ influencers, segments, onSelect }) {
  const allInfluencers = influencers.length > 0 ? influencers : Object.values(segments).flat()

  if (allInfluencers.length === 0) {
    return (
      <div className="bg-white rounded-xl p-12 shadow-sm border text-center">
        <p className="text-gray-500">No influencers found. Run discovery first.</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-50 border-b">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Platform</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Followers</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Engagement</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Niche</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Priority</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y">
          {allInfluencers.map((inf) => (
            <tr key={inf.id} className="hover:bg-gray-50">
              <td className="px-6 py-4">
                <div>
                  <p className="font-medium text-gray-900">{inf.name}</p>
                  <p className="text-sm text-gray-500">{inf.handle}</p>
                </div>
              </td>
              <td className="px-6 py-4">
                <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs">{inf.platform}</span>
              </td>
              <td className="px-6 py-4 text-gray-700">{inf.followers?.toLocaleString()}</td>
              <td className="px-6 py-4 text-gray-700">{inf.engagement_rate}%</td>
              <td className="px-6 py-4 text-gray-700">{inf.niche}</td>
              <td className="px-6 py-4">
                <span className={`px-2 py-1 rounded-full text-xs ${
                  inf.outreach_priority === 'High' ? 'bg-green-100 text-green-700' :
                  inf.outreach_priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {inf.outreach_priority || 'N/A'}
                </span>
              </td>
              <td className="px-6 py-4">
                <div className="flex gap-2">
                  <button
                    onClick={() => onSelect(inf)}
                    className="p-2 text-gray-400 hover:text-purple-600 transition-colors"
                    title="View Profile"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                  <button
                    className="p-2 text-gray-400 hover:text-purple-600 transition-colors"
                    title="Send Email"
                  >
                    <Mail className="w-4 h-4" />
                  </button>
                  <button
                    className="p-2 text-gray-400 hover:text-purple-600 transition-colors"
                    title="Brand Fit Score"
                  >
                    <Star className="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}