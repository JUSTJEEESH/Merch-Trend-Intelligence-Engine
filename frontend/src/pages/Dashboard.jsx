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
  Shield,
  ShieldCheck,
  ShieldAlert,
  X,
  Wand2,
  Zap,
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
  Baby,
  Stethoscope,
  GraduationCap,
  Mountain,
  Crosshair,
  Trash2,
  BookmarkPlus,
  Bookmark,
  Search,
  ArrowUpRight,
  BarChart3,
  DollarSign,
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

// Simulated trending data (would come from API in production)
const TRENDING_NOW = [
  { phrase: "In my healing era", bsr: 1250, trend: "+340%", platform: "Amazon" },
  { phrase: "Overstimulated moms club", bsr: 890, trend: "+280%", platform: "Amazon" },
  { phrase: "Anxious but hopeful", bsr: 2100, trend: "+195%", platform: "Etsy" },
  { phrase: "Professional overthinker", bsr: 1680, trend: "+175%", platform: "Amazon" },
  { phrase: "Touch grass enthusiast", bsr: 3200, trend: "+160%", platform: "Amazon" },
  { phrase: "Emotionally unavailable", bsr: 2800, trend: "+145%", platform: "Etsy" },
]

const STORAGE_KEY = 'merch_engine_ideas'
const FAVORITES_KEY = 'merch_engine_favorites'

export default function Dashboard() {
  const [ideas, setIdeas] = useState([])
  const [favorites, setFavorites] = useState([])
  const [selectedNiche, setSelectedNiche] = useState('all')
  const [count, setCount] = useState(200)
  const [copiedId, setCopiedId] = useState(null)
  const [selectedPhrase, setSelectedPhrase] = useState(null)
  const [variations, setVariations] = useState([])
  const [trademarkStatus, setTrademarkStatus] = useState({})
  const [viewMode, setViewMode] = useState('grid')
  const [showNicheDropdown, setShowNicheDropdown] = useState(false)
  const [searchFilter, setSearchFilter] = useState('')
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false)

  // Load ideas and favorites from localStorage on mount
  useEffect(() => {
    const savedIdeas = localStorage.getItem(STORAGE_KEY)
    const savedFavorites = localStorage.getItem(FAVORITES_KEY)
    if (savedIdeas) {
      try {
        setIdeas(JSON.parse(savedIdeas))
      } catch (e) {
        console.error('Failed to parse saved ideas')
      }
    }
    if (savedFavorites) {
      try {
        setFavorites(JSON.parse(savedFavorites))
      } catch (e) {
        console.error('Failed to parse saved favorites')
      }
    }
  }, [])

  // Save ideas to localStorage when they change
  useEffect(() => {
    if (ideas.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(ideas))
    }
  }, [ideas])

  // Save favorites to localStorage
  useEffect(() => {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites))
  }, [favorites])

  const generateMutation = useMutation({
    mutationFn: generateIdeas,
    onSuccess: (data) => {
      const newIdeas = data.ideas || []
      setIdeas(prev => {
        // Add new ideas, avoiding duplicates
        const existingPhrases = new Set(prev.map(i => i.phrase.toLowerCase()))
        const uniqueNew = newIdeas.filter(i => !existingPhrases.has(i.phrase.toLowerCase()))
        return [...uniqueNew, ...prev]
      })
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

  const handleClearAll = () => {
    setIdeas([])
    localStorage.removeItem(STORAGE_KEY)
  }

  const handleCopy = (phrase, id) => {
    navigator.clipboard.writeText(phrase)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 1500)
  }

  const handleToggleFavorite = (phrase, e) => {
    if (e) e.stopPropagation()
    setFavorites(prev => {
      if (prev.includes(phrase)) {
        return prev.filter(p => p !== phrase)
      }
      return [...prev, phrase]
    })
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

  // Filter ideas
  const filteredIdeas = ideas.filter(idea => {
    const matchesSearch = !searchFilter ||
      idea.phrase.toLowerCase().includes(searchFilter.toLowerCase())
    const matchesFavorites = !showFavoritesOnly || favorites.includes(idea.phrase)
    const matchesNiche = selectedNiche === 'all' || idea.niche === selectedNiche
    return matchesSearch && matchesFavorites && matchesNiche
  })

  const currentNiche = NICHES.find(n => n.id === selectedNiche)

  return (
    <div className="space-y-6">
      {/* Trending Section */}
      <div className="bg-gradient-to-r from-zinc-900 to-zinc-900/50 rounded-xl border border-zinc-800 p-5">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <TrendingUp size={18} className="text-emerald-400" />
            <h2 className="text-base font-semibold text-zinc-200">Trending Now</h2>
            <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded-full">Live</span>
          </div>
          <span className="text-xs text-zinc-500">Updated hourly</span>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {TRENDING_NOW.map((item, idx) => (
            <div
              key={idx}
              onClick={() => handlePhraseClick(item.phrase)}
              className="group bg-zinc-800/50 rounded-xl p-3 hover:bg-zinc-800 transition-all cursor-pointer border border-transparent hover:border-zinc-700"
            >
              <p className="text-sm font-medium text-zinc-200 mb-2 line-clamp-2">{item.phrase}</p>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1 text-xs text-emerald-400">
                  <ArrowUpRight size={12} />
                  <span>{item.trend}</span>
                </div>
                <span className="text-xs text-zinc-500">{item.platform}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-zinc-100">Idea Generator</h1>
          <p className="text-zinc-500 text-sm mt-1">
            {ideas.length > 0 ? (
              <><span className="text-emerald-400 font-semibold">{ideas.length}</span> ideas saved</>
            ) : (
              'Generate hundreds of winning merch phrases'
            )}
          </p>
        </div>
        {favorites.length > 0 && (
          <div className="flex items-center gap-2 text-amber-400">
            <Star size={16} fill="currentColor" />
            <span className="text-sm font-medium">{favorites.length} saved</span>
          </div>
        )}
      </div>

      {/* Control Panel */}
      <div className="bg-zinc-900 rounded-xl border border-zinc-800 p-5">
        <div className="flex flex-wrap items-center gap-3">
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
                <span>Generate {count}</span>
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
              <span>{currentNiche?.name || 'All'}</span>
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
          <div className="flex items-center gap-3 px-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-xl">
            <span className="text-sm text-zinc-400">Count:</span>
            <input
              type="range"
              min="50"
              max="500"
              step="50"
              value={count}
              onChange={(e) => setCount(parseInt(e.target.value))}
              className="w-20 accent-emerald-500"
            />
            <span className="text-sm font-medium text-zinc-200 w-8">{count}</span>
          </div>

          {/* Search */}
          <div className="relative flex-1 min-w-[200px]">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
            <input
              type="text"
              placeholder="Filter ideas..."
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-xl text-sm text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-zinc-600"
            />
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

          {/* Favorites Toggle */}
          <button
            onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
            className={`flex items-center gap-2 px-3 py-2.5 rounded-xl text-sm transition-all ${
              showFavoritesOnly
                ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                : 'bg-zinc-800 border border-zinc-700 text-zinc-400 hover:text-zinc-300'
            }`}
          >
            <Star size={16} fill={showFavoritesOnly ? 'currentColor' : 'none'} />
            <span>Favorites</span>
          </button>

          {/* Clear All */}
          {ideas.length > 0 && (
            <button
              onClick={handleClearAll}
              className="flex items-center gap-2 px-3 py-2.5 text-red-400 hover:bg-red-500/10 rounded-xl text-sm transition-all"
            >
              <Trash2 size={16} />
              <span>Clear All</span>
            </button>
          )}
        </div>
      </div>

      {/* Loading State */}
      {generateMutation.isPending && (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="w-14 h-14 bg-zinc-900 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-zinc-800">
              <Loader2 size={28} className="animate-spin text-emerald-400" />
            </div>
            <p className="text-zinc-400">Generating ideas...</p>
          </div>
        </div>
      )}

      {/* Results */}
      {filteredIdeas.length > 0 && (
        <>
          {viewMode === 'grid' ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
              {filteredIdeas.map((idea, idx) => {
                const isFavorite = favorites.includes(idea.phrase)
                return (
                  <div
                    key={idx}
                    onClick={() => handlePhraseClick(idea.phrase)}
                    className={`group bg-zinc-900 rounded-xl border p-4 hover:bg-zinc-800/50 transition-all cursor-pointer ${
                      isFavorite ? 'border-amber-500/30' : 'border-zinc-800 hover:border-zinc-700'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2 mb-3">
                      <p className="text-sm font-medium text-zinc-200 leading-relaxed">
                        {idea.phrase}
                      </p>
                      <div className="flex items-center gap-1 shrink-0">
                        <button
                          onClick={(e) => handleToggleFavorite(idea.phrase, e)}
                          className="p-1.5 hover:bg-zinc-700 rounded-lg transition-all"
                        >
                          <Star
                            size={14}
                            className={isFavorite ? 'text-amber-400' : 'text-zinc-600'}
                            fill={isFavorite ? 'currentColor' : 'none'}
                          />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            handleCopy(idea.phrase, idx)
                          }}
                          className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-zinc-700 rounded-lg transition-all"
                        >
                          {copiedId === idx ? (
                            <Check size={14} className="text-emerald-400" />
                          ) : (
                            <Copy size={14} className="text-zinc-500" />
                          )}
                        </button>
                      </div>
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
                )
              })}
            </div>
          ) : (
            <div className="bg-zinc-900 rounded-xl border border-zinc-800 divide-y divide-zinc-800">
              {filteredIdeas.map((idea, idx) => {
                const isFavorite = favorites.includes(idea.phrase)
                return (
                  <div
                    key={idx}
                    onClick={() => handlePhraseClick(idea.phrase)}
                    className="group flex items-center justify-between p-4 hover:bg-zinc-800/50 transition-all cursor-pointer"
                  >
                    <div className="flex items-center gap-4 flex-1">
                      <button
                        onClick={(e) => handleToggleFavorite(idea.phrase, e)}
                        className="p-1 hover:bg-zinc-700 rounded transition-all"
                      >
                        <Star
                          size={14}
                          className={isFavorite ? 'text-amber-400' : 'text-zinc-600'}
                          fill={isFavorite ? 'currentColor' : 'none'}
                        />
                      </button>
                      <span className="text-xs text-zinc-600 w-6">{idx + 1}</span>
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
                )
              })}
            </div>
          )}
        </>
      )}

      {/* Empty State */}
      {!generateMutation.isPending && filteredIdeas.length === 0 && ideas.length === 0 && (
        <div className="text-center py-16">
          <div className="w-20 h-20 bg-zinc-900 rounded-2xl flex items-center justify-center mx-auto mb-6 border border-zinc-800">
            <Sparkles size={36} className="text-zinc-600" />
          </div>
          <h3 className="text-lg font-semibold text-zinc-200 mb-2">Ready to generate winning ideas</h3>
          <p className="text-zinc-500 max-w-md mx-auto text-sm">
            Click Generate to create hundreds of merch phrases. Your ideas are automatically saved.
          </p>
        </div>
      )}

      {/* Filtered Empty */}
      {!generateMutation.isPending && filteredIdeas.length === 0 && ideas.length > 0 && (
        <div className="text-center py-12">
          <p className="text-zinc-500">No ideas match your filters</p>
          <button
            onClick={() => {
              setSearchFilter('')
              setShowFavoritesOnly(false)
              setSelectedNiche('all')
            }}
            className="mt-2 text-emerald-400 text-sm hover:underline"
          >
            Clear filters
          </button>
        </div>
      )}

      {/* Detail Modal */}
      {selectedPhrase && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={closeModal}>
          <div className="bg-zinc-900 rounded-2xl w-full max-w-2xl max-h-[85vh] overflow-hidden border border-zinc-800 shadow-2xl" onClick={(e) => e.stopPropagation()}>
            {/* Modal Header */}
            <div className="flex items-start justify-between p-5 border-b border-zinc-800">
              <div className="flex-1 pr-4">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-lg font-semibold text-zinc-100">"{selectedPhrase}"</h3>
                  <button
                    onClick={(e) => handleToggleFavorite(selectedPhrase, e)}
                    className="p-1.5 hover:bg-zinc-800 rounded-lg transition-all"
                  >
                    <Star
                      size={18}
                      className={favorites.includes(selectedPhrase) ? 'text-amber-400' : 'text-zinc-600'}
                      fill={favorites.includes(selectedPhrase) ? 'currentColor' : 'none'}
                    />
                  </button>
                </div>

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
                      <div className="flex items-center gap-1">
                        <button
                          onClick={() => handleToggleFavorite(v.text)}
                          className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-zinc-700 rounded-lg transition-all"
                        >
                          <Star
                            size={14}
                            className={favorites.includes(v.text) ? 'text-amber-400' : 'text-zinc-600'}
                            fill={favorites.includes(v.text) ? 'currentColor' : 'none'}
                          />
                        </button>
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
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-center text-zinc-600 py-8">No variations available</p>
              )}
            </div>

            {/* Modal Footer */}
            <div className="flex items-center gap-3 p-5 border-t border-zinc-800 bg-zinc-900/50">
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
