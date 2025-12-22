import { Link, Outlet, useLocation } from 'react-router-dom'
import {
  Sparkles,
  TrendingUp,
  Layers,
  Shield,
  FileText,
  Download,
  Zap,
  Lock,
} from 'lucide-react'

const navigation = [
  { name: 'Generate Ideas', href: '/', icon: Sparkles },
  { name: 'Trending', href: '/phrases', icon: TrendingUp },
  { name: 'Patterns', href: '/patterns', icon: Layers },
  { name: 'Trademark Check', href: '/trademarks', icon: Shield },
  { name: 'SEO Generator', href: '/seo', icon: FileText },
  { name: 'Data Sources', href: '/scraping', icon: Zap },
  { name: 'Export', href: '/export', icon: Download },
]

export default function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen flex bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-6 border-b border-gray-100">
          <h1 className="text-lg font-semibold text-gray-900">Merch Trend Engine</h1>
          <p className="text-gray-500 text-xs mt-1">Phrase Intelligence Tool</p>
        </div>

        <nav className="flex-1 p-3">
          <ul className="space-y-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href ||
                (item.href !== '/' && location.pathname.startsWith(item.href))
              const Icon = item.icon

              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-gray-900 text-white'
                        : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                    }`}
                  >
                    <Icon size={18} strokeWidth={2} />
                    <span>{item.name}</span>
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>

        <div className="p-4 border-t border-gray-100">
          <div className="flex items-center gap-2 text-xs text-gray-400">
            <Lock size={12} />
            <span>Local-only / Private</span>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto p-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
