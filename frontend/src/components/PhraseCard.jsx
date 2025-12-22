import { Link } from 'react-router-dom'

export default function PhraseCard({ phrase, showDetails = true }) {
  const getTrendBadge = (score) => {
    if (score >= 80) return { text: 'Hot', class: 'badge-danger' }
    if (score >= 60) return { text: 'Rising', class: 'badge-warning' }
    if (score >= 40) return { text: 'Stable', class: 'badge-info' }
    return { text: 'Low', class: 'badge-success' }
  }

  const getRiskBadge = (score, isSafe) => {
    if (!isSafe) return { text: 'Unsafe', class: 'badge-danger' }
    if (score >= 50) return { text: 'Caution', class: 'badge-warning' }
    return { text: 'Safe', class: 'badge-success' }
  }

  const trendBadge = getTrendBadge(phrase.trend_score)
  const riskBadge = getRiskBadge(phrase.risk_score, phrase.is_safe)

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <Link
            to={`/phrases/${phrase.id}`}
            className="text-lg font-medium text-gray-900 hover:text-primary-600"
          >
            "{phrase.text}"
          </Link>

          {showDetails && (
            <div className="mt-2 flex flex-wrap gap-2">
              <span className={`badge ${trendBadge.class}`}>
                {trendBadge.text} ({phrase.trend_score.toFixed(0)})
              </span>
              <span className={`badge ${riskBadge.class}`}>
                {riskBadge.text}
              </span>
              {phrase.niche && (
                <span className="badge bg-gray-100 text-gray-700">
                  {phrase.niche}
                </span>
              )}
              {phrase.is_pattern && (
                <span className="badge bg-purple-100 text-purple-700">
                  Pattern
                </span>
              )}
            </div>
          )}

          {showDetails && (
            <div className="mt-3 text-sm text-gray-500 flex gap-4">
              <span>Frequency: {phrase.frequency}</span>
              <span>{phrase.word_count} words</span>
              <span>First seen: {new Date(phrase.first_seen).toLocaleDateString()}</span>
            </div>
          )}
        </div>

        <div className="text-right">
          <div className="text-2xl font-bold text-primary-600">
            {phrase.trend_score.toFixed(0)}
          </div>
          <div className="text-xs text-gray-500">Trend Score</div>
        </div>
      </div>
    </div>
  )
}
