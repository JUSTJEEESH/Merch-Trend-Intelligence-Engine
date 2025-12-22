import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { generateIdeas, getAvailableNiches, generateVariations } from '../api/client'
import {
  Sparkles,
  Loader2,
  Copy,
  Check,
  Filter,
  ChevronDown,
  ChevronUp,
  Star,
  RefreshCw,
  Wand2,
  X,
} from 'lucide-react'

const NICHE_OPTIONS = [
  'All Niches',
  'outdoors',
  'fitness',
  'coffee',
  'pets',
  'parenting',
  'gaming',
  'nursing',
  'teaching',
  'beer',
  'wine',
  'fishing',
  'hunting',
]

const CREATIVITY_OPTIONS = [
  { value: 'low', label: 'Safe', desc: 'Proven patterns only' },
  { value: 'medium', label: 'Balanced', desc: 'Mix of proven and new' },
  { value: 'high', label: 'Experimental', desc: 'More creative combinations' },
]

export default function Dashboard() {
  const [ideas, setIdeas] = useState([])
  const [selectedNiche, setSelectedNiche] = useState('All Niches')
  const [creativity, setCreativity] = useState('medium')
  const [count, setCount] = useState(200)
  const [showFilters, setShowFilters] = useState(false)
  const [copiedId, setCopiedId] = useState(null)
  const [selectedPhrase, setSelectedPhrase] = useState(null)
  const [variations, setVariations] = useState([])
  const [viewMode, setViewMode] = useState('grid') // grid or list

  const generateMutation = useMutation({
    mutationFn: generateIdeas,
    onSuccess: (data) => {
      setIdeas(data.ideas || [])
    },
  })

  const variationsMutation = useMutation({
    mutationFn: (phrase) => generateVariations({ phrase, count: 20 }),
    onSuccess: (data) => {
      setVariations(data.variations || [])
    },
  })

  const handleGenerate = () => {
    const params = {
      count,
      creativity,
      include_classics: true,
      include_generated: true,
      include_variations: true,
    }
    if (selectedNiche !== 'All Niches') {
      params.niches = selectedNiche
    }
    generateMutation.mutate(params)
  }

  const handleCopy = (phrase, id) => {
    navigator.clipboard.writeText(phrase)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const handlePhraseClick = (phrase) => {
    setSelectedPhrase(phrase)
    variationsMutation.mutate(phrase)
  }

  const closeVariations = () => {
    setSelectedPhrase(null)
    setVariations([])
  }

  const filteredIdeas = ideas

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Generate Ideas</h1>
          <p className="text-gray-500 mt-1 text-sm">
            One click to generate hundreds of merch phrase ideas
          </p>
        </div>
      </div>

      {/* Main Generation Card */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-end">
          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={generateMutation.isPending}
            className="flex items-center justify-center gap-2 px-8 py-4 bg-gray-900 text-white rounded-xl font-medium text-lg hover:bg-gray-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
          >
            {generateMutation.isPending ? (
              <>
                <Loader2 size={22} className="animate-spin" />
                <span>Generating...</span>
              </>
            ) : (
              <>
                <Sparkles size={22} />
                <span>Generate {count} Ideas</span>
              </>
            )}
          </button>

          {/* Quick Filters */}
          <div className="flex items-center gap-3">
            <select
              value={selectedNiche}
              onChange={(e) => setSelectedNiche(e.target.value)}
              className="px-4 py-3 border border-gray-200 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-gray-900"
            >
              {NICHE_OPTIONS.map((niche) => (
                <option key={niche} value={niche}>
                  {niche === 'All Niches' ? 'All Niches' : niche.charAt(0).toUpperCase() + niche.slice(1)}
                </option>
              ))}
            </select>

            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center gap-2 px-4 py-3 border border-gray-200 rounded-lg text-sm hover:bg-gray-50"
            >
              <Filter size={16} />
              <span>Options</span>
              {showFilters ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
          </div>
        </div>

        {/* Expanded Filters */}
        {showFilters && (
          <div className="mt-6 pt-6 border-t border-gray-100 grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Ideas
              </label>
              <input
                type="range"
                min="50"
                max="500"
                step="50"
                value={count}
                onChange={(e) => setCount(parseInt(e.target.value))}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>50</span>
                <span className="font-medium text-gray-900">{count}</span>
                <span>500</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Creativity Level
              </label>
              <div className="space-y-2">
                {CREATIVITY_OPTIONS.map((opt) => (
                  <label
                    key={opt.value}
                    className={`flex items-center gap-3 p-2 rounded-lg cursor-pointer transition-all ${
                      creativity === opt.value
                        ? 'bg-gray-100'
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <input
                      type="radio"
                      name="creativity"
                      value={opt.value}
                      checked={creativity === opt.value}
                      onChange={(e) => setCreativity(e.target.value)}
                      className="sr-only"
                    />
                    <div
                      className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                        creativity === opt.value
                          ? 'border-gray-900'
                          : 'border-gray-300'
                      }`}
                    >
                      {creativity === opt.value && (
                        <div className="w-2 h-2 rounded-full bg-gray-900" />
                      )}
                    </div>
                    <div>
                      <div className="text-sm font-medium">{opt.label}</div>
                      <div className="text-xs text-gray-500">{opt.desc}</div>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                View Mode
              </label>
              <div className="flex gap-2">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                    viewMode === 'grid'
                      ? 'bg-gray-900 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  Grid
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                    viewMode === 'list'
                      ? 'bg-gray-900 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  List
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Results */}
      {generateMutation.isPending && (
        <div className="flex items-center justify-center py-20">
          <div className="text-center">
            <Loader2 size={40} className="animate-spin text-gray-400 mx-auto" />
            <p className="text-gray-500 mt-4">Generating your ideas...</p>
          </div>
        </div>
      )}

      {!generateMutation.isPending && ideas.length > 0 && (
        <>
          {/* Stats Bar */}
          <div className="flex items-center justify-between text-sm">
            <div className="text-gray-600">
              <span className="font-semibold text-gray-900">{ideas.length}</span> ideas generated
            </div>
            <button
              onClick={handleGenerate}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
            >
              <RefreshCw size={14} />
              <span>Regenerate</span>
            </button>
          </div>

          {/* Ideas Grid/List */}
          {viewMode === 'grid' ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
              {filteredIdeas.map((idea, idx) => (
                <div
                  key={idx}
                  className="group bg-white rounded-lg border border-gray-200 p-4 hover:border-gray-300 hover:shadow-sm transition-all cursor-pointer"
                  onClick={() => handlePhraseClick(idea.phrase)}
                >
                  <div className="flex items-start justify-between gap-2">
                    <p className="text-sm font-medium text-gray-900 leading-snug">
                      {idea.phrase}
                    </p>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleCopy(idea.phrase, idx)
                      }}
                      className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-gray-100 rounded transition-all"
                    >
                      {copiedId === idx ? (
                        <Check size={14} className="text-green-600" />
                      ) : (
                        <Copy size={14} className="text-gray-400" />
                      )}
                    </button>
                  </div>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded">
                      {idea.niche}
                    </span>
                    {idea.score >= 70 && (
                      <Star size={12} className="text-amber-500" fill="currentColor" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-gray-200 divide-y divide-gray-100">
              {filteredIdeas.map((idea, idx) => (
                <div
                  key={idx}
                  className="group flex items-center justify-between p-4 hover:bg-gray-50 transition-all cursor-pointer"
                  onClick={() => handlePhraseClick(idea.phrase)}
                >
                  <div className="flex items-center gap-4">
                    <span className="text-xs text-gray-400 w-8">{idx + 1}</span>
                    <p className="text-sm font-medium text-gray-900">{idea.phrase}</p>
                    <span className="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded">
                      {idea.niche}
                    </span>
                    {idea.score >= 70 && (
                      <Star size={12} className="text-amber-500" fill="currentColor" />
                    )}
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleCopy(idea.phrase, idx)
                    }}
                    className="opacity-0 group-hover:opacity-100 p-2 hover:bg-gray-200 rounded transition-all"
                  >
                    {copiedId === idx ? (
                      <Check size={14} className="text-green-600" />
                    ) : (
                      <Copy size={14} className="text-gray-400" />
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
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Sparkles size={28} className="text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to generate ideas</h3>
          <p className="text-gray-500 max-w-md mx-auto">
            Click the button above to generate hundreds of merch phrase ideas based on proven bestseller patterns.
          </p>
        </div>
      )}

      {/* Variations Modal */}
      {selectedPhrase && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl w-full max-w-2xl max-h-[80vh] overflow-hidden shadow-2xl">
            <div className="flex items-center justify-between p-6 border-b border-gray-100">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Phrase Variations</h3>
                <p className="text-sm text-gray-500 mt-1">"{selectedPhrase}"</p>
              </div>
              <button
                onClick={closeVariations}
                className="p-2 hover:bg-gray-100 rounded-lg transition-all"
              >
                <X size={20} />
              </button>
            </div>

            <div className="p-6 overflow-y-auto max-h-[60vh]">
              {variationsMutation.isPending ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 size={32} className="animate-spin text-gray-400" />
                </div>
              ) : variations.length > 0 ? (
                <div className="space-y-2">
                  {variations.map((v, idx) => (
                    <div
                      key={idx}
                      className="group flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-all"
                    >
                      <div className="flex items-center gap-3">
                        <Wand2 size={14} className="text-gray-400" />
                        <span className="text-sm font-medium text-gray-900">{v.text}</span>
                        {v.is_safe && (
                          <span className="text-xs px-1.5 py-0.5 bg-green-100 text-green-700 rounded">
                            Safe
                          </span>
                        )}
                      </div>
                      <button
                        onClick={() => handleCopy(v.text, `var-${idx}`)}
                        className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-gray-200 rounded transition-all"
                      >
                        {copiedId === `var-${idx}` ? (
                          <Check size={14} className="text-green-600" />
                        ) : (
                          <Copy size={14} className="text-gray-400" />
                        )}
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-center text-gray-500 py-12">No variations generated</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
