import { useState, useEffect } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import {
  getAllTrends,
  refreshTrends,
  getCalendarOverview,
  generateAIPhrases,
  getAvailableTones,
  getBestNiches,
  getBSROpportunities,
  calculateNicheProfitability,
  generateDesignConcept,
  generateOptimizedListing,
  estimateSalesFromBSR,
  calculatePortfolioMetrics,
} from '../api/client'
import {
  TrendingUp,
  Calendar,
  Wand2,
  BarChart3,
  DollarSign,
  Palette,
  FileText,
  Loader2,
  ChevronRight,
  Sparkles,
  Clock,
  AlertTriangle,
  CheckCircle,
  Copy,
  Check,
  Zap,
  Target,
  PieChart,
  ArrowUpRight,
  Hash,
  MessageCircle,
  Flame,
  Star,
  TrendingDown,
  Calculator,
  RefreshCw,
  ExternalLink,
} from 'lucide-react'

const TABS = [
  { id: 'trending', name: 'Social Trends', icon: TrendingUp },
  { id: 'calendar', name: 'Seasonal Calendar', icon: Calendar },
  { id: 'ai', name: 'AI Generator', icon: Wand2 },
  { id: 'bsr', name: 'BSR Tracker', icon: BarChart3 },
  { id: 'profitability', name: 'Profitability', icon: DollarSign },
  { id: 'design', name: 'Design Concepts', icon: Palette },
]

export default function Tools() {
  const [activeTab, setActiveTab] = useState('trending')
  const [copiedText, setCopiedText] = useState(null)

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text)
    setCopiedText(text)
    setTimeout(() => setCopiedText(null), 1500)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-zinc-100">Advanced Tools</h1>
          <p className="text-zinc-500 text-sm mt-1">
            Powerful research tools to dominate merch
          </p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
          <Sparkles size={14} className="text-emerald-400" />
          <span className="text-xs text-emerald-400 font-medium">Pro Features</span>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium whitespace-nowrap transition-all ${
              activeTab === tab.id
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                : 'bg-zinc-800/50 text-zinc-400 hover:bg-zinc-800 hover:text-zinc-300 border border-transparent'
            }`}
          >
            <tab.icon size={16} />
            {tab.name}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="bg-zinc-900 rounded-xl border border-zinc-800 p-6">
        {activeTab === 'trending' && <TrendingTab onCopy={handleCopy} copiedText={copiedText} />}
        {activeTab === 'calendar' && <CalendarTab />}
        {activeTab === 'ai' && <AIGeneratorTab onCopy={handleCopy} copiedText={copiedText} />}
        {activeTab === 'bsr' && <BSRTab />}
        {activeTab === 'profitability' && <ProfitabilityTab />}
        {activeTab === 'design' && <DesignTab />}
      </div>
    </div>
  )
}

// ============ TRENDING TAB ============
function TrendingTab({ onCopy, copiedText }) {
  const [viewMode, setViewMode] = useState('opportunities') // opportunities, platforms, all
  const [expandedTrend, setExpandedTrend] = useState(null)

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['allTrends'],
    queryFn: () => getAllTrends(15),
    staleTime: 1000 * 60 * 15, // 15 minutes
  })

  const refreshMutation = useMutation({
    mutationFn: refreshTrends,
    onSuccess: () => refetch(),
  })

  if (isLoading) return <LoadingState />

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-400 mb-2">Failed to fetch trends</p>
        <button onClick={() => refetch()} className="text-emerald-400 hover:underline">
          Try again
        </button>
      </div>
    )
  }

  const trends = data?.data || {}
  const summary = trends.summary || {}
  const topOpportunities = trends.top_opportunities || []

  // Signal color mapping
  const signalColors = {
    emerald: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    green: 'bg-green-500/20 text-green-400 border-green-500/30',
    yellow: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    orange: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
    red: 'bg-red-500/20 text-red-400 border-red-500/30',
    zinc: 'bg-zinc-500/20 text-zinc-400 border-zinc-500/30',
  }

  // Competition color mapping
  const compColors = {
    low: 'text-emerald-400',
    medium: 'text-yellow-400',
    high: 'text-orange-400',
    very_high: 'text-red-400',
  }

  // Platform display config
  const MERCH_PLATFORMS = [
    { key: 'amazon', name: 'Amazon', color: 'orange', icon: TrendingUp },
    { key: 'etsy', name: 'Etsy', color: 'pink', icon: Hash },
    { key: 'pinterest', name: 'Pinterest', color: 'red', icon: Palette },
  ]

  const VIRAL_PLATFORMS = [
    { key: 'reddit', name: 'Reddit', color: 'orange', icon: ArrowUpRight },
    { key: 'tiktok', name: 'TikTok', color: 'pink', icon: Zap },
    { key: 'twitter', name: 'Twitter/X', color: 'blue', icon: MessageCircle },
  ]

  // Trend Card Component
  const TrendCard = ({ trend, idx, showPlatform = false }) => {
    const signal = trend.signal || {}
    const lifecycle = trend.lifecycle || {}
    const competition = trend.competition || {}
    const isExpanded = expandedTrend === `${trend.trend}-${idx}`

    return (
      <div
        className={`bg-zinc-800/50 rounded-xl border transition-all cursor-pointer ${
          signal.color === 'emerald' ? 'border-emerald-500/30 hover:border-emerald-500/50' :
          signal.color === 'green' ? 'border-green-500/30 hover:border-green-500/50' :
          'border-zinc-700/50 hover:border-zinc-600'
        }`}
        onClick={() => setExpandedTrend(isExpanded ? null : `${trend.trend}-${idx}`)}
      >
        {/* Main Content */}
        <div className="p-4">
          {/* Top Row: Signal + Score */}
          <div className="flex items-center justify-between mb-2">
            <span className={`text-xs font-bold px-2 py-0.5 rounded border ${signalColors[signal.color] || signalColors.zinc}`}>
              {signal.label || '?'}
            </span>
            <div className="flex items-center gap-2">
              <span className={`text-lg font-bold ${
                trend.opportunity_score >= 70 ? 'text-emerald-400' :
                trend.opportunity_score >= 55 ? 'text-yellow-400' : 'text-zinc-400'
              }`}>
                {trend.opportunity_score || 0}
              </span>
              <span className="text-xs text-zinc-500">/ 100</span>
            </div>
          </div>

          {/* Phrase */}
          <h4 className="font-semibold text-zinc-100 mb-2 leading-tight">{trend.trend}</h4>

          {/* Tags Row */}
          <div className="flex flex-wrap items-center gap-2 mb-2">
            {/* Lifecycle Badge */}
            <span className={`text-xs px-2 py-0.5 rounded ${
              lifecycle.color === 'emerald' ? 'bg-emerald-500/20 text-emerald-400' :
              lifecycle.color === 'green' ? 'bg-green-500/20 text-green-400' :
              lifecycle.color === 'orange' ? 'bg-orange-500/20 text-orange-400' :
              lifecycle.color === 'yellow' ? 'bg-yellow-500/20 text-yellow-400' :
              lifecycle.color === 'red' ? 'bg-red-500/20 text-red-400' :
              'bg-blue-500/20 text-blue-400'
            }`}>
              {lifecycle.label || 'Stable'}
            </span>

            {/* Competition */}
            <span className={`text-xs ${compColors[competition.level] || 'text-zinc-400'}`}>
              {competition.icon} {competition.label} comp
            </span>

            {/* Growth */}
            <span className="text-xs text-zinc-500">{trend.growth}</span>
          </div>

          {/* Platform + Actions */}
          <div className="flex items-center justify-between">
            {showPlatform && (
              <span className="text-xs text-zinc-500">{trend.platform}</span>
            )}
            {!showPlatform && <span />}
            <button
              onClick={(e) => {
                e.stopPropagation()
                onCopy(trend.trend)
              }}
              className="p-1.5 hover:bg-zinc-700 rounded"
            >
              {copiedText === trend.trend ? (
                <Check size={14} className="text-emerald-400" />
              ) : (
                <Copy size={14} className="text-zinc-500" />
              )}
            </button>
          </div>
        </div>

        {/* Expanded Details */}
        {isExpanded && (
          <div className="px-4 pb-4 pt-2 border-t border-zinc-700/50 space-y-3">
            {/* Score Breakdown */}
            <div className="grid grid-cols-4 gap-2">
              {trend.score_components && Object.entries(trend.score_components).map(([key, val]) => (
                <div key={key} className="text-center">
                  <div className="text-lg font-bold text-zinc-200">{val}</div>
                  <div className="text-xs text-zinc-500 capitalize">{key.replace('_', ' ')}</div>
                </div>
              ))}
            </div>

            {/* Quick Info */}
            <div className="text-xs text-zinc-400 space-y-1">
              {trend.search_query && trend.search_query !== trend.trend && (
                <p><span className="text-zinc-500">Query:</span> {trend.search_query}</p>
              )}
              <p><span className="text-zinc-500">Source:</span> {trend.source}</p>
              {lifecycle.desc && (
                <p><span className="text-zinc-500">Stage:</span> {lifecycle.desc}</p>
              )}
            </div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-zinc-100">Merch Trend Intelligence</h2>
          <p className="text-sm text-zinc-500">Real-time opportunity scoring for merch research</p>
        </div>
        <div className="flex items-center gap-2">
          {trends.is_live && (
            <span className="text-xs px-2 py-1 bg-emerald-500/20 text-emerald-400 rounded-full animate-pulse">
              ● LIVE
            </span>
          )}
          <button
            onClick={() => refreshMutation.mutate()}
            disabled={refreshMutation.isPending}
            className="flex items-center gap-2 px-3 py-2 bg-zinc-800 rounded-lg text-sm text-zinc-400 hover:text-zinc-200 disabled:opacity-50"
          >
            <RefreshCw size={14} className={refreshMutation.isPending ? 'animate-spin' : ''} />
            Refresh
          </button>
        </div>
      </div>

      {/* Summary Cards - Helium 10 Style */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-1">
            <Target size={14} className="text-emerald-400" />
            <span className="text-xs text-emerald-400">High Opportunity</span>
          </div>
          <p className="text-2xl font-bold text-emerald-400">{summary.high_opportunity_count || 0}</p>
          <p className="text-xs text-zinc-500">Score 70+</p>
        </div>

        <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-1">
            <Zap size={14} className="text-blue-400" />
            <span className="text-xs text-blue-400">Emerging</span>
          </div>
          <p className="text-2xl font-bold text-blue-400">{summary.emerging_count || 0}</p>
          <p className="text-xs text-zinc-500">Early stage</p>
        </div>

        <div className="bg-purple-500/10 border border-purple-500/30 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-1">
            <Star size={14} className="text-purple-400" />
            <span className="text-xs text-purple-400">Low Competition</span>
          </div>
          <p className="text-2xl font-bold text-purple-400">{summary.low_competition_count || 0}</p>
          <p className="text-xs text-zinc-500">Easy entry</p>
        </div>

        <div className="bg-zinc-800/50 border border-zinc-700/50 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-1">
            <BarChart3 size={14} className="text-zinc-400" />
            <span className="text-xs text-zinc-400">Avg Score</span>
          </div>
          <p className="text-2xl font-bold text-zinc-200">{summary.avg_opportunity_score || 0}</p>
          <p className="text-xs text-zinc-500">{trends.counts?.total || 0} total</p>
        </div>
      </div>

      {/* View Mode Tabs */}
      <div className="flex gap-2 border-b border-zinc-800 pb-2">
        {[
          { id: 'opportunities', label: 'Top Opportunities', icon: Target },
          { id: 'platforms', label: 'By Platform', icon: Hash },
          { id: 'all', label: 'All Trends', icon: TrendingUp },
        ].map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setViewMode(id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-all ${
              viewMode === id
                ? 'bg-emerald-500/20 text-emerald-400'
                : 'text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Icon size={14} />
            {label}
          </button>
        ))}
      </div>

      {/* TOP OPPORTUNITIES VIEW */}
      {viewMode === 'opportunities' && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <div className="w-2 h-6 bg-emerald-500 rounded-full" />
            <h3 className="text-sm font-semibold text-emerald-400 uppercase tracking-wide">
              Top Opportunities (Score 70+)
            </h3>
          </div>

          {topOpportunities.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {topOpportunities.map((trend, idx) => (
                <TrendCard key={idx} trend={trend} idx={idx} showPlatform />
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-zinc-500">
              <Target size={32} className="mx-auto mb-2 opacity-50" />
              <p>No high-opportunity trends found</p>
              <p className="text-xs">Try refreshing to fetch new data</p>
            </div>
          )}

          {/* Quick Stats */}
          {topOpportunities.length > 0 && (
            <div className="flex items-center gap-4 text-xs text-zinc-500 pt-2">
              <span>Showing {topOpportunities.length} opportunities</span>
              <span>•</span>
              <span>Click any card for details</span>
            </div>
          )}
        </div>
      )}

      {/* PLATFORMS VIEW */}
      {viewMode === 'platforms' && (
        <div className="space-y-6">
          {/* MERCH TRENDS */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-6 bg-emerald-500 rounded-full" />
              <h3 className="text-sm font-semibold text-emerald-400 uppercase tracking-wide">
                Merch Trends - What's Selling
              </h3>
            </div>

            {MERCH_PLATFORMS.map(({ key, name, icon: Icon }) => (
              <div key={key} className="space-y-3">
                <div className="flex items-center gap-2">
                  <Icon size={16} className="text-zinc-400" />
                  <h4 className="font-medium text-zinc-200">{name}</h4>
                  <span className="text-xs text-zinc-500">{trends[key]?.length || 0}</span>
                </div>

                {(trends[key]?.length || 0) > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {(trends[key] || []).slice(0, 6).map((trend, idx) => (
                      <TrendCard key={idx} trend={trend} idx={idx} />
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-zinc-600 italic">No data available</p>
                )}
              </div>
            ))}
          </div>

          {/* VIRAL TRENDS */}
          <div className="space-y-4 pt-4 border-t border-zinc-800">
            <div className="flex items-center gap-2">
              <div className="w-2 h-6 bg-purple-500 rounded-full" />
              <h3 className="text-sm font-semibold text-purple-400 uppercase tracking-wide">
                Viral Trends - Breaking Now
              </h3>
            </div>

            {VIRAL_PLATFORMS.map(({ key, name, icon: Icon }) => (
              <div key={key} className="space-y-3">
                <div className="flex items-center gap-2">
                  <Icon size={16} className="text-zinc-400" />
                  <h4 className="font-medium text-zinc-200">{name}</h4>
                  <span className="text-xs text-zinc-500">{trends[key]?.length || 0}</span>
                </div>

                {(trends[key]?.length || 0) > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {(trends[key] || []).slice(0, 6).map((trend, idx) => (
                      <TrendCard key={idx} trend={trend} idx={idx} />
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-zinc-600 italic">No data available</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ALL TRENDS VIEW */}
      {viewMode === 'all' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-2 h-6 bg-zinc-500 rounded-full" />
              <h3 className="text-sm font-semibold text-zinc-400 uppercase tracking-wide">
                All Trends (Sorted by Opportunity)
              </h3>
            </div>
            <span className="text-xs text-zinc-500">{trends.combined?.length || 0} trends</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {(trends.combined || []).map((trend, idx) => (
              <TrendCard key={idx} trend={trend} idx={idx} showPlatform />
            ))}
          </div>
        </div>
      )}

      {/* Footer Info */}
      {trends.fetched_at && (
        <p className="text-xs text-zinc-600 text-center pt-4 border-t border-zinc-800">
          Data updated: {new Date(trends.fetched_at).toLocaleString()}
        </p>
      )}
    </div>
  )
}

// ============ CALENDAR TAB ============
function CalendarTab() {
  const { data, isLoading } = useQuery({
    queryKey: ['calendarOverview'],
    queryFn: getCalendarOverview,
  })

  if (isLoading) return <LoadingState />

  const overview = data?.data || {}
  const urgent = overview.urgent_uploads || []
  const upcoming = overview.next_30_days || []

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-zinc-100">Seasonal Calendar</h2>
        <p className="text-sm text-zinc-500">Never miss an upload deadline for seasonal events</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-zinc-800/50 rounded-xl p-4 border border-zinc-700/50">
          <div className="flex items-center gap-2 mb-1">
            <Calendar size={14} className="text-blue-400" />
            <span className="text-xs text-zinc-500">Upcoming</span>
          </div>
          <p className="text-2xl font-bold text-zinc-100">{overview.summary?.total_upcoming || 0}</p>
        </div>
        <div className="bg-zinc-800/50 rounded-xl p-4 border border-zinc-700/50">
          <div className="flex items-center gap-2 mb-1">
            <AlertTriangle size={14} className="text-red-400" />
            <span className="text-xs text-zinc-500">Urgent</span>
          </div>
          <p className="text-2xl font-bold text-red-400">{overview.summary?.urgent_count || 0}</p>
        </div>
        <div className="bg-zinc-800/50 rounded-xl p-4 border border-zinc-700/50">
          <div className="flex items-center gap-2 mb-1">
            <Flame size={14} className="text-orange-400" />
            <span className="text-xs text-zinc-500">Critical</span>
          </div>
          <p className="text-2xl font-bold text-orange-400">{overview.summary?.critical_count || 0}</p>
        </div>
        <div className="bg-zinc-800/50 rounded-xl p-4 border border-zinc-700/50">
          <div className="flex items-center gap-2 mb-1">
            <Clock size={14} className="text-amber-400" />
            <span className="text-xs text-zinc-500">Overdue</span>
          </div>
          <p className="text-2xl font-bold text-amber-400">{overview.summary?.overdue_count || 0}</p>
        </div>
      </div>

      {/* Urgent Events */}
      {urgent.length > 0 && (
        <div className="space-y-3">
          <h3 className="font-medium text-zinc-200 flex items-center gap-2">
            <AlertTriangle size={16} className="text-red-400" />
            Urgent Upload Deadlines
          </h3>
          <div className="space-y-2">
            {urgent.slice(0, 5).map((event, idx) => (
              <div
                key={idx}
                className={`flex items-center justify-between p-4 rounded-xl border ${
                  event.status === 'overdue'
                    ? 'bg-red-500/10 border-red-500/30'
                    : 'bg-amber-500/10 border-amber-500/30'
                }`}
              >
                <div>
                  <p className="font-medium text-zinc-200">{event.name}</p>
                  <p className="text-xs text-zinc-400">
                    Event: {event.event_date} | Upload by: {event.upload_deadline}
                  </p>
                </div>
                <div className="text-right">
                  <p className={`text-sm font-medium ${
                    event.days_to_upload_deadline < 0 ? 'text-red-400' : 'text-amber-400'
                  }`}>
                    {event.days_to_upload_deadline < 0
                      ? `${Math.abs(event.days_to_upload_deadline)} days overdue`
                      : `${event.days_to_upload_deadline} days left`}
                  </p>
                  <p className="text-xs text-zinc-500">{event.priority} priority</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Upcoming Events */}
      <div className="space-y-3">
        <h3 className="font-medium text-zinc-200">Next 30 Days</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {upcoming.slice(0, 8).map((event, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/50"
            >
              <div>
                <p className="font-medium text-zinc-200">{event.name}</p>
                <div className="flex items-center gap-2 mt-1">
                  {event.niches?.slice(0, 3).map((niche, i) => (
                    <span key={i} className="text-xs px-2 py-0.5 bg-zinc-700 text-zinc-400 rounded">
                      {niche}
                    </span>
                  ))}
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium text-emerald-400">{event.days_until} days</p>
                <p className="text-xs text-zinc-500">{event.event_date}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// ============ AI GENERATOR TAB ============
function AIGeneratorTab({ onCopy, copiedText }) {
  const [topic, setTopic] = useState('')
  const [tone, setTone] = useState('funny')
  const [phrases, setPhrases] = useState([])

  const { data: tonesData } = useQuery({
    queryKey: ['availableTones'],
    queryFn: getAvailableTones,
  })

  const generateMutation = useMutation({
    mutationFn: () => generateAIPhrases(topic, tone, 25),
    onSuccess: (data) => {
      setPhrases(data.phrases || [])
    },
  })

  const tones = tonesData?.tones || ['funny', 'sarcastic', 'wholesome', 'edgy', 'motivational', 'aesthetic', 'gen_z', 'millennial']
  const topics = tonesData?.topics_with_vocabulary || []

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-zinc-100">AI Phrase Generator</h2>
        <p className="text-sm text-zinc-500">Generate merch phrases with tone control</p>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap gap-4">
        <div className="flex-1 min-w-[200px]">
          <label className="block text-sm text-zinc-400 mb-2">Topic</label>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., coffee, dogs, anxiety..."
            className="w-full px-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-xl text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-emerald-500"
          />
          {topics.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {topics.slice(0, 8).map((t) => (
                <button
                  key={t}
                  onClick={() => setTopic(t)}
                  className="text-xs px-2 py-1 bg-zinc-800 text-zinc-400 rounded hover:bg-zinc-700"
                >
                  {t}
                </button>
              ))}
            </div>
          )}
        </div>

        <div>
          <label className="block text-sm text-zinc-400 mb-2">Tone</label>
          <select
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            className="px-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-xl text-zinc-200 focus:outline-none focus:border-emerald-500"
          >
            {tones.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>

        <div className="flex items-end">
          <button
            onClick={() => generateMutation.mutate()}
            disabled={!topic || generateMutation.isPending}
            className="flex items-center gap-2 px-6 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-medium disabled:opacity-50"
          >
            {generateMutation.isPending ? (
              <Loader2 size={16} className="animate-spin" />
            ) : (
              <Wand2 size={16} />
            )}
            Generate
          </button>
        </div>
      </div>

      {/* Results */}
      {phrases.length > 0 && (
        <div className="space-y-3">
          <h3 className="font-medium text-zinc-200">Generated Phrases ({phrases.length})</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {phrases.map((p, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-3 bg-zinc-800/50 rounded-xl border border-zinc-700/50 hover:border-zinc-600"
              >
                <span className="text-sm text-zinc-200">{p.phrase}</span>
                <button onClick={() => onCopy(p.phrase)} className="p-1.5 hover:bg-zinc-700 rounded">
                  {copiedText === p.phrase ? (
                    <Check size={14} className="text-emerald-400" />
                  ) : (
                    <Copy size={14} className="text-zinc-500" />
                  )}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

// ============ BSR TAB ============
function BSRTab() {
  const [bsr, setBsr] = useState('')
  const [estimate, setEstimate] = useState(null)

  const { data: opportunities } = useQuery({
    queryKey: ['bsrOpportunities'],
    queryFn: getBSROpportunities,
  })

  const estimateMutation = useMutation({
    mutationFn: (val) => estimateSalesFromBSR(val),
    onSuccess: (data) => setEstimate(data.data),
  })

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-zinc-100">BSR Tracker & Estimator</h2>
        <p className="text-sm text-zinc-500">Estimate sales from Best Seller Rank</p>
      </div>

      {/* BSR Calculator */}
      <div className="flex gap-4 items-end">
        <div>
          <label className="block text-sm text-zinc-400 mb-2">Enter BSR</label>
          <input
            type="number"
            value={bsr}
            onChange={(e) => setBsr(e.target.value)}
            placeholder="e.g., 15000"
            className="w-48 px-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-xl text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-emerald-500"
          />
        </div>
        <button
          onClick={() => bsr && estimateMutation.mutate(parseInt(bsr))}
          className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-medium"
        >
          <Calculator size={16} className="inline mr-2" />
          Estimate
        </button>
      </div>

      {/* Estimate Results */}
      {estimate && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-xl">
          <div>
            <p className="text-xs text-zinc-400">Daily Sales</p>
            <p className="text-xl font-bold text-emerald-400">{estimate.estimated_daily_sales}</p>
          </div>
          <div>
            <p className="text-xs text-zinc-400">Monthly Sales</p>
            <p className="text-xl font-bold text-emerald-400">{estimate.estimated_monthly_sales}</p>
          </div>
          <div>
            <p className="text-xs text-zinc-400">Monthly Revenue</p>
            <p className="text-xl font-bold text-emerald-400">${estimate.estimated_monthly_revenue}</p>
          </div>
          <div>
            <p className="text-xs text-zinc-400">Yearly Revenue</p>
            <p className="text-xl font-bold text-emerald-400">${estimate.estimated_yearly_revenue}</p>
          </div>
        </div>
      )}

      {/* Opportunities */}
      <div className="space-y-3">
        <h3 className="font-medium text-zinc-200">Top Niche Opportunities</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {(opportunities?.opportunities || []).slice(0, 8).map((opp, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/50"
            >
              <div>
                <p className="font-medium text-zinc-200 capitalize">{opp.niche}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`text-xs px-2 py-0.5 rounded ${
                    opp.competition === 'low' ? 'bg-emerald-500/20 text-emerald-400' :
                    opp.competition === 'medium' ? 'bg-amber-500/20 text-amber-400' :
                    'bg-red-500/20 text-red-400'
                  }`}>
                    {opp.competition} competition
                  </span>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-emerald-400">{opp.opportunity_score}</p>
                <p className="text-xs text-zinc-500">~${opp.estimated_monthly_revenue}/mo</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// ============ PROFITABILITY TAB ============
function ProfitabilityTab() {
  const [designsCount, setDesignsCount] = useState(50)
  const [avgSales, setAvgSales] = useState(3)
  const [portfolio, setPortfolio] = useState(null)

  const { data: bestNiches } = useQuery({
    queryKey: ['bestNiches'],
    queryFn: () => getBestNiches(15),
  })

  const portfolioMutation = useMutation({
    mutationFn: () => calculatePortfolioMetrics(designsCount, avgSales),
    onSuccess: (data) => setPortfolio(data.metrics),
  })

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-zinc-100">Profitability Calculator</h2>
        <p className="text-sm text-zinc-500">Calculate niche profitability and portfolio metrics</p>
      </div>

      {/* Portfolio Calculator */}
      <div className="p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/50">
        <h3 className="font-medium text-zinc-200 mb-4">Portfolio Calculator</h3>
        <div className="flex flex-wrap gap-4 items-end">
          <div>
            <label className="block text-sm text-zinc-400 mb-2">Active Designs</label>
            <input
              type="number"
              value={designsCount}
              onChange={(e) => setDesignsCount(parseInt(e.target.value) || 0)}
              className="w-32 px-4 py-2.5 bg-zinc-700 border border-zinc-600 rounded-xl text-zinc-200"
            />
          </div>
          <div>
            <label className="block text-sm text-zinc-400 mb-2">Avg Sales/Design</label>
            <input
              type="number"
              step="0.5"
              value={avgSales}
              onChange={(e) => setAvgSales(parseFloat(e.target.value) || 0)}
              className="w-32 px-4 py-2.5 bg-zinc-700 border border-zinc-600 rounded-xl text-zinc-200"
            />
          </div>
          <button
            onClick={() => portfolioMutation.mutate()}
            className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-medium"
          >
            Calculate
          </button>
        </div>

        {portfolio && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 pt-4 border-t border-zinc-700">
            <div>
              <p className="text-xs text-zinc-400">Monthly Sales</p>
              <p className="text-xl font-bold text-zinc-100">{portfolio.total_monthly_sales}</p>
            </div>
            <div>
              <p className="text-xs text-zinc-400">Monthly Revenue</p>
              <p className="text-xl font-bold text-emerald-400">${portfolio.total_monthly_revenue}</p>
            </div>
            <div>
              <p className="text-xs text-zinc-400">Yearly Revenue</p>
              <p className="text-xl font-bold text-emerald-400">${portfolio.total_yearly_revenue}</p>
            </div>
            <div>
              <p className="text-xs text-zinc-400">Current Tier</p>
              <p className="text-xl font-bold text-blue-400">T{portfolio.current_tier}</p>
            </div>
          </div>
        )}
      </div>

      {/* Best Niches */}
      <div className="space-y-3">
        <h3 className="font-medium text-zinc-200">Most Profitable Niches</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {(bestNiches?.niches || []).map((niche, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-xl border ${
                idx < 3 ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-zinc-800/50 border-zinc-700/50'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-zinc-200 capitalize">{niche.niche}</span>
                {idx < 3 && <Star size={14} className="text-emerald-400" fill="currentColor" />}
              </div>
              <div className="flex items-center justify-between">
                <span className={`text-xs px-2 py-0.5 rounded ${
                  niche.competition_level === 'low' ? 'bg-emerald-500/20 text-emerald-400' :
                  niche.competition_level === 'medium' ? 'bg-amber-500/20 text-amber-400' :
                  'bg-red-500/20 text-red-400'
                }`}>
                  {niche.competition_level}
                </span>
                <span className="text-lg font-bold text-emerald-400">{niche.opportunity_score}</span>
              </div>
              <p className="text-xs text-zinc-500 mt-2">{niche.recommendation?.slice(0, 60)}...</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// ============ DESIGN TAB ============
function DesignTab() {
  const [phrase, setPhrase] = useState('')
  const [style, setStyle] = useState('funny')
  const [concept, setConcept] = useState(null)

  const styles = ['funny', 'motivational', 'sarcastic', 'wholesome', 'edgy', 'aesthetic', 'vintage']

  const conceptMutation = useMutation({
    mutationFn: () => generateDesignConcept(phrase, style),
    onSuccess: (data) => setConcept(data.concept),
  })

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-zinc-100">Design Concept Generator</h2>
        <p className="text-sm text-zinc-500">Get font, color, and layout recommendations</p>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap gap-4 items-end">
        <div className="flex-1 min-w-[200px]">
          <label className="block text-sm text-zinc-400 mb-2">Phrase</label>
          <input
            type="text"
            value={phrase}
            onChange={(e) => setPhrase(e.target.value)}
            placeholder="Enter your phrase..."
            className="w-full px-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-xl text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-emerald-500"
          />
        </div>
        <div>
          <label className="block text-sm text-zinc-400 mb-2">Style</label>
          <select
            value={style}
            onChange={(e) => setStyle(e.target.value)}
            className="px-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-xl text-zinc-200"
          >
            {styles.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
        <button
          onClick={() => phrase && conceptMutation.mutate()}
          disabled={!phrase || conceptMutation.isPending}
          className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-medium disabled:opacity-50"
        >
          {conceptMutation.isPending ? <Loader2 size={16} className="animate-spin" /> : <Palette size={16} className="inline mr-2" />}
          Generate
        </button>
      </div>

      {/* Concept Results */}
      {concept && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Font */}
          <div className="p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/50">
            <h4 className="font-medium text-zinc-200 mb-3 flex items-center gap-2">
              <FileText size={16} className="text-blue-400" />
              Font Pairing
            </h4>
            <p className="text-lg font-medium text-zinc-100">{concept.concept.font_pairing.primary}</p>
            <p className="text-sm text-zinc-400">+ {concept.concept.font_pairing.secondary}</p>
            <span className="inline-block mt-2 text-xs px-2 py-1 bg-blue-500/20 text-blue-400 rounded">
              {concept.concept.font_pairing.style}
            </span>
          </div>

          {/* Colors */}
          <div className="p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/50">
            <h4 className="font-medium text-zinc-200 mb-3 flex items-center gap-2">
              <Palette size={16} className="text-pink-400" />
              Color Palette
            </h4>
            <p className="text-sm text-zinc-400 mb-2">{concept.concept.color_palette.name}</p>
            <div className="flex gap-1">
              {concept.concept.color_palette.colors.map((color, idx) => (
                <div
                  key={idx}
                  className="w-8 h-8 rounded"
                  style={{ backgroundColor: color }}
                  title={color}
                />
              ))}
            </div>
          </div>

          {/* Layout */}
          <div className="p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/50">
            <h4 className="font-medium text-zinc-200 mb-3 flex items-center gap-2">
              <Target size={16} className="text-emerald-400" />
              Layout
            </h4>
            <p className="text-lg font-medium text-zinc-100">{concept.concept.layout.name}</p>
            <p className="text-xs text-zinc-400 mt-1">{concept.concept.layout.description}</p>
          </div>
        </div>
      )}
    </div>
  )
}

// ============ LISTING TAB ============
function ListingTab({ onCopy, copiedText }) {
  const [phrase, setPhrase] = useState('')
  const [niche, setNiche] = useState('general')
  const [listing, setListing] = useState(null)

  const niches = ['general', 'coffee', 'dogs', 'cats', 'mom', 'dad', 'fitness', 'nurse', 'teacher', 'gaming']

  const listingMutation = useMutation({
    mutationFn: () => generateOptimizedListing(phrase, niche),
    onSuccess: (data) => setListing(data.listing),
  })

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-zinc-100">Listing Optimizer</h2>
        <p className="text-sm text-zinc-500">Generate optimized titles, bullets, and keywords</p>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap gap-4 items-end">
        <div className="flex-1 min-w-[200px]">
          <label className="block text-sm text-zinc-400 mb-2">Phrase</label>
          <input
            type="text"
            value={phrase}
            onChange={(e) => setPhrase(e.target.value)}
            placeholder="Enter your shirt phrase..."
            className="w-full px-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-xl text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-emerald-500"
          />
        </div>
        <div>
          <label className="block text-sm text-zinc-400 mb-2">Niche</label>
          <select
            value={niche}
            onChange={(e) => setNiche(e.target.value)}
            className="px-4 py-2.5 bg-zinc-800 border border-zinc-700 rounded-xl text-zinc-200"
          >
            {niches.map((n) => (
              <option key={n} value={n}>{n}</option>
            ))}
          </select>
        </div>
        <button
          onClick={() => phrase && listingMutation.mutate()}
          disabled={!phrase || listingMutation.isPending}
          className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-medium disabled:opacity-50"
        >
          {listingMutation.isPending ? <Loader2 size={16} className="animate-spin" /> : <Zap size={16} className="inline mr-2" />}
          Optimize
        </button>
      </div>

      {/* Listing Results */}
      {listing && (
        <div className="space-y-4">
          {/* Title */}
          <div className="p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/50">
            <div className="flex items-center justify-between mb-2">
              <h4 className="font-medium text-zinc-200">Optimized Title</h4>
              <div className="flex items-center gap-2">
                <span className={`text-xs px-2 py-0.5 rounded ${
                  listing.title.within_limit ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
                }`}>
                  {listing.title.character_count}/60 chars
                </span>
                <span className="text-xs px-2 py-0.5 bg-blue-500/20 text-blue-400 rounded">
                  SEO: {listing.title.seo_score}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <p className="flex-1 text-zinc-100">{listing.title.primary}</p>
              <button onClick={() => onCopy(listing.title.primary)} className="p-2 hover:bg-zinc-700 rounded">
                {copiedText === listing.title.primary ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} className="text-zinc-500" />}
              </button>
            </div>
            {listing.title.alternatives?.length > 0 && (
              <div className="mt-3 pt-3 border-t border-zinc-700">
                <p className="text-xs text-zinc-500 mb-2">Alternatives:</p>
                {listing.title.alternatives.map((alt, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-sm text-zinc-400 mb-1">
                    <span>{alt}</span>
                    <button onClick={() => onCopy(alt)} className="p-1 hover:bg-zinc-700 rounded">
                      <Copy size={12} className="text-zinc-600" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Keywords */}
          <div className="p-4 bg-zinc-800/50 rounded-xl border border-zinc-700/50">
            <div className="flex items-center justify-between mb-2">
              <h4 className="font-medium text-zinc-200">Backend Keywords</h4>
              <span className={`text-xs px-2 py-0.5 rounded ${
                listing.keywords.within_limit ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
              }`}>
                {listing.keywords.byte_count}/250 bytes
              </span>
            </div>
            <div className="flex items-center gap-2">
              <p className="flex-1 text-sm text-zinc-300 font-mono bg-zinc-900 p-3 rounded-lg">
                {listing.keywords.keywords}
              </p>
              <button onClick={() => onCopy(listing.keywords.keywords)} className="p-2 hover:bg-zinc-700 rounded">
                {copiedText === listing.keywords.keywords ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} className="text-zinc-500" />}
              </button>
            </div>
          </div>

          {/* Tips */}
          {listing.tips?.length > 0 && (
            <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-xl">
              <h4 className="font-medium text-blue-400 mb-2">Optimization Tips</h4>
              <ul className="space-y-1">
                {listing.tips.map((tip, idx) => (
                  <li key={idx} className="text-sm text-zinc-300 flex items-center gap-2">
                    <CheckCircle size={12} className="text-blue-400" />
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// ============ LOADING STATE ============
function LoadingState() {
  return (
    <div className="flex items-center justify-center py-12">
      <Loader2 size={32} className="animate-spin text-emerald-400" />
    </div>
  )
}
