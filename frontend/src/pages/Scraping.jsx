import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getSources, getScrapingLogs, startScrape, scrapeReddit, scrapeGoogleTrends } from '../api/client'
import Loading from '../components/Loading'

export default function Scraping() {
  const [selectedSource, setSelectedSource] = useState('reddit')
  const [target, setTarget] = useState('')
  const [limit, setLimit] = useState(100)

  const queryClient = useQueryClient()

  const { data: sources } = useQuery({
    queryKey: ['sources'],
    queryFn: getSources,
  })

  const { data: logs, isLoading: logsLoading } = useQuery({
    queryKey: ['scrapingLogs'],
    queryFn: () => getScrapingLogs(20),
    refetchInterval: 5000, // Refresh every 5 seconds
  })

  const scrapeMutation = useMutation({
    mutationFn: (data) => startScrape(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['scrapingLogs'])
      queryClient.invalidateQueries(['sources'])
    },
  })

  const handleScrape = () => {
    scrapeMutation.mutate({
      source_type: selectedSource,
      target: target || undefined,
      limit,
    })
  }

  const quickScrapes = [
    { name: 'Reddit - Memes', action: () => scrapeReddit('memes', 100) },
    { name: 'Reddit - Funny', action: () => scrapeReddit('funny', 100) },
    { name: 'Google Trends', action: () => scrapeGoogleTrends() },
  ]

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Data Scraping</h1>
        <p className="text-gray-500 mt-1">Collect data from various sources to discover trending phrases</p>
      </div>

      {/* Quick Scrape */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Quick Scrape</h2>
        <div className="flex flex-wrap gap-3">
          {quickScrapes.map((qs) => (
            <button
              key={qs.name}
              className="btn btn-primary"
              onClick={async () => {
                await qs.action()
                queryClient.invalidateQueries(['scrapingLogs'])
              }}
            >
              {qs.name}
            </button>
          ))}
        </div>
      </div>

      {/* Custom Scrape */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Custom Scrape</h2>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Source</label>
            <select
              className="input"
              value={selectedSource}
              onChange={(e) => setSelectedSource(e.target.value)}
            >
              <option value="reddit">Reddit</option>
              <option value="google_trends">Google Trends</option>
              <option value="amazon">Amazon</option>
              <option value="etsy">Etsy</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Target {selectedSource === 'reddit' ? '(subreddit)' : '(search term)'}
            </label>
            <input
              type="text"
              className="input"
              placeholder={selectedSource === 'reddit' ? 'memes' : 'search term'}
              value={target}
              onChange={(e) => setTarget(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Limit</label>
            <input
              type="number"
              className="input"
              min="10"
              max="500"
              value={limit}
              onChange={(e) => setLimit(parseInt(e.target.value) || 100)}
            />
          </div>

          <div className="flex items-end">
            <button
              className="btn btn-primary w-full"
              onClick={handleScrape}
              disabled={scrapeMutation.isPending}
            >
              {scrapeMutation.isPending ? 'Starting...' : 'Start Scrape'}
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Scraping Logs */}
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>

          {logsLoading ? (
            <Loading />
          ) : logs?.length > 0 ? (
            <div className="card overflow-hidden p-0">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left p-4">Source</th>
                    <th className="text-left p-4">Status</th>
                    <th className="text-left p-4">Items</th>
                    <th className="text-left p-4">Phrases</th>
                    <th className="text-left p-4">Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {logs.map((log) => (
                    <tr key={log.id} className="hover:bg-gray-50">
                      <td className="p-4 font-medium">{log.source}</td>
                      <td className="p-4">
                        <span className={`badge ${
                          log.status === 'completed' ? 'badge-success' :
                          log.status === 'failed' ? 'badge-danger' :
                          log.status === 'running' ? 'badge-warning' :
                          'badge-info'
                        }`}>
                          {log.status}
                        </span>
                      </td>
                      <td className="p-4">{log.items_collected || 0}</td>
                      <td className="p-4">{log.phrases_extracted || 0}</td>
                      <td className="p-4 text-gray-500 text-sm">
                        {new Date(log.started_at).toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="card text-center py-8">
              <p className="text-gray-500">No scraping activity yet. Start a scrape to collect data.</p>
            </div>
          )}
        </div>

        {/* Sources */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Data Sources</h2>
          <div className="card">
            {sources?.length > 0 ? (
              <ul className="divide-y divide-gray-100">
                {sources.map((source) => (
                  <li key={source.id} className="py-3 first:pt-0 last:pb-0">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">{source.name}</p>
                        <p className="text-xs text-gray-500">
                          {source.last_scraped
                            ? `Last: ${new Date(source.last_scraped).toLocaleDateString()}`
                            : 'Never scraped'}
                        </p>
                      </div>
                      <span className={`badge ${source.is_active ? 'badge-success' : 'badge-info'}`}>
                        {source.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-center py-4">No sources configured</p>
            )}
          </div>

          {/* Info */}
          <div className="card mt-4 bg-blue-50 border-blue-200">
            <h3 className="font-medium text-blue-800 mb-2">Supported Sources</h3>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• <strong>Reddit</strong> - Subreddit posts and comments</li>
              <li>• <strong>Google Trends</strong> - Rising and trending queries</li>
              <li>• <strong>Amazon</strong> - Search suggestions and results</li>
              <li>• <strong>Etsy</strong> - Listing titles and trends</li>
            </ul>
          </div>

          <div className="card mt-4 bg-yellow-50 border-yellow-200">
            <h3 className="font-medium text-yellow-800 mb-2">API Setup Required</h3>
            <p className="text-sm text-yellow-700">
              Some sources require API credentials. Configure them in the backend .env file.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
