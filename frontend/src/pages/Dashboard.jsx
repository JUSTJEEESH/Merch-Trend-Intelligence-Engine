import { useState, useEffect } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { generateIdeas, generateVariations, checkTrademark, getAllTrends, refreshTrends } from '../api/client'
import {
  Sparkles,
  Loader2,
  Copy,
  Check,
  ChevronDown,
  ChevronRight,
  TrendingUp,
  TrendingDown,
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
  Download,
  Clock,
  AlertTriangle,
  Target,
} from 'lucide-react'

// Comprehensive niche list matching backend - 100+ niches
const NICHES = [
  { id: 'all', name: 'All Niches', icon: Grid3X3, category: 'all' },
  // Beverages
  { id: 'coffee', name: 'Coffee', icon: Coffee, category: 'beverages' },
  { id: 'tea', name: 'Tea', icon: Coffee, category: 'beverages' },
  { id: 'beer', name: 'Beer', icon: Beer, category: 'beverages' },
  { id: 'wine', name: 'Wine', icon: Wine, category: 'beverages' },
  { id: 'whiskey', name: 'Whiskey', icon: Wine, category: 'beverages' },
  { id: 'cocktails', name: 'Cocktails', icon: Wine, category: 'beverages' },
  // Fitness
  { id: 'fitness', name: 'Fitness', icon: Dumbbell, category: 'fitness' },
  { id: 'yoga', name: 'Yoga', icon: Dumbbell, category: 'fitness' },
  { id: 'running', name: 'Running', icon: Dumbbell, category: 'fitness' },
  { id: 'crossfit', name: 'CrossFit', icon: Dumbbell, category: 'fitness' },
  { id: 'weightlifting', name: 'Weightlifting', icon: Dumbbell, category: 'fitness' },
  { id: 'bodybuilding', name: 'Bodybuilding', icon: Dumbbell, category: 'fitness' },
  { id: 'swimming', name: 'Swimming', icon: Dumbbell, category: 'fitness' },
  { id: 'cycling', name: 'Cycling', icon: Dumbbell, category: 'fitness' },
  { id: 'pilates', name: 'Pilates', icon: Dumbbell, category: 'fitness' },
  // Sports
  { id: 'golf', name: 'Golf', icon: Mountain, category: 'sports' },
  { id: 'baseball', name: 'Baseball', icon: Gamepad2, category: 'sports' },
  { id: 'football', name: 'Football', icon: Gamepad2, category: 'sports' },
  { id: 'basketball', name: 'Basketball', icon: Gamepad2, category: 'sports' },
  { id: 'hockey', name: 'Hockey', icon: Gamepad2, category: 'sports' },
  { id: 'soccer', name: 'Soccer', icon: Gamepad2, category: 'sports' },
  { id: 'tennis', name: 'Tennis', icon: Gamepad2, category: 'sports' },
  { id: 'volleyball', name: 'Volleyball', icon: Gamepad2, category: 'sports' },
  { id: 'wrestling', name: 'Wrestling', icon: Gamepad2, category: 'sports' },
  { id: 'boxing', name: 'Boxing', icon: Gamepad2, category: 'sports' },
  { id: 'mma', name: 'MMA', icon: Gamepad2, category: 'sports' },
  { id: 'pickleball', name: 'Pickleball', icon: Gamepad2, category: 'sports' },
  // Outdoors
  { id: 'hiking', name: 'Hiking', icon: Mountain, category: 'outdoors' },
  { id: 'camping', name: 'Camping', icon: Mountain, category: 'outdoors' },
  { id: 'fishing', name: 'Fishing', icon: Fish, category: 'outdoors' },
  { id: 'hunting', name: 'Hunting', icon: Crosshair, category: 'outdoors' },
  { id: 'kayaking', name: 'Kayaking', icon: Mountain, category: 'outdoors' },
  { id: 'skiing', name: 'Skiing', icon: Mountain, category: 'outdoors' },
  { id: 'snowboarding', name: 'Snowboarding', icon: Mountain, category: 'outdoors' },
  { id: 'surfing', name: 'Surfing', icon: Mountain, category: 'outdoors' },
  { id: 'climbing', name: 'Climbing', icon: Mountain, category: 'outdoors' },
  { id: 'boating', name: 'Boating', icon: Mountain, category: 'outdoors' },
  { id: 'rv', name: 'RV Life', icon: Mountain, category: 'outdoors' },
  { id: 'offroading', name: 'Off-roading', icon: Mountain, category: 'outdoors' },
  // Pets
  { id: 'dogs', name: 'Dogs', icon: Dog, category: 'pets' },
  { id: 'cats', name: 'Cats', icon: Dog, category: 'pets' },
  { id: 'horses', name: 'Horses', icon: Dog, category: 'pets' },
  { id: 'chickens', name: 'Chickens', icon: Dog, category: 'pets' },
  { id: 'goats', name: 'Goats', icon: Dog, category: 'pets' },
  { id: 'bees', name: 'Bees', icon: Dog, category: 'pets' },
  { id: 'birds', name: 'Birds', icon: Dog, category: 'pets' },
  { id: 'reptiles', name: 'Reptiles', icon: Dog, category: 'pets' },
  { id: 'rabbits', name: 'Rabbits', icon: Dog, category: 'pets' },
  { id: 'aquarium', name: 'Aquarium', icon: Fish, category: 'pets' },
  // Professions
  { id: 'nursing', name: 'Nursing', icon: Stethoscope, category: 'professions' },
  { id: 'teaching', name: 'Teaching', icon: GraduationCap, category: 'professions' },
  { id: 'trucking', name: 'Trucking', icon: Mountain, category: 'professions' },
  { id: 'firefighter', name: 'Firefighter', icon: Stethoscope, category: 'professions' },
  { id: 'police', name: 'Police', icon: Stethoscope, category: 'professions' },
  { id: 'emt', name: 'EMT', icon: Stethoscope, category: 'professions' },
  { id: 'military', name: 'Military', icon: Stethoscope, category: 'professions' },
  { id: 'mechanic', name: 'Mechanic', icon: Mountain, category: 'professions' },
  { id: 'welder', name: 'Welder', icon: Mountain, category: 'professions' },
  { id: 'electrician', name: 'Electrician', icon: Mountain, category: 'professions' },
  { id: 'plumber', name: 'Plumber', icon: Mountain, category: 'professions' },
  { id: 'carpenter', name: 'Carpenter', icon: Mountain, category: 'professions' },
  { id: 'farmer', name: 'Farmer', icon: Mountain, category: 'professions' },
  { id: 'chef', name: 'Chef', icon: Coffee, category: 'professions' },
  { id: 'hairstylist', name: 'Hairstylist', icon: Stethoscope, category: 'professions' },
  { id: 'realtor', name: 'Realtor', icon: Mountain, category: 'professions' },
  { id: 'lawyer', name: 'Lawyer', icon: GraduationCap, category: 'professions' },
  { id: 'accountant', name: 'Accountant', icon: GraduationCap, category: 'professions' },
  { id: 'engineer', name: 'Engineer', icon: GraduationCap, category: 'professions' },
  { id: 'programmer', name: 'Programmer', icon: Gamepad2, category: 'professions' },
  { id: 'dispatcher', name: 'Dispatcher', icon: Stethoscope, category: 'professions' },
  { id: 'librarian', name: 'Librarian', icon: GraduationCap, category: 'professions' },
  { id: 'pilot', name: 'Pilot', icon: Mountain, category: 'professions' },
  { id: 'dental', name: 'Dental', icon: Stethoscope, category: 'professions' },
  { id: 'pharmacy', name: 'Pharmacy', icon: Stethoscope, category: 'professions' },
  // Family
  { id: 'mom', name: 'Mom', icon: Baby, category: 'family' },
  { id: 'dad', name: 'Dad', icon: Baby, category: 'family' },
  { id: 'grandma', name: 'Grandma', icon: Baby, category: 'family' },
  { id: 'grandpa', name: 'Grandpa', icon: Baby, category: 'family' },
  { id: 'parenting', name: 'Parenting', icon: Baby, category: 'family' },
  { id: 'pregnancy', name: 'Pregnancy', icon: Baby, category: 'family' },
  { id: 'twins', name: 'Twins', icon: Baby, category: 'family' },
  { id: 'aunt', name: 'Aunt', icon: Baby, category: 'family' },
  { id: 'uncle', name: 'Uncle', icon: Baby, category: 'family' },
  { id: 'sister', name: 'Sister', icon: Baby, category: 'family' },
  { id: 'brother', name: 'Brother', icon: Baby, category: 'family' },
  // Hobbies
  { id: 'gaming', name: 'Gaming', icon: Gamepad2, category: 'hobbies' },
  { id: 'reading', name: 'Reading', icon: GraduationCap, category: 'hobbies' },
  { id: 'cooking', name: 'Cooking', icon: Coffee, category: 'hobbies' },
  { id: 'baking', name: 'Baking', icon: Coffee, category: 'hobbies' },
  { id: 'gardening', name: 'Gardening', icon: Mountain, category: 'hobbies' },
  { id: 'photography', name: 'Photography', icon: Mountain, category: 'hobbies' },
  { id: 'painting', name: 'Painting', icon: Mountain, category: 'hobbies' },
  { id: 'crafting', name: 'Crafting', icon: Mountain, category: 'hobbies' },
  { id: 'knitting', name: 'Knitting', icon: Mountain, category: 'hobbies' },
  { id: 'crocheting', name: 'Crocheting', icon: Mountain, category: 'hobbies' },
  { id: 'sewing', name: 'Sewing', icon: Mountain, category: 'hobbies' },
  { id: 'quilting', name: 'Quilting', icon: Mountain, category: 'hobbies' },
  { id: 'woodworking', name: 'Woodworking', icon: Mountain, category: 'hobbies' },
  { id: 'pottery', name: 'Pottery', icon: Mountain, category: 'hobbies' },
  { id: 'collecting', name: 'Collecting', icon: Mountain, category: 'hobbies' },
  { id: 'vinyl', name: 'Vinyl', icon: Gamepad2, category: 'hobbies' },
  { id: 'birding', name: 'Birding', icon: Mountain, category: 'hobbies' },
  // Music
  { id: 'guitar', name: 'Guitar', icon: Gamepad2, category: 'music' },
  { id: 'drums', name: 'Drums', icon: Gamepad2, category: 'music' },
  { id: 'piano', name: 'Piano', icon: Gamepad2, category: 'music' },
  { id: 'bass', name: 'Bass', icon: Gamepad2, category: 'music' },
  { id: 'singing', name: 'Singing', icon: Gamepad2, category: 'music' },
  { id: 'dj', name: 'DJ', icon: Gamepad2, category: 'music' },
  { id: 'metal', name: 'Metal', icon: Gamepad2, category: 'music' },
  { id: 'country', name: 'Country', icon: Gamepad2, category: 'music' },
  { id: 'hiphop', name: 'Hip Hop', icon: Gamepad2, category: 'music' },
  // Lifestyle
  { id: 'introvert', name: 'Introvert', icon: Coffee, category: 'lifestyle' },
  { id: 'sarcasm', name: 'Sarcasm', icon: Coffee, category: 'lifestyle' },
  { id: 'anxiety', name: 'Anxiety', icon: Coffee, category: 'lifestyle' },
  { id: 'truecrime', name: 'True Crime', icon: Coffee, category: 'lifestyle' },
  { id: 'astrology', name: 'Astrology', icon: Mountain, category: 'lifestyle' },
  { id: 'tarot', name: 'Tarot', icon: Mountain, category: 'lifestyle' },
  { id: 'witchy', name: 'Witchy', icon: Mountain, category: 'lifestyle' },
  { id: 'crystals', name: 'Crystals', icon: Mountain, category: 'lifestyle' },
  { id: 'minimalist', name: 'Minimalist', icon: Mountain, category: 'lifestyle' },
  { id: 'vegan', name: 'Vegan', icon: Mountain, category: 'lifestyle' },
  { id: 'keto', name: 'Keto', icon: Coffee, category: 'lifestyle' },
  // Age/Milestones
  { id: 'retirement', name: 'Retirement', icon: Coffee, category: 'milestones' },
  { id: 'vintage', name: 'Vintage', icon: Coffee, category: 'milestones' },
  { id: 'birthday', name: 'Birthday', icon: Baby, category: 'milestones' },
  // Food
  { id: 'tacos', name: 'Tacos', icon: Coffee, category: 'food' },
  { id: 'pizza', name: 'Pizza', icon: Coffee, category: 'food' },
  { id: 'bacon', name: 'Bacon', icon: Coffee, category: 'food' },
  { id: 'bbq', name: 'BBQ', icon: Coffee, category: 'food' },
  { id: 'sushi', name: 'Sushi', icon: Coffee, category: 'food' },
  { id: 'chocolate', name: 'Chocolate', icon: Coffee, category: 'food' },
  // Seasonal
  { id: 'christmas', name: 'Christmas', icon: Mountain, category: 'seasonal' },
  { id: 'halloween', name: 'Halloween', icon: Mountain, category: 'seasonal' },
  { id: 'fall', name: 'Fall', icon: Mountain, category: 'seasonal' },
  { id: 'summer', name: 'Summer', icon: Mountain, category: 'seasonal' },
  { id: 'spring', name: 'Spring', icon: Mountain, category: 'seasonal' },
  { id: 'winter', name: 'Winter', icon: Mountain, category: 'seasonal' },
  // Location
  { id: 'beach', name: 'Beach', icon: Mountain, category: 'location' },
  { id: 'mountains', name: 'Mountains', icon: Mountain, category: 'location' },
  { id: 'lake', name: 'Lake', icon: Mountain, category: 'location' },
  { id: 'texas', name: 'Texas', icon: Mountain, category: 'location' },
  { id: 'florida', name: 'Florida', icon: Mountain, category: 'location' },
  { id: 'midwest', name: 'Midwest', icon: Mountain, category: 'location' },
]

// Niche categories for grouped dropdown
const NICHE_CATEGORIES = [
  { id: 'all', name: 'All' },
  { id: 'beverages', name: 'Beverages' },
  { id: 'fitness', name: 'Fitness' },
  { id: 'sports', name: 'Sports' },
  { id: 'outdoors', name: 'Outdoors' },
  { id: 'pets', name: 'Pets' },
  { id: 'professions', name: 'Professions' },
  { id: 'family', name: 'Family' },
  { id: 'hobbies', name: 'Hobbies' },
  { id: 'music', name: 'Music' },
  { id: 'lifestyle', name: 'Lifestyle' },
  { id: 'food', name: 'Food' },
  { id: 'seasonal', name: 'Seasonal' },
  { id: 'location', name: 'Location' },
]

// Trending data is now fetched LIVE from Google Trends + Reddit

const STORAGE_KEY = 'merch_engine_ideas'
const FAVORITES_KEY = 'merch_engine_favorites'

// Helper to get competition color
const getCompetitionColor = (competition) => {
  switch (competition) {
    case 'low': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30'
    case 'medium': return 'text-amber-400 bg-amber-500/10 border-amber-500/30'
    case 'high': return 'text-red-400 bg-red-500/10 border-red-500/30'
    default: return 'text-zinc-400 bg-zinc-500/10 border-zinc-500/30'
  }
}

const getCompetitionLabel = (competition) => {
  switch (competition) {
    case 'low': return 'Low Competition'
    case 'medium': return 'Medium'
    case 'high': return 'High Competition'
    default: return 'Unknown'
  }
}

export default function Dashboard() {
  const [ideas, setIdeas] = useState([])
  const [favorites, setFavorites] = useState([])
  const [selectedNiche, setSelectedNiche] = useState('all')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [nicheInfo, setNicheInfo] = useState(null)
  const [count, setCount] = useState(200)
  const [copiedId, setCopiedId] = useState(null)
  const [selectedPhrase, setSelectedPhrase] = useState(null)
  const [variations, setVariations] = useState([])
  const [trademarkStatus, setTrademarkStatus] = useState({})
  const [viewMode, setViewMode] = useState('grid')
  const [showNicheDropdown, setShowNicheDropdown] = useState(false)
  const [searchFilter, setSearchFilter] = useState('')
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false)

  // Fetch LIVE trending data from backend (Amazon + Etsy autocomplete)
  const {
    data: trendsData,
    isLoading: trendsLoading,
    error: trendsError,
    refetch: refetchTrends
  } = useQuery({
    queryKey: ['trends'],
    queryFn: () => getAllTrends(15),
    staleTime: 1000 * 60 * 15, // 15 minutes
    refetchOnMount: true,
  })

  // Refresh mutation
  const refreshMutation = useMutation({
    mutationFn: refreshTrends,
    onSuccess: (data) => {
      refetchTrends()
    },
  })

  // Convert API response to display format
  const liveTrends = trendsData?.data?.combined?.map((t, idx) => ({
    phrase: t.trend,
    trend: t.growth || '+100%',
    platform: t.platform || 'Google',
    bsr: t.shirt_potential?.score ? Math.round(2000 - (t.shirt_potential.score * 15)) : 1000,
    category: t.category,
    isLive: t.is_live,
    source: t.source,
  })) || []

  // Export ideas to CSV
  const exportToCSV = (data, filename) => {
    const headers = ['Phrase', 'Niche', 'Score', 'Competition', 'Est. BSR', 'Discovered']
    const csvRows = [headers.join(',')]

    data.forEach(idea => {
      const row = [
        `"${idea.phrase.replace(/"/g, '""')}"`,
        idea.niche || 'general',
        idea.score || '',
        idea.competition || '',
        idea.estimated_bsr || '',
        idea.discovered_at ? new Date(idea.discovered_at).toLocaleDateString() : ''
      ]
      csvRows.push(row.join(','))
    })

    const csv = csvRows.join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${filename}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleExportIdeas = () => {
    exportToCSV(filteredIdeas, `merch-ideas-${selectedNiche}-${new Date().toISOString().slice(0,10)}`)
  }

  const handleExportFavorites = () => {
    const favIdeas = ideas.filter(i => favorites.includes(i.phrase))
    exportToCSV(favIdeas, `merch-favorites-${new Date().toISOString().slice(0,10)}`)
  }

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
      // Store niche info for competition/BSR display
      if (data.niche_info) {
        setNicheInfo(data.niche_info)
      }
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
      {/* Trending Section - LIVE MERCH DATA */}
      <div className="bg-gradient-to-r from-zinc-900 to-zinc-900/50 rounded-xl border border-zinc-800 p-5">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <TrendingUp size={18} className="text-emerald-400" />
            <h2 className="text-base font-semibold text-zinc-200">What Buyers Are Searching</h2>
            {!trendsLoading && liveTrends.length > 0 && (
              <>
                <span className="text-xs px-2 py-0.5 bg-emerald-500/20 text-emerald-400 rounded-full animate-pulse">LIVE</span>
                <span className="text-xs px-2 py-0.5 bg-purple-500/20 text-purple-400 rounded-full">{liveTrends.length} phrases</span>
              </>
            )}
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-xs text-zinc-500">
              <span className="px-2 py-1 bg-orange-500/10 text-orange-400 rounded">Amazon</span>
              <span className="px-2 py-1 bg-pink-500/10 text-pink-400 rounded">Etsy</span>
              <span className="px-2 py-1 bg-emerald-500/10 text-emerald-400 rounded">Google</span>
            </div>
            <button
              onClick={() => refreshMutation.mutate()}
              disabled={refreshMutation.isPending || trendsLoading}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 rounded-lg text-xs text-zinc-300 transition-all disabled:opacity-50"
            >
              <RefreshCw size={12} className={refreshMutation.isPending ? 'animate-spin' : ''} />
              <span>{refreshMutation.isPending ? 'Refreshing...' : 'Refresh'}</span>
            </button>
          </div>
        </div>

        {/* Loading State */}
        {trendsLoading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <Loader2 size={24} className="animate-spin text-emerald-400 mx-auto mb-3" />
              <p className="text-sm text-zinc-500">Fetching what buyers are searching for...</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {trendsError && !trendsLoading && (
          <div className="text-center py-8">
            <p className="text-red-400 text-sm mb-2">Failed to fetch trends</p>
            <button
              onClick={() => refetchTrends()}
              className="text-emerald-400 text-sm hover:underline"
            >
              Try again
            </button>
          </div>
        )}

        {/* Scrollable trending grid */}
        {!trendsLoading && liveTrends.length > 0 && (
          <div className="max-h-[320px] overflow-y-auto pr-2 custom-scrollbar">
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
              {liveTrends.sort((a, b) => parseInt(b.trend) - parseInt(a.trend)).map((item, idx) => (
                <div
                  key={idx}
                  onClick={() => handlePhraseClick(item.phrase)}
                  className={`group bg-zinc-800/50 rounded-xl p-3 hover:bg-zinc-800 transition-all cursor-pointer border border-transparent hover:border-zinc-700 ${
                    idx < 5 ? 'ring-1 ring-emerald-500/30' : ''
                  }`}
                >
                  {idx < 5 && (
                    <div className="flex items-center gap-1 mb-2">
                      <Flame size={12} className="text-orange-400" />
                      <span className="text-[10px] text-orange-400 font-medium">HOT</span>
                    </div>
                  )}
                  <p className="text-sm font-medium text-zinc-200 mb-2 line-clamp-2">{item.phrase}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1 text-xs text-emerald-400">
                      <ArrowUpRight size={12} />
                      <span className="font-medium">{item.trend}</span>
                    </div>
                    <span className={`text-xs px-1.5 py-0.5 rounded ${
                      item.platform === 'TikTok' ? 'bg-pink-500/10 text-pink-400' :
                      item.platform === 'Reddit' ? 'bg-orange-500/10 text-orange-400' :
                      item.platform === 'Twitter' ? 'bg-blue-500/10 text-blue-400' :
                      'bg-emerald-500/10 text-emerald-400'
                    }`}>{item.platform}</span>
                  </div>
                  {item.bsr && (
                    <div className="flex items-center gap-1 mt-2 text-[10px] text-zinc-500">
                      <BarChart3 size={10} />
                      <span>Potential: {item.bsr < 500 ? 'High' : item.bsr < 1000 ? 'Medium' : 'Good'}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!trendsLoading && !trendsError && liveTrends.length === 0 && (
          <div className="text-center py-8">
            <p className="text-zinc-500 text-sm mb-2">No trends available</p>
            <button
              onClick={() => refreshMutation.mutate()}
              className="text-emerald-400 text-sm hover:underline"
            >
              Fetch live trends
            </button>
          </div>
        )}

        {/* Last updated info */}
        {trendsData?.data?.fetched_at && (
          <div className="mt-3 pt-3 border-t border-zinc-800 flex items-center justify-between text-xs text-zinc-600">
            <span>Data from: Amazon & Etsy search suggestions</span>
            <span>Updated: {new Date(trendsData.data.fetched_at).toLocaleTimeString()}</span>
          </div>
        )}
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
              <div className="absolute top-full left-0 mt-2 w-72 bg-zinc-800 border border-zinc-700 rounded-xl shadow-xl z-50 py-2 max-h-[70vh] overflow-y-auto">
                {/* Category tabs */}
                <div className="flex flex-wrap gap-1 px-2 pb-2 mb-2 border-b border-zinc-700">
                  {NICHE_CATEGORIES.map((cat) => (
                    <button
                      key={cat.id}
                      onClick={() => setSelectedCategory(cat.id)}
                      className={`px-2 py-1 text-xs rounded-lg transition-all ${
                        selectedCategory === cat.id
                          ? 'bg-emerald-500/20 text-emerald-400'
                          : 'text-zinc-500 hover:text-zinc-300'
                      }`}
                    >
                      {cat.name}
                    </button>
                  ))}
                </div>

                {/* Filtered niches */}
                <div className="space-y-0.5">
                  {NICHES.filter(n =>
                    selectedCategory === 'all' ? true : n.category === selectedCategory
                  ).map((niche) => (
                    <button
                      key={niche.id}
                      onClick={() => {
                        setSelectedNiche(niche.id)
                        setShowNicheDropdown(false)
                      }}
                      className={`w-full flex items-center gap-3 px-4 py-2 text-sm hover:bg-zinc-700 transition-all ${
                        selectedNiche === niche.id ? 'text-emerald-400 bg-emerald-500/10' : 'text-zinc-300'
                      }`}
                    >
                      <niche.icon size={14} className="shrink-0" />
                      <span className="flex-1 text-left">{niche.name}</span>
                      {selectedNiche === niche.id && <Check size={14} />}
                    </button>
                  ))}
                </div>
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

          {/* Export Button */}
          {filteredIdeas.length > 0 && (
            <button
              onClick={handleExportIdeas}
              className="flex items-center gap-2 px-3 py-2.5 text-blue-400 hover:bg-blue-500/10 rounded-xl text-sm transition-all"
            >
              <Download size={16} />
              <span>Export CSV</span>
            </button>
          )}

          {/* Export Favorites */}
          {favorites.length > 0 && (
            <button
              onClick={handleExportFavorites}
              className="flex items-center gap-2 px-3 py-2.5 text-amber-400 hover:bg-amber-500/10 rounded-xl text-sm transition-all"
            >
              <Download size={16} />
              <span>Export Favorites</span>
            </button>
          )}

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

        {/* Niche Info Banner */}
        {selectedNiche !== 'all' && nicheInfo && nicheInfo[selectedNiche] && (
          <div className="mt-4 pt-4 border-t border-zinc-800 flex items-center gap-4 text-sm">
            <div className="flex items-center gap-2">
              <Target size={14} className="text-zinc-500" />
              <span className="text-zinc-400">Selected Niche:</span>
              <span className="font-medium text-zinc-200">{selectedNiche}</span>
            </div>
            <div className={`flex items-center gap-1 px-2 py-1 rounded border ${getCompetitionColor(nicheInfo[selectedNiche].competition)}`}>
              {nicheInfo[selectedNiche].competition === 'low' ? (
                <>
                  <TrendingUp size={12} />
                  <span>Low Competition - Great Opportunity!</span>
                </>
              ) : nicheInfo[selectedNiche].competition === 'high' ? (
                <>
                  <AlertTriangle size={12} />
                  <span>High Competition - Stand Out Required</span>
                </>
              ) : (
                <>
                  <Target size={12} />
                  <span>Medium Competition</span>
                </>
              )}
            </div>
            <div className="flex items-center gap-1 text-zinc-500">
              <BarChart3 size={12} />
              <span>Avg BSR: {nicheInfo[selectedNiche].avg_bsr?.toLocaleString()}</span>
            </div>
          </div>
        )}
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
                    <div className="flex items-center justify-between gap-2 flex-wrap">
                      <span className="text-xs px-2 py-1 bg-zinc-800 text-zinc-400 rounded-lg">
                        {idea.niche}
                      </span>
                      <div className="flex items-center gap-2">
                        {idea.competition && (
                          <span className={`text-xs px-2 py-0.5 rounded border ${getCompetitionColor(idea.competition)}`}>
                            {idea.competition === 'low' ? '🟢' : idea.competition === 'medium' ? '🟡' : '🔴'}
                          </span>
                        )}
                        {idea.estimated_bsr && (
                          <span className="text-xs text-zinc-500 flex items-center gap-1">
                            <BarChart3 size={10} />
                            {idea.estimated_bsr > 1000 ? `${Math.round(idea.estimated_bsr/1000)}k` : idea.estimated_bsr}
                          </span>
                        )}
                        {idea.score >= 60 && (
                          <div className={`flex items-center gap-1 text-xs ${getScoreColor(idea.score)}`}>
                            <Flame size={12} />
                          </div>
                        )}
                      </div>
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
                    <div className="flex items-center gap-4 flex-1 min-w-0">
                      <button
                        onClick={(e) => handleToggleFavorite(idea.phrase, e)}
                        className="p-1 hover:bg-zinc-700 rounded transition-all shrink-0"
                      >
                        <Star
                          size={14}
                          className={isFavorite ? 'text-amber-400' : 'text-zinc-600'}
                          fill={isFavorite ? 'currentColor' : 'none'}
                        />
                      </button>
                      <span className="text-xs text-zinc-600 w-6 shrink-0">{idx + 1}</span>
                      <p className="text-sm font-medium text-zinc-200 truncate">{idea.phrase}</p>
                      <span className="text-xs px-2 py-1 bg-zinc-800 text-zinc-400 rounded-lg shrink-0">
                        {idea.niche}
                      </span>
                      {idea.competition && (
                        <span className={`text-xs px-2 py-0.5 rounded border shrink-0 ${getCompetitionColor(idea.competition)}`}>
                          {idea.competition === 'low' ? '🟢 Low' : idea.competition === 'medium' ? '🟡 Med' : '🔴 High'}
                        </span>
                      )}
                      {idea.estimated_bsr && (
                        <span className="text-xs text-zinc-500 flex items-center gap-1 shrink-0">
                          <BarChart3 size={10} />
                          {idea.estimated_bsr > 1000 ? `${Math.round(idea.estimated_bsr/1000)}k` : idea.estimated_bsr}
                        </span>
                      )}
                      {idea.score >= 60 && (
                        <div className={`flex items-center gap-1 text-xs shrink-0 ${getScoreColor(idea.score)}`}>
                          <Flame size={12} />
                        </div>
                      )}
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleCopy(idea.phrase, idx)
                      }}
                      className="opacity-0 group-hover:opacity-100 p-2 hover:bg-zinc-700 rounded-lg transition-all shrink-0"
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
