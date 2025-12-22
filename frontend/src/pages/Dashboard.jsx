import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { getStats, getTrendingPhrases, getActivity } from '../api/client'
import StatsCard from '../components/StatsCard'
import PhraseCard from '../components/PhraseCard'
import Loading from '../components/Loading'
import EmptyState from '../components/EmptyState'

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['stats'],
    queryFn: getStats,
  })

  const { data: trending, isLoading: trendingLoading } = useQuery({
    queryKey: ['trending', 10],
    queryFn: () => getTrendingPhrases(10),
  })

  const { data: activity, isLoading: activityLoading } = useQuery({
    queryKey: ['activity'],
    queryFn: () => getActivity(10),
  })

  if (statsLoading) return <Loading />

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">Overview of trending phrases and patterns</p>
        </div>
        <Link to="/scraping" className="btn btn-primary">
          Start Scraping
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Phrases"
          value={stats?.total_phrases || 0}
          icon="📝"
        />
        <StatsCard
          title="Safe Phrases"
          value={stats?.safe_phrases || 0}
          icon="✅"
        />
        <StatsCard
          title="Trending Now"
          value={stats?.trending_phrases || 0}
          icon="🔥"
        />
        <StatsCard
          title="Patterns Detected"
          value={stats?.patterns_detected || 0}
          icon="🧩"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Trending Phrases */}
        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Top Trending Phrases</h2>
            <Link to="/phrases" className="text-primary-600 hover:text-primary-700 text-sm">
              View all →
            </Link>
          </div>

          {trendingLoading ? (
            <Loading text="Loading trends..." />
          ) : trending?.length > 0 ? (
            <div className="space-y-4">
              {trending.map((phrase) => (
                <PhraseCard key={phrase.id} phrase={phrase} />
              ))}
            </div>
          ) : (
            <EmptyState
              icon="📊"
              title="No trending phrases yet"
              description="Start scraping data sources to discover trending phrases."
              action={
                <Link to="/scraping" className="btn btn-primary">
                  Start Scraping
                </Link>
              }
            />
          )}
        </div>

        {/* Recent Activity */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
          <div className="card">
            {activityLoading ? (
              <Loading text="Loading activity..." />
            ) : activity?.length > 0 ? (
              <ul className="divide-y divide-gray-100">
                {activity.map((item) => (
                  <li key={item.id} className="py-3 first:pt-0 last:pb-0">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-sm">{item.source}</p>
                        <p className="text-xs text-gray-500">
                          {item.phrases_extracted} phrases extracted
                        </p>
                      </div>
                      <span className={`badge ${
                        item.status === 'completed' ? 'badge-success' :
                        item.status === 'failed' ? 'badge-danger' :
                        'badge-warning'
                      }`}>
                        {item.status}
                      </span>
                    </div>
                    <p className="text-xs text-gray-400 mt-1">
                      {new Date(item.started_at).toLocaleString()}
                    </p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-center py-4">No recent activity</p>
            )}
          </div>

          {/* Top Niches */}
          {stats?.top_niches?.length > 0 && (
            <>
              <h2 className="text-xl font-semibold mb-4 mt-8">Top Niches</h2>
              <div className="card">
                <ul className="divide-y divide-gray-100">
                  {stats.top_niches.map((item, idx) => (
                    <li key={item.niche} className="py-3 first:pt-0 last:pb-0 flex items-center justify-between">
                      <span className="font-medium">{item.niche}</span>
                      <span className="text-gray-500">{item.count} phrases</span>
                    </li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
