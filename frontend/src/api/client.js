import axios from 'axios'

const API_BASE_URL = '/api'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Dashboard
export const getStats = () => client.get('/stats').then(res => res.data)
export const getActivity = (limit = 20) => client.get(`/activity?limit=${limit}`).then(res => res.data)

// Phrases
export const getPhrases = (params) => client.get('/phrases', { params }).then(res => res.data)
export const getPhrase = (id) => client.get(`/phrases/${id}`).then(res => res.data)
export const getTrendingPhrases = (limit = 20, niche = null) => {
  const params = { limit }
  if (niche) params.niche = niche
  return client.get('/phrases/trending', { params }).then(res => res.data)
}
export const getEmergingPhrases = (limit = 20, days = 7) =>
  client.get(`/phrases/emerging?limit=${limit}&days=${days}`).then(res => res.data)
export const getNiches = () => client.get('/phrases/niches').then(res => res.data)
export const analyzePhrase = (text) => client.post(`/phrases/analyze?text=${encodeURIComponent(text)}`).then(res => res.data)
export const generateVariations = (data) => client.post('/phrases/variations', data).then(res => res.data)
export const getPhraseHistory = (id, days = 30) =>
  client.get(`/phrases/${id}/history?days=${days}`).then(res => res.data)

// Patterns
export const getPatterns = (limit = 50) => client.get(`/patterns?limit=${limit}`).then(res => res.data)
export const getPopularPatterns = (limit = 10) => client.get(`/patterns/popular?limit=${limit}`).then(res => res.data)
export const getPatternPhrases = (id, limit = 20) =>
  client.get(`/patterns/${id}/phrases?limit=${limit}`).then(res => res.data)
export const generateFromPattern = (patternId, variables) =>
  client.post(`/patterns/generate?pattern_id=${patternId}`, variables).then(res => res.data)

// Trademarks
export const getTrademarks = (params) => client.get('/trademarks', { params }).then(res => res.data)
export const checkTrademark = (phrase) => client.post('/trademarks/check', { phrase }).then(res => res.data)
export const checkTrademarkBatch = (phrases) => client.post('/trademarks/check-batch', phrases).then(res => res.data)
export const getBlockedTerms = () => client.get('/trademarks/blocked').then(res => res.data)
export const addBlockedTerm = (term, reason) =>
  client.post(`/trademarks/blocked?term=${encodeURIComponent(term)}&reason=${encodeURIComponent(reason)}`).then(res => res.data)

// SEO
export const generateSEO = (data) => client.post('/seo/generate', data).then(res => res.data)
export const generateSEOBatch = (phrases, niche, tone) =>
  client.post(`/seo/generate-batch?niche=${niche}&tone=${tone}`, phrases).then(res => res.data)
export const validateListing = (params) => client.post('/seo/validate', null, { params }).then(res => res.data)
export const getForbiddenWords = () => client.get('/seo/forbidden-words').then(res => res.data)

// Scraping
export const startScrape = (data) => client.post('/scrape/start', data).then(res => res.data)
export const getScrapeStatus = (logId) => client.get(`/scrape/status/${logId}`).then(res => res.data)
export const getSources = () => client.get('/scrape/sources').then(res => res.data)
export const getScrapingLogs = (limit = 50) => client.get(`/scrape/logs?limit=${limit}`).then(res => res.data)
export const scrapeReddit = (subreddit, limit = 100) =>
  client.post(`/scrape/reddit?subreddit=${subreddit}&limit=${limit}`).then(res => res.data)
export const scrapeGoogleTrends = (keyword) =>
  client.post(`/scrape/google-trends${keyword ? `?keyword=${encodeURIComponent(keyword)}` : ''}`).then(res => res.data)

// Export
export const exportPhrases = (data) => client.post('/export/phrases', data).then(res => res.data)
export const exportSEO = (phraseIds, format) =>
  client.post(`/export/seo?format=${format}`, phraseIds).then(res => res.data)
export const getExportFiles = () => client.get('/export/files').then(res => res.data)
export const downloadExport = (filename) => `${API_BASE_URL}/export/download/${filename}`
export const deleteExportFile = (filename) => client.delete(`/export/files/${filename}`).then(res => res.data)

// Ideas - Bulk Generation
export const generateIdeas = (params = {}) => {
  const queryParams = new URLSearchParams()
  if (params.count) queryParams.append('count', params.count)
  if (params.niches) queryParams.append('niches', params.niches)
  if (params.creativity) queryParams.append('creativity', params.creativity)
  if (params.include_classics !== undefined) queryParams.append('include_classics', params.include_classics)
  if (params.include_generated !== undefined) queryParams.append('include_generated', params.include_generated)
  if (params.include_variations !== undefined) queryParams.append('include_variations', params.include_variations)
  return client.post(`/ideas/generate?${queryParams.toString()}`).then(res => res.data)
}
export const quickGenerateIdeas = (topic, count = 50) =>
  client.post('/ideas/quick', { topic, count }).then(res => res.data)
export const getBestsellers = (niche = null, limit = 100) => {
  const params = { limit }
  if (niche) params.niche = niche
  return client.get('/ideas/bestsellers', { params }).then(res => res.data)
}
export const getAvailableNiches = () => client.get('/ideas/niches').then(res => res.data)
export const getTemplates = (limit = 50) => client.get(`/ideas/templates?limit=${limit}`).then(res => res.data)
export const getTopics = () => client.get('/ideas/topics').then(res => res.data)

// ============ ADVANCED TOOLS API ============

// Social Trending
export const getAllTrends = (limit = 15) =>
  client.get(`/tools/trending/all?limit_per_platform=${limit}`).then(res => res.data)
export const getTikTokTrends = (limit = 25) =>
  client.get(`/tools/trending/tiktok?limit=${limit}`).then(res => res.data)
export const getTwitterTrends = (limit = 20) =>
  client.get(`/tools/trending/twitter?limit=${limit}`).then(res => res.data)
export const getRedditTrends = (limit = 10) =>
  client.get(`/tools/trending/reddit?limit=${limit}`).then(res => res.data)
export const getTrendingForNiche = (niche) =>
  client.get(`/tools/trending/niche/${niche}`).then(res => res.data)
export const refreshTrends = () =>
  client.post('/tools/trending/refresh').then(res => res.data)

// Seasonal Calendar
export const getUpcomingEvents = (days = 90) =>
  client.get(`/tools/calendar/upcoming?days=${days}`).then(res => res.data)
export const getCalendarOverview = () =>
  client.get('/tools/calendar/overview').then(res => res.data)
export const getEventsForNiche = (niche) =>
  client.get(`/tools/calendar/niche/${niche}`).then(res => res.data)
export const getEventPhrases = (eventName) =>
  client.get(`/tools/calendar/event/${encodeURIComponent(eventName)}/phrases`).then(res => res.data)

// AI Phrase Generator
export const generateAIPhrases = (topic, tone = 'funny', count = 20) =>
  client.post('/tools/ai/generate', { topic, tone, count }).then(res => res.data)
export const generateBulkPhrases = (topic, countPerTone = 10) =>
  client.post(`/tools/ai/generate-bulk?topic=${topic}&count_per_tone=${countPerTone}`).then(res => res.data)
export const getAvailableTones = () =>
  client.get('/tools/ai/tones').then(res => res.data)
export const suggestTonesForTopic = (topic) =>
  client.get(`/tools/ai/suggest-tones/${topic}`).then(res => res.data)

// BSR Tracker
export const estimateSalesFromBSR = (bsr) =>
  client.get(`/tools/bsr/estimate/${bsr}`).then(res => res.data)
export const getNicheBSRData = (niche) =>
  client.get(`/tools/bsr/niche/${niche}`).then(res => res.data)
export const getBSRHistory = (keyword, days = 30) =>
  client.get(`/tools/bsr/history/${keyword}?days=${days}`).then(res => res.data)
export const getBSROpportunities = () =>
  client.get('/tools/bsr/opportunities').then(res => res.data)

// Profitability Calculator
export const calculateNicheProfitability = (niche) =>
  client.get(`/tools/profitability/niche/${niche}`).then(res => res.data)
export const getBestNiches = (count = 10) =>
  client.get(`/tools/profitability/best-niches?count=${count}`).then(res => res.data)
export const compareNiches = (niches) =>
  client.post('/tools/profitability/compare', niches).then(res => res.data)
export const calculateRevenueProjection = (monthlySales, product = 'standard_tee', months = 12) =>
  client.get(`/tools/profitability/projection?monthly_sales=${monthlySales}&product=${product}&months=${months}`).then(res => res.data)
export const calculateDesignROI = (data) =>
  client.post('/tools/profitability/roi', data).then(res => res.data)
export const calculatePortfolioMetrics = (designsCount, avgSales, product = 'standard_tee') =>
  client.post('/tools/profitability/portfolio', { designs_count: designsCount, avg_sales_per_design: avgSales, product }).then(res => res.data)

// Design Generator
export const generateDesignConcept = (phrase, style = 'funny') =>
  client.post('/tools/design/concept', { phrase, style }).then(res => res.data)
export const getMultipleDesignConcepts = (phrase, count = 3) =>
  client.get(`/tools/design/concepts/${encodeURIComponent(phrase)}?count=${count}`).then(res => res.data)
export const getColorPalettesForNiche = (niche) =>
  client.get(`/tools/design/colors/${niche}`).then(res => res.data)

// Listing Optimizer
export const generateOptimizedListing = (phrase, niche = 'general', product = 'T-Shirt', tone = 'funny') =>
  client.post('/tools/listing/optimize', { phrase, niche, product, tone }).then(res => res.data)
export const generateOptimizedTitle = (phrase, niche = 'general', product = 'T-Shirt', tone = 'funny') =>
  client.post('/tools/listing/title', { phrase, niche, product, tone }).then(res => res.data)
export const generateBackendKeywords = (phrase, niche = 'general') =>
  client.post(`/tools/listing/keywords?phrase=${encodeURIComponent(phrase)}&niche=${niche}`).then(res => res.data)

export default client
