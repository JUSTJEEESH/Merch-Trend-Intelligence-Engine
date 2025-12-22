import { Link, Outlet, useLocation } from 'react-router-dom'

const navigation = [
  { name: 'Dashboard', href: '/', icon: '📊' },
  { name: 'Trending Phrases', href: '/phrases', icon: '🔥' },
  { name: 'Patterns', href: '/patterns', icon: '🧩' },
  { name: 'Trademarks', href: '/trademarks', icon: '🛡️' },
  { name: 'SEO Generator', href: '/seo', icon: '✍️' },
  { name: 'Scraping', href: '/scraping', icon: '🕷️' },
  { name: 'Export', href: '/export', icon: '📤' },
]

export default function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900 text-white flex flex-col">
        <div className="p-6 border-b border-gray-800">
          <h1 className="text-xl font-bold">Merch Trend Engine</h1>
          <p className="text-gray-400 text-sm mt-1">Phrase Intelligence Tool</p>
        </div>

        <nav className="flex-1 p-4">
          <ul className="space-y-1">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href ||
                (item.href !== '/' && location.pathname.startsWith(item.href))

              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-primary-600 text-white'
                        : 'text-gray-300 hover:bg-gray-800'
                    }`}
                  >
                    <span>{item.icon}</span>
                    <span>{item.name}</span>
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>

        <div className="p-4 border-t border-gray-800">
          <div className="text-xs text-gray-500">
            <p>Local-only • 100% Private</p>
            <p className="mt-1">No data leaves your machine</p>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
