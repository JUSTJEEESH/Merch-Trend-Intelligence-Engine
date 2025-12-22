import { useState, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import { generateIdeas, generateVariations, checkTrademark } from '../api/client'
import {
  Sparkles,
  Loader2,
  Copy,
  Check,
  ChevronDown,
  TrendingUp,
  RefreshCw,
  Flame,
  Target,
  Shield,
  ShieldCheck,
  ShieldAlert,
  X,
  Wand2,
  Zap,
  Filter,
  Grid3X3,
  List,
  Star,
  Coffee,
  Dumbbell,
  Dog,
  Fish,
  Beer,
  Wine,
  Gamepad2,
  Heart,
  Baby,
  Stethoscope,
  GraduationCap,
  Mountain,
  Crosshair,
} from 'lucide-react'

const NICHES = [
  { id: 'all', name: 'All Niches', icon: Grid3X3 },
  { id: 'coffee', name: 'Coffee', icon: Coffee },
  { id: 'fitness', name: 'Fitness', icon: Dumbbell },
  { id: 'pets', name: 'Pets', icon: Dog },
  { id: 'fishing', name: 'Fishing', icon: Fish },
  { id: 'beer', name: 'Beer', icon: Beer },
  { id: 'wine', name: 'Wine', icon: Wine },
  { id: 'gaming', name: 'Gaming', icon: Gamepad2 },
  { id: 'parenting', name: 'Parenting', icon: Baby },
  { id: 'nursing', name: 'Nursing', icon: Stethoscope },
  { id: 'teaching', name: 'Teaching', icon: GraduationCap },
  { id: 'outdoors', name: 'Outdoors', icon: Mountain },
  { id: 'hunting', name: 'Hunting', icon: Crosshair },
]

export default function Dashboard() {
  const [ideas, setIdeas] = useState([])
  const [selectedNiche, setSelectedNiche] = useState('all')
  const [count, setCount] = useState(200)
  const [copiedId, setCopiedId] = useState(null)
  const [selectedPhrase, setSelectedPhrase] = useState(null)
  const [variations, setVariations] = useState([])
  const [trademarkStatus, setTrademarkStatus] = useState({})
  const [viewMode, setViewMode] = useState('grid')
  const [showNicheDropdown, setShowNicheDropdown] = useState(false)

  const generateMutation = useMutation({
    mutationFn: generateIdeas,
    onSuccess: (data) => {
      setIdeas(data.ideas || [])
      setTrademarkStatus({})
    },
  })

  const variationsMutation = useMutation({
    mutationFn: (phrase) => generateVariations({ phrase, count: 15 }),
    onSuccess: (data) => {
      setVariations(data.variations || [])
    },
  })

  const trademarkMutation = useMutation({
    mutationFn: checkTrademark,
    onSuccess: (data, variables) => {
      setTrademarkStatus(prev => ({
        ...prev,
        [variables]: data
      }))
    },
  })

  const handleGenerate = () => {
    const params = {
      count,
      creativity: 'high',
      include_classics: true,
      include_generated: true,
      include_variations: true,
    }
    if (selectedNiche !== 'all') {
      params.niches = selectedNiche
    }
    generateMutation.mutate(params)
  }

  const handleCopy = (phrase, id) => {
    navigator.clipboard.writeText(phrase)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 1500)
  }

  const handlePhraseClick = (phrase) => {
    setSelectedPhrase(phrase)
    setVariations([])
    variationsMutation.mutate(phrase)
    if (!trademarkStatus[phrase]) {
      trademarkMutation.mutate(phrase)
    }
  }

  const closeModal = () => {
    setSelectedPhrase(null)
    setVariations([])
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-emerald-400'
    if (score >= 60) return 'text-amber-400'
    return 'text-zinc-500'
  }

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Hot'
    if (score >= 60) return 'Good'
    return ''
  }

  const currentNiche = NICHES.find(n => n.id === selectedNiche)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-zinc-100">Idea Generator</h1>
          <p className="text-zinc-500 text-sm mt-1">
            Generate hundreds of winning merch phrases instantly
          </p>
        </div>
        {ideas.length > 0 && (
          <div className="text-sm text-zinc-500">
            <span className="text-emerald-400 font-semibold">{ideas.length}</span> ideas ready
          </div>
        )}
      </div>

      {/* Control Panel */}
      <div className="bg-zinc-900 rounded-xl border border-zinc-800 p-5">
        <div className="flex flex-wrap items-center gap-4">
          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={generateMutation.isPending}
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white rounded-xl font-semibold text-base transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-emerald-500/20"
          >
            {generateMutation.isPending ? (
              <>
                <Loader2 size={20} className="animate-spin" />
                <span>Generating...</span>
              </>
            ) : (
              <>
                <Zap size={20} />
                <span>Generate {count} Ideas</span>
              </>
            )}
          </button>

          {/* Niche Dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowNicheDropdown(!showNicheDropdown)}
              className="flex items-center gap-2 px-4 py-3 bg-zinc-800 border border-zinc-700 rounded-xl text-sm hover:bg-zinc-700 transition-all"
            >
              {currentNiche && <currentNiche.icon size={16} className="text-zinc-400" />}
              <span>{currentNiche?.name || 'All Niches'}</span>
              <ChevronDown size={16} className="text-zinc-500" />
            </button>

            {showNicheDropdown && (
              <div className="absolute top-full left-0 mt-2 w-48 bg-zinc-800 border border-zinc-700 rounded-xl shadow-xl z-50 py-2 max-h-80 overflow-y-auto">
                {NICHES.map((niche) => (
                  <button
                    key={niche.id}
                    onClick={() => {
                      setSelectedNiche(niche.id)
                      setShowNicheDropdown(false)
                    }}
                    className={`w-full flex items-center gap-3 px-4 py-2.5 text-sm hover:bg-zinc-700 transition-all ${
                      selectedNiche === niche.id ? 'text-emerald-400' : 'text-zinc-300'
                    }`}
                  >
                    <niche.icon size={16} />
                    <span>{niche.name}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Count Slider */}
          <div className="flex items-center gap-3 px-4 py-2 bg-zinc-800 border border-zinc-700 rounded-xl">
            <span className="text-sm text-zinc-400">Count:</span>
            <input
              type="range"
              min="50"
              max="500"
              step="50"
              value={count}
              onChange={(e) => setCount(parseInt(e.target.value))}
              className="w-24 accent-emerald-500"
            />
            <span className="text-sm font-medium text-zinc-200 w-8">{count}</span>
          </div>

          {/* View Toggle */}
          <div className="flex items-center bg-zinc-800 border border-zinc-700 rounded-xl p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded-lg transition-all ${
                viewMode === 'grid' ? 'bg-zinc-700 text-emerald-400' : 'text-zinc-500 hover:text-zinc-300'
              }`}
            >
              <Grid3X3 size={18} />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-lg transition-all ${
                viewMode === 'list' ? 'bg-zinc-700 text-emerald-400' : 'text-zinc-500 hover:text-zinc-300'
              }`}
            >
              <List size={18} />
            </button>
          </div>

          {/* Regenerate */}
          {ideas.length > 0 && (
            <button
              onClick={handleGenerate}
              disabled={generateMutation.isPending}
              className="flex items-center gap-2 px-3 py-2 text-zinc-400 hover:text-zinc-200 transition-all"
            >
              <RefreshCw size={16} />
              <span className="text-sm">Refresh</span>
            </button>
          )}
        </div>
      </div>

      {/* Loading State */}
      {generateMutation.isPending && (
        <div className="flex items-center justify-center py-20">
          <div className="text-center">
            <div className="w-16 h-16 bg-zinc-900 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-zinc-800">
              <Loader2 size={32} className="animate-spin text-emerald-400" />
            </div>
            <p className="text-zinc-400">Generating your ideas...</p>
          </div>
        </div>
      )}

      {/* Results */}
      {!generateMutation.isPending && ideas.length > 0 && (
        <>
          {viewMode === 'grid' ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
              {ideas.map((idea, idx) => (
                <div
                  key={idx}
                  onClick={() => handlePhraseClick(idea.phrase)}
                  className="group bg-zinc-900 rounded-xl border border-zinc-800 p-4 hover:border-zinc-700 hover:bg-zinc-800/50 transition-all cursor-pointer"
                >
                  <div className="flex items-start justify-between gap-2 mb-3">
                    <p className="text-sm font-medium text-zinc-200 leading-relaxed">
                      {idea.phrase}
                    </p>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleCopy(idea.phrase, idx)
                      }}
                      className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-zinc-700 rounded-lg transition-all shrink-0"
                    >
                      {copiedId === idx ? (
                        <Check size={14} className="text-emerald-400" />
                      ) : (
                        <Copy size={14} className="text-zinc-500" />
                      )}
                    </button>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs px-2 py-1 bg-zinc-800 text-zinc-400 rounded-lg">
                      {idea.niche}
                    </span>
                    {idea.score >= 60 && (
                      <div className={`flex items-center gap-1 text-xs ${getScoreColor(idea.score)}`}>
                        <Flame size={12} />
                        <span>{getScoreLabel(idea.score)}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-zinc-900 rounded-xl border border-zinc-800 divide-y divide-zinc-800">
              {ideas.map((idea, idx) => (
                <div
                  key={idx}
                  onClick={() => handlePhraseClick(idea.phrase)}
                  className="group flex items-center justify-between p-4 hover:bg-zinc-800/50 transition-all cursor-pointer"
                >
                  <div className="flex items-center gap-4">
                    <span className="text-xs text-zinc-600 w-8">{idx + 1}</span>
                    <p className="text-sm font-medium text-zinc-200">{idea.phrase}</p>
                    <span className="text-xs px-2 py-1 bg-zinc-800 text-zinc-400 rounded-lg">
                      {idea.niche}
                    </span>
                    {idea.score >= 60 && (
                      <div className={`flex items-center gap-1 text-xs ${getScoreColor(idea.score)}`}>
                        <Flame size={12} />
                        <span>{getScoreLabel(idea.score)}</span>
                      </div>
                    )}
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleCopy(idea.phrase, idx)
                    }}
                    className="opacity-0 group-hover:opacity-100 p-2 hover:bg-zinc-700 rounded-lg transition-all"
                  >
                    {copiedId === idx ? (
                      <Check size={14} className="text-emerald-400" />
                    ) : (
                      <Copy size={14} className="text-zinc-500" />
                    )}
                  </button>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {/* Empty State */}
      {!generateMutation.isPending && ideas.length === 0 && (
        <div className="text-center py-20">
          <div className="w-20 h-20 bg-zinc-900 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-zinc-800">
            <Sparkles size={36} className="text-zinc-600" />
          </div>
          <h3 className="text-lg font-semibold text-zinc-200 mb-2">Ready to generate winning ideas</h3>
          <p className="text-zinc-500 max-w-md mx-auto text-sm">
            Click the button above to generate hundreds of merch phrases based on proven bestseller patterns and trending topics.
          </p>
        </div>
      )}

      {/* Detail Modal */}
      {selectedPhrase && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={closeModal}>
          <div className="bg-zinc-900 rounded-2xl w-full max-w-2xl max-h-[85vh] overflow-hidden border border-zinc-800 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            {/* Modal Header */}
            <div className="flex items-start justify-between p-5 border-b border-zinc-800">
              <div className="flex-1 pr-4">
                <h3 className="text-lg font-semibold text-zinc-100 mb-2">"{selectedPhrase}"</h3>

                {/* Trademark Status */}
                <div className="flex items-center gap-2">
                  {trademarkMutation.isPending ? (
                    <div className="flex items-center gap-2 text-zinc-500 text-sm">
                      <Loader2 size={14} className="animate-spin" />
                      <span>Checking trademark...</span>
                    </div>
                  ) : trademarkStatus[selectedPhrase] ? (
                    trademarkStatus[selectedPhrase].is_safe ? (
                      <div className="flex items-center gap-2 text-emerald-400 text-sm">
                        <ShieldCheck size={16} />
                        <span>Safe to use</span>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 text-red-400 text-sm">
                        <ShieldAlert size={16} />
                        <span>Trademark risk detected</span>
                      </div>
                    )
                  ) : null}
                </div>
              </div>
              <button
                onClick={closeModal}
                className="p-2 hover:bg-zinc-800 rounded-lg transition-all text-zinc-500 hover:text-zinc-300"
              >
                <X size={20} />
              </button>
            </div>

            {/* Variations */}
            <div className="p-5 overflow-y-auto max-h-[60vh]">
              <div className="flex items-center gap-2 mb-4">
                <Wand2 size={16} className="text-emerald-400" />
                <h4 className="text-sm font-medium text-zinc-300">Variations</h4>
              </div>

              {variationsMutation.isPending ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 size={24} className="animate-spin text-zinc-600" />
                </div>
              ) : variations.length > 0 ? (
                <div className="space-y-2">
                  {variations.map((v, idx) => (
                    <div
                      key={idx}
                      className="group flex items-center justify-between p-3 bg-zinc-800/50 rounded-xl hover:bg-zinc-800 transition-all"
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-sm font-medium text-zinc-200">{v.text}</span>
                        {v.is_safe && (
                          <ShieldCheck size={14} className="text-emerald-500" />
                        )}
                      </div>
                      <button
                        onClick={() => handleCopy(v.text, `var-${idx}`)}
                        className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-zinc-700 rounded-lg transition-all"
                      >
                        {copiedId === `var-${idx}` ? (
                          <Check size={14} className="text-emerald-400" />
                        ) : (
                          <Copy size={14} className="text-zinc-500" />
                        )}
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-center text-zinc-600 py-8">No variations available</p>
              )}
            </div>

            {/* Modal Footer */}
            <div className="flex items-center justify-between p-5 border-t border-zinc-800 bg-zinc-900/50">
              <button
                onClick={() => handleCopy(selectedPhrase, 'main')}
                className="flex items-center gap-2 px-4 py-2 bg-zinc-800 hover:bg-zinc-700 rounded-lg text-sm transition-all"
              >
                {copiedId === 'main' ? (
                  <>
                    <Check size={16} className="text-emerald-400" />
                    <span className="text-emerald-400">Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy size={16} className="text-zinc-400" />
                    <span className="text-zinc-300">Copy phrase</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Click outside to close dropdown */}
      {showNicheDropdown && (
        <div className="fixed inset-0 z-40" onClick={() => setShowNicheDropdown(false)} />
      )}
    </div>
  )
}
