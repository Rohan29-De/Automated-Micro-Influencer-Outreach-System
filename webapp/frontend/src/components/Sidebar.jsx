import { Search, BarChart3, Users, MessageSquare, Settings } from 'lucide-react'

const menuItems = [
  { id: 1, name: 'Discovery', icon: Search },
  { id: 2, name: 'Enrichment', icon: BarChart3 },
  { id: 3, name: 'Segments', icon: Users },
  { id: 4, name: 'Messages', icon: MessageSquare },
]

export default function Sidebar({ currentStep, onStepClick }) {
  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-gray-900 text-white p-4">
      <div className="flex items-center gap-2 mb-8 pt-4">
        <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
          <Users className="w-6 h-6" />
        </div>
        <div>
          <h2 className="font-bold">Outreach</h2>
          <p className="text-xs text-gray-400">System</p>
        </div>
      </div>

      <nav className="space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = currentStep === item.id
          return (
            <button
              key={item.id}
              onClick={() => onStepClick(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                isActive
                  ? 'bg-purple-600 text-white'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span>{item.name}</span>
            </button>
          )
        })}
      </nav>

      <div className="absolute bottom-4 left-4 right-4">
        <button className="w-full flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white transition-colors">
          <Settings className="w-5 h-5" />
          <span>Settings</span>
        </button>
      </div>
    </aside>
  )
}