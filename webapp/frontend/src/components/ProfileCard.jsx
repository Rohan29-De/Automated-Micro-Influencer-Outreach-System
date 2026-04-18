import { MapPin, Users, MessageSquare, Globe } from 'lucide-react'

export default function ProfileCard({ influencer, onClose }) {
  if (!influencer) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-2xl p-6 max-w-md w-full mx-4" onClick={(e) => e.stopPropagation()}>
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-xl font-bold">{influencer.name}</h3>
            <p className="text-gray-500">{influencer.handle}</p>
          </div>
          <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
            {influencer.niche}
          </span>
        </div>

        <div className="space-y-3">
          <div className="flex items-center gap-3 text-gray-600">
            <Users className="w-5 h-5" />
            <span>{influencer.followers?.toLocaleString()} followers</span>
          </div>
          <div className="flex items-center gap-3 text-gray-600">
            <MapPin className="w-5 h-5" />
            <span>{influencer.city}</span>
          </div>
          <div className="flex items-center gap-3 text-gray-600">
            <Globe className="w-5 h-5" />
            <span>{influencer.language}</span>
          </div>
          <div className="flex items-center gap-3 text-gray-600">
            <MessageSquare className="w-5 h-5" />
            <span>{influencer.contact_email}</span>
          </div>
        </div>

        {influencer.content_themes && (
          <div className="mt-4">
            <p className="text-sm font-medium text-gray-700 mb-2">Content Themes</p>
            <div className="flex flex-wrap gap-2">
              {influencer.content_themes.map((theme, i) => (
                <span key={i} className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-sm">
                  {theme}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="mt-6 flex gap-3">
          <a
            href={influencer.profile_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 bg-purple-600 text-white text-center py-2 rounded-lg hover:bg-purple-700"
          >
            View Profile
          </a>
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