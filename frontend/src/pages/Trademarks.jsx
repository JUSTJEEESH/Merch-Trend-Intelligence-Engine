import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { checkTrademark, getBlockedTerms, addBlockedTerm } from '../api/client'
import {
  Shield,
  ShieldCheck,
  ShieldAlert,
  Loader2,
  Plus,
  Search,
  AlertTriangle,
  Info,
  X,
} from 'lucide-react'

export default function Trademarks() {
  const [checkPhrase, setCheckPhrase] = useState('')
  const [checkResult, setCheckResult] = useState(null)
  const [newBlockedTerm, setNewBlockedTerm] = useState('')
  const [blockReason, setBlockReason] = useState('manual')

  const queryClient = useQueryClient()

  const { data: blockedTerms } = useQuery({
    queryKey: ['blockedTerms'],
    queryFn: getBlockedTerms,
  })

  const checkMutation = useMutation({
    mutationFn: checkTrademark,
    onSuccess: (data) => setCheckResult(data),
  })

  const addBlockMutation = useMutation({
    mutationFn: ({ term, reason }) => addBlockedTerm(term, reason),
    onSuccess: () => {
      queryClient.invalidateQueries(['blockedTerms'])
      setNewBlockedTerm('')
    },
  })

  const handleCheck = () => {
    if (!checkPhrase.trim()) return
    checkMutation.mutate(checkPhrase)
  }

  const handleAddBlocked = () => {
    if (!newBlockedTerm.trim()) return
    addBlockMutation.mutate({ term: newBlockedTerm, reason: blockReason })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-zinc-100">Trademark Check</h1>
        <p className="text-zinc-500 text-sm mt-1">Verify phrase safety before uploading to Amazon</p>
      </div>

      {/* Safety Checker */}
      <div className="bg-zinc-900 rounded-xl border border-zinc-800 p-5">
        <div className="flex items-center gap-2 mb-4">
          <Shield size={18} className="text-amber-400" />
          <h2 className="text-base font-semibold text-zinc-200">Check Phrase Safety</h2>
        </div>

        <div className="flex gap-3">
          <div className="relative flex-1">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
            <input
              type="text"
              className="input pl-10"
              placeholder="Enter a phrase to check..."
              value={checkPhrase}
              onChange={(e) => setCheckPhrase(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleCheck()}
            />
          </div>
          <button
            className="btn btn-primary"
            onClick={handleCheck}
            disabled={checkMutation.isPending}
          >
            {checkMutation.isPending ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                <span>Checking...</span>
              </>
            ) : (
              'Check'
            )}
          </button>
        </div>

        {/* Result */}
        {checkResult && (
          <div className={`mt-4 p-4 rounded-xl border ${
            checkResult.is_safe
              ? 'bg-emerald-500/10 border-emerald-500/30'
              : 'bg-red-500/10 border-red-500/30'
          }`}>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                {checkResult.is_safe ? (
                  <ShieldCheck size={24} className="text-emerald-400" />
                ) : (
                  <ShieldAlert size={24} className="text-red-400" />
                )}
                <span className={`text-lg font-semibold ${
                  checkResult.is_safe ? 'text-emerald-400' : 'text-red-400'
                }`}>
                  {checkResult.is_safe ? 'Safe to Use' : 'Risk Detected'}
                </span>
              </div>
              <div className={`text-2xl font-bold ${
                checkResult.is_safe ? 'text-emerald-400' : 'text-red-400'
              }`}>
                {checkResult.risk_score.toFixed(0)}%
              </div>
            </div>

            {checkResult.matches?.length > 0 && (
              <div className="mt-3 space-y-2">
                <p className="text-sm font-medium text-red-400">Matches Found:</p>
                {checkResult.matches.map((match, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-sm text-red-300">
                    <AlertTriangle size={14} />
                    <span>"{match.term}" - {match.type} ({match.match_type})</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Blocked Terms */}
      <div className="bg-zinc-900 rounded-xl border border-zinc-800 p-5">
        <div className="flex items-center gap-2 mb-4">
          <X size={18} className="text-red-400" />
          <h2 className="text-base font-semibold text-zinc-200">Blocked Terms</h2>
        </div>

        <div className="flex gap-3 mb-4">
          <input
            type="text"
            className="input flex-1"
            placeholder="Add term to blocklist..."
            value={newBlockedTerm}
            onChange={(e) => setNewBlockedTerm(e.target.value)}
          />
          <select
            className="input w-40"
            value={blockReason}
            onChange={(e) => setBlockReason(e.target.value)}
          >
            <option value="manual">Manual</option>
            <option value="trademark">Trademark</option>
            <option value="brand">Brand</option>
            <option value="offensive">Offensive</option>
          </select>
          <button
            className="btn btn-danger"
            onClick={handleAddBlocked}
            disabled={addBlockMutation.isPending}
          >
            <Plus size={18} />
            <span>Block</span>
          </button>
        </div>

        {blockedTerms?.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {blockedTerms.map((term) => (
              <span
                key={term.id}
                className="px-3 py-1.5 bg-red-500/20 text-red-400 border border-red-500/30 rounded-lg text-sm"
              >
                {term.term}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-zinc-600 text-sm">No blocked terms</p>
        )}
      </div>

      {/* Info */}
      <div className="bg-zinc-900/50 rounded-xl border border-zinc-800 p-4">
        <div className="flex items-start gap-3">
          <Info size={18} className="text-blue-400 mt-0.5" />
          <div className="text-sm text-zinc-400">
            <p className="font-medium text-zinc-300 mb-2">How it works:</p>
            <ul className="space-y-1">
              <li>- Exact matches with known trademarks are blocked</li>
              <li>- Fuzzy matches (85%+ similar) are flagged as risky</li>
              <li>- Brand names and offensive terms are blocked</li>
              <li>- Add your own terms to the blocklist</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
