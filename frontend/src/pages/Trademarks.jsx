import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getTrademarks, checkTrademark, getBlockedTerms, addBlockedTerm } from '../api/client'
import Loading from '../components/Loading'

export default function Trademarks() {
  const [searchTerm, setSearchTerm] = useState('')
  const [checkPhrase, setCheckPhrase] = useState('')
  const [checkResult, setCheckResult] = useState(null)
  const [checking, setChecking] = useState(false)
  const [newBlockedTerm, setNewBlockedTerm] = useState('')
  const [blockReason, setBlockReason] = useState('manual')

  const queryClient = useQueryClient()

  const { data: trademarks, isLoading } = useQuery({
    queryKey: ['trademarks', searchTerm],
    queryFn: () => getTrademarks({ search: searchTerm, page_size: 100 }),
  })

  const { data: blockedTerms } = useQuery({
    queryKey: ['blockedTerms'],
    queryFn: getBlockedTerms,
  })

  const addBlockMutation = useMutation({
    mutationFn: ({ term, reason }) => addBlockedTerm(term, reason),
    onSuccess: () => {
      queryClient.invalidateQueries(['blockedTerms'])
      setNewBlockedTerm('')
    },
  })

  const handleCheck = async () => {
    if (!checkPhrase.trim()) return
    setChecking(true)
    try {
      const result = await checkTrademark(checkPhrase)
      setCheckResult(result)
    } catch (error) {
      console.error('Check failed:', error)
    }
    setChecking(false)
  }

  const handleAddBlocked = () => {
    if (!newBlockedTerm.trim()) return
    addBlockMutation.mutate({ term: newBlockedTerm, reason: blockReason })
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Trademark Safety</h1>
        <p className="text-gray-500 mt-1">Check phrases for trademark conflicts and manage blocklists</p>
      </div>

      {/* Safety Checker */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Check Phrase Safety</h2>
        <div className="flex gap-4">
          <input
            type="text"
            className="input flex-1"
            placeholder="Enter a phrase to check for trademark conflicts..."
            value={checkPhrase}
            onChange={(e) => setCheckPhrase(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleCheck()}
          />
          <button
            className="btn btn-primary"
            onClick={handleCheck}
            disabled={checking}
          >
            {checking ? 'Checking...' : 'Check Safety'}
          </button>
        </div>

        {checkResult && (
          <div className={`mt-4 p-4 rounded-lg ${
            checkResult.is_safe ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-lg">
                {checkResult.is_safe ? '✅ Safe to Use' : '⚠️ Risk Detected'}
              </h3>
              <span className={`text-2xl font-bold ${
                checkResult.is_safe ? 'text-green-600' : 'text-red-600'
              }`}>
                Risk: {checkResult.risk_score.toFixed(0)}%
              </span>
            </div>

            {checkResult.matches?.length > 0 && (
              <div className="mt-3">
                <p className="font-medium text-red-800 mb-2">Matches Found:</p>
                <ul className="list-disc list-inside text-red-700">
                  {checkResult.matches.map((match, idx) => (
                    <li key={idx}>
                      "{match.term}" - {match.type} ({match.match_type}, score: {match.score})
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {checkResult.warnings?.length > 0 && (
              <div className="mt-3">
                <p className="font-medium text-yellow-800 mb-2">Warnings:</p>
                <ul className="list-disc list-inside text-yellow-700">
                  {checkResult.warnings.map((warning, idx) => (
                    <li key={idx}>{warning}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Trademark Database */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Trademark Database</h2>
          <div className="card">
            <div className="mb-4">
              <input
                type="text"
                className="input"
                placeholder="Search trademarks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            {isLoading ? (
              <Loading text="Loading trademarks..." />
            ) : trademarks?.length > 0 ? (
              <div className="max-h-96 overflow-y-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50 sticky top-0">
                    <tr>
                      <th className="text-left p-2">Term</th>
                      <th className="text-left p-2">Source</th>
                      <th className="text-left p-2">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {trademarks.map((tm) => (
                      <tr key={tm.id} className="hover:bg-gray-50">
                        <td className="p-2 font-medium">{tm.term}</td>
                        <td className="p-2 text-gray-500">{tm.source}</td>
                        <td className="p-2">
                          <span className={`badge ${
                            tm.status === 'LIVE' ? 'badge-success' : 'badge-info'
                          }`}>
                            {tm.status || 'Unknown'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">
                {searchTerm ? 'No trademarks found' : 'No trademarks in database. Import a USPTO CSV file.'}
              </p>
            )}
          </div>
        </div>

        {/* Blocked Terms */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Blocked Terms</h2>
          <div className="card">
            <div className="mb-4 space-y-3">
              <input
                type="text"
                className="input"
                placeholder="Add term to blocklist..."
                value={newBlockedTerm}
                onChange={(e) => setNewBlockedTerm(e.target.value)}
              />
              <div className="flex gap-2">
                <select
                  className="input flex-1"
                  value={blockReason}
                  onChange={(e) => setBlockReason(e.target.value)}
                >
                  <option value="manual">Manual Block</option>
                  <option value="trademark">Trademark</option>
                  <option value="brand">Brand Name</option>
                  <option value="offensive">Offensive</option>
                  <option value="policy">Policy Violation</option>
                </select>
                <button
                  className="btn btn-danger"
                  onClick={handleAddBlocked}
                  disabled={addBlockMutation.isPending}
                >
                  Block
                </button>
              </div>
            </div>

            {blockedTerms?.length > 0 ? (
              <ul className="divide-y divide-gray-100">
                {blockedTerms.map((term) => (
                  <li key={term.id} className="py-2 flex items-center justify-between">
                    <div>
                      <span className="font-medium">{term.term}</span>
                      <span className="text-gray-500 text-sm ml-2">({term.reason})</span>
                    </div>
                    <span className="badge badge-danger">Blocked</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-center py-4">No blocked terms</p>
            )}
          </div>

          {/* Info Box */}
          <div className="card mt-4 bg-blue-50 border-blue-200">
            <h3 className="font-medium text-blue-800 mb-2">About Trademark Checking</h3>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Exact matches are automatically blocked</li>
              <li>• Fuzzy matches (≥85% similar) are flagged</li>
              <li>• Known brand names are blocked</li>
              <li>• Risk triggers like "parody of" increase risk score</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
