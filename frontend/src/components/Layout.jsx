import { Link, Outlet, useLocation } from 'react-router-dom'
import {
  Sparkles,
  Shield,
  FileText,
  TrendingUp,
  Zap,
  Wrench,
} from 'lucide-react'

const navigation = [
  { name: 'Idea Generator', href: '/', icon: Sparkles, color: 'text-emerald-400' },
  { name: 'Advanced Tools', href: '/tools', icon: Wrench, color: 'text-purple-400' },
  { name: 'Trademark Check', href: '/trademarks', icon: Shield, color: 'text-amber-400' },
  { name: 'SEO Builder', href: '/seo', icon: FileText, color: 'text-blue-400' },
]

export default function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen flex bg-zinc-950">
      {/* Sidebar */}
      <aside className="w-56 bg-zinc-900/50 border-r border-zinc-800 flex flex-col">
        {/* Logo */}
        <div className="p-5 border-b border-zinc-800">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-lg flex items-center justify-center">
              <Zap size={18} className="text-white" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-zinc-100">MerchEngine</h1>
              <p className="text-[10px] text-zinc-500 uppercase tracking-wider">Pro Research</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-3">
          <ul className="space-y-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              const Icon = item.icon

              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-zinc-800 text-zinc-100'
                        : 'text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-200'
                    }`}
                  >
                    <Icon size={18} className={isActive ? item.color : ''} />
                    <span>{item.name}</span>
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-zinc-800">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
            <span className="text-xs text-zinc-500">Local Mode</span>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto p-6">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
