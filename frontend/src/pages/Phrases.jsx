import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getPhrases, getNiches, analyzePhrase } from '../api/client'
import PhraseCard from '../components/PhraseCard'
import Loading from '../components/Loading'
import EmptyState from '../components/EmptyState'

export default function Phrases() {
  const [filters, setFilters] = useState({
    page: 1,
    page_size: 20,
    is_safe: true,
    sort_by: 'trend_score',
    sort_order: 'desc',
    niche: '',
    min_trend_score: '',
  })

  const [analyzeText, setAnalyzeText] = useState('')
  const [analyzeResult, setAnalyzeResult] = useState(null)
  const [analyzing, setAnalyzing] = useState(false)

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['phrases', filters],
    queryFn: () => getPhrases(filters),
  })

  const { data: niches } = useQuery({
    queryKey: ['niches'],
    queryFn: getNiches,
  })

  const handleAnalyze = async () => {
    if (!analyzeText.trim()) return
    setAnalyzing(true)
    try {
      const result = await analyzePhrase(analyzeText)
      setAnalyzeResult(result)
    } catch (error) {
      console.error('Analysis failed:', error)
    }
    setAnalyzing(false)
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value, page: 1 }))
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Trending Phrases</h1>
        <p className="text-gray-500 mt-1">Browse and analyze safe, trending phrases</p>
      </div>

      {/* Phrase Analyzer */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Analyze a Phrase</h2>
        <div className="flex gap-4">
          <input
            type="text"
            className="input flex-1"
            placeholder="Enter a phrase to analyze..."
            value={analyzeText}
            onChange={(e) => setAnalyzeText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
          />
          <button
            className="btn btn-primary"
            onClick={handleAnalyze}
            disabled={analyzing}
          >
            {analyzing ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>

        {analyzeResult && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-500">Trend Score</p>
                <p className="text-2xl font-bold text-primary-600">
                  {analyzeResult.trend_score?.toFixed(0) || 'N/A'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Risk Score</p>
                <p className={`text-2xl font-bold ${
                  analyzeResult.is_safe ? 'text-green-600' : 'text-red-600'
                }`}>
                  {analyzeResult.risk_score?.toFixed(0)}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Status</p>
                <span className={`badge ${analyzeResult.is_safe ? 'badge-success' : 'badge-danger'}`}>
                  {analyzeResult.is_safe ? 'Safe' : 'Risky'}
                </span>
              </div>
              <div>
                <p className="text-sm text-gray-500">Word Count</p>
                <p className="text-2xl font-bold">{analyzeResult.word_count}</p>
              </div>
            </div>
            {analyzeResult.pattern && (
              <div className="mt-4">
                <p className="text-sm text-gray-500">Pattern Detected</p>
                <p className="font-medium text-purple-600">{analyzeResult.pattern}</p>
              </div>
            )}
            {analyzeResult.risk_details?.length > 0 && (
              <div className="mt-4">
                <p className="text-sm text-gray-500 mb-2">Risk Details</p>
                <ul className="list-disc list-inside text-sm text-red-600">
                  {analyzeResult.risk_details.map((detail, idx) => (
                    <li key={idx}>{detail.term} ({detail.type})</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-wrap gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Niche</label>
            <select
              className="input w-40"
              value={filters.niche}
              onChange={(e) => handleFilterChange('niche', e.target.value)}
            >
              <option value="">All Niches</option>
              {niches?.map((n) => (
                <option key={n.niche} value={n.niche}>{n.niche} ({n.count})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Min Score</label>
            <input
              type="number"
              className="input w-24"
              placeholder="0"
              min="0"
              max="100"
              value={filters.min_trend_score}
              onChange={(e) => handleFilterChange('min_trend_score', e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
            <select
              className="input w-40"
              value={filters.sort_by}
              onChange={(e) => handleFilterChange('sort_by', e.target.value)}
            >
              <option value="trend_score">Trend Score</option>
              <option value="frequency">Frequency</option>
              <option value="first_seen">First Seen</option>
              <option value="risk_score">Risk Score</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Safety</label>
            <select
              className="input w-32"
              value={filters.is_safe === true ? 'safe' : filters.is_safe === false ? 'unsafe' : 'all'}
              onChange={(e) => handleFilterChange('is_safe',
                e.target.value === 'safe' ? true :
                e.target.value === 'unsafe' ? false : null
              )}
            >
              <option value="safe">Safe Only</option>
              <option value="unsafe">Unsafe Only</option>
              <option value="all">All</option>
            </select>
          </div>
        </div>
      </div>

      {/* Phrases List */}
      {isLoading ? (
        <Loading />
      ) : data?.phrases?.length > 0 ? (
        <>
          <div className="space-y-4">
            {data.phrases.map((phrase) => (
              <PhraseCard key={phrase.id} phrase={phrase} />
            ))}
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-500">
              Showing {((filters.page - 1) * filters.page_size) + 1} to{' '}
              {Math.min(filters.page * filters.page_size, data.total)} of {data.total}
            </p>
            <div className="flex gap-2">
              <button
                className="btn btn-secondary"
                disabled={filters.page === 1}
                onClick={() => setFilters(prev => ({ ...prev, page: prev.page - 1 }))}
              >
                Previous
              </button>
              <button
                className="btn btn-secondary"
                disabled={filters.page * filters.page_size >= data.total}
                onClick={() => setFilters(prev => ({ ...prev, page: prev.page + 1 }))}
              >
                Next
              </button>
            </div>
          </div>
        </>
      ) : (
        <EmptyState
          icon="🔍"
          title="No phrases found"
          description="Try adjusting your filters or start scraping to collect new phrases."
        />
      )}
    </div>
  )
}
