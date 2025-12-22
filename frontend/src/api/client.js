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

export default client
