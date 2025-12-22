import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getPatterns, getPopularPatterns, getPatternPhrases } from '../api/client'
import Loading from '../components/Loading'
import EmptyState from '../components/EmptyState'

export default function Patterns() {
  const [selectedPattern, setSelectedPattern] = useState(null)

  const { data: patterns, isLoading } = useQuery({
    queryKey: ['patterns'],
    queryFn: () => getPatterns(50),
  })

  const { data: popular } = useQuery({
    queryKey: ['popularPatterns'],
    queryFn: () => getPopularPatterns(10),
  })

  const { data: patternPhrases, isLoading: phrasesLoading } = useQuery({
    queryKey: ['patternPhrases', selectedPattern?.id],
    queryFn: () => getPatternPhrases(selectedPattern.id, 20),
    enabled: !!selectedPattern,
  })

  if (isLoading) return <Loading />

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Phrase Patterns</h1>
        <p className="text-gray-500 mt-1">Reusable phrase frameworks and templates</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Pattern List */}
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold mb-4">Detected Patterns</h2>

          {patterns?.length > 0 ? (
            <div className="space-y-4">
              {patterns.map((pattern) => (
                <div
                  key={pattern.id}
                  className={`card cursor-pointer transition-all ${
                    selectedPattern?.id === pattern.id
                      ? 'ring-2 ring-primary-500 bg-primary-50'
                      : 'hover:shadow-md'
                  }`}
                  onClick={() => setSelectedPattern(pattern)}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-mono text-lg font-medium text-primary-700">
                        {pattern.template}
                      </h3>
                      {pattern.description && (
                        <p className="text-gray-600 mt-1">{pattern.description}</p>
                      )}
                      <div className="flex gap-2 mt-3">
                        <span className="badge bg-purple-100 text-purple-700">
                          {pattern.variable_count} variable{pattern.variable_count > 1 ? 's' : ''}
                        </span>
                        <span className="badge bg-gray-100 text-gray-700">
                          {pattern.usage_count} uses
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-primary-600">
                        {pattern.popularity_score?.toFixed(0) || 0}
                      </div>
                      <div className="text-xs text-gray-500">Popularity</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState
              icon="🧩"
              title="No patterns detected"
              description="Patterns are automatically detected when analyzing phrases. Start scraping to discover patterns."
            />
          )}
        </div>

        {/* Pattern Details / Popular Patterns */}
        <div>
          {selectedPattern ? (
            <div className="card sticky top-8">
              <h2 className="text-lg font-semibold mb-4">Pattern Details</h2>

              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-700">Template</label>
                  <p className="font-mono text-primary-700 mt-1">{selectedPattern.template}</p>
                </div>

                {selectedPattern.description && (
                  <div>
                    <label className="text-sm font-medium text-gray-700">Description</label>
                    <p className="text-gray-600 mt-1">{selectedPattern.description}</p>
                  </div>
                )}

                <div>
                  <label className="text-sm font-medium text-gray-700">Matching Phrases</label>
                  {phrasesLoading ? (
                    <Loading text="Loading phrases..." />
                  ) : patternPhrases?.phrases?.length > 0 ? (
                    <ul className="mt-2 space-y-2">
                      {patternPhrases.phrases.map((p) => (
                        <li key={p.id} className="p-2 bg-gray-50 rounded text-sm">
                          "{p.text}"
                          <span className="text-gray-500 ml-2">({p.trend_score?.toFixed(0)})</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-gray-500 mt-2">No matching phrases found</p>
                  )}
                </div>

                <button
                  className="btn btn-secondary w-full"
                  onClick={() => setSelectedPattern(null)}
                >
                  Close
                </button>
              </div>
            </div>
          ) : (
            <>
              <h2 className="text-xl font-semibold mb-4">Popular Patterns</h2>
              <div className="card">
                {popular?.length > 0 ? (
                  <ul className="divide-y divide-gray-100">
                    {popular.map((pattern, idx) => (
                      <li
                        key={pattern.id}
                        className="py-3 first:pt-0 last:pb-0 cursor-pointer hover:bg-gray-50 -mx-2 px-2 rounded"
                        onClick={() => setSelectedPattern(pattern)}
                      >
                        <div className="flex items-center gap-3">
                          <span className="text-lg font-bold text-gray-400">#{idx + 1}</span>
                          <div className="flex-1">
                            <p className="font-mono text-sm text-primary-700">{pattern.template}</p>
                            <p className="text-xs text-gray-500 mt-1">{pattern.usage_count} uses</p>
                          </div>
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-500 text-center">No popular patterns yet</p>
                )}
              </div>

              {/* Pattern Examples */}
              <h2 className="text-xl font-semibold mb-4 mt-8">Common Templates</h2>
              <div className="card">
                <ul className="space-y-3 text-sm">
                  <li className="font-mono text-primary-700">I'm not {'{WORD}'}, I'm {'{WORD}'}</li>
                  <li className="font-mono text-primary-700">Powered by {'{PHRASE}'}</li>
                  <li className="font-mono text-primary-700">{'{WORD}'} is my cardio</li>
                  <li className="font-mono text-primary-700">{'{WORD}'} mode activated</li>
                  <li className="font-mono text-primary-700">Professional {'{WORD}'}</li>
                  <li className="font-mono text-primary-700">{'{WORD}'} whisperer</li>
                </ul>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
