import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getPhrase, getPhraseHistory, generateVariations, generateSEO } from '../api/client'
import TrendChart from '../components/TrendChart'
import Loading from '../components/Loading'
import { useState } from 'react'

export default function PhraseDetail() {
  const { id } = useParams()
  const [variations, setVariations] = useState(null)
  const [seoContent, setSeoContent] = useState(null)
  const [loadingVariations, setLoadingVariations] = useState(false)
  const [loadingSEO, setLoadingSEO] = useState(false)

  const { data: phrase, isLoading } = useQuery({
    queryKey: ['phrase', id],
    queryFn: () => getPhrase(id),
  })

  const { data: history } = useQuery({
    queryKey: ['phraseHistory', id],
    queryFn: () => getPhraseHistory(id, 30),
    enabled: !!id,
  })

  const handleGenerateVariations = async () => {
    setLoadingVariations(true)
    try {
      const result = await generateVariations({
        phrase: phrase.text,
        variation_type: 'all',
        count: 10
      })
      setVariations(result)
    } catch (error) {
      console.error('Failed to generate variations:', error)
    }
    setLoadingVariations(false)
  }

  const handleGenerateSEO = async () => {
    setLoadingSEO(true)
    try {
      const result = await generateSEO({
        phrase: phrase.text,
        niche: phrase.niche,
        tone: 'neutral'
      })
      setSeoContent(result)
    } catch (error) {
      console.error('Failed to generate SEO:', error)
    }
    setLoadingSEO(false)
  }

  if (isLoading) return <Loading />
  if (!phrase) return <div>Phrase not found</div>

  return (
    <div className="space-y-8">
      <div className="flex items-start justify-between">
        <div>
          <Link to="/phrases" className="text-primary-600 hover:text-primary-700 text-sm mb-2 inline-block">
            ← Back to Phrases
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">"{phrase.text}"</h1>
          <div className="flex gap-2 mt-3">
            <span className={`badge ${phrase.is_safe ? 'badge-success' : 'badge-danger'}`}>
              {phrase.is_safe ? 'Safe' : 'Risky'}
            </span>
            {phrase.niche && (
              <span className="badge bg-gray-100 text-gray-700">{phrase.niche}</span>
            )}
            {phrase.is_pattern && (
              <span className="badge bg-purple-100 text-purple-700">Pattern</span>
            )}
          </div>
        </div>

        <div className="text-right">
          <div className="text-4xl font-bold text-primary-600">{phrase.trend_score.toFixed(0)}</div>
          <div className="text-sm text-gray-500">Trend Score</div>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card">
          <p className="text-sm text-gray-500">Frequency</p>
          <p className="text-2xl font-bold">{phrase.frequency}</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-500">Risk Score</p>
          <p className={`text-2xl font-bold ${phrase.risk_score < 30 ? 'text-green-600' : phrase.risk_score < 70 ? 'text-yellow-600' : 'text-red-600'}`}>
            {phrase.risk_score.toFixed(0)}
          </p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-500">Word Count</p>
          <p className="text-2xl font-bold">{phrase.word_count}</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-500">First Seen</p>
          <p className="text-lg font-medium">{new Date(phrase.first_seen).toLocaleDateString()}</p>
        </div>
      </div>

      {/* Pattern Info */}
      {phrase.is_pattern && phrase.pattern_template && (
        <div className="card bg-purple-50 border-purple-200">
          <h3 className="font-medium text-purple-800 mb-2">Pattern Template</h3>
          <p className="text-purple-900 font-mono">{phrase.pattern_template}</p>
        </div>
      )}

      {/* Trend History */}
      {history?.history?.length > 0 && (
        <TrendChart data={history.history} title="Trend History (30 days)" />
      )}

      {/* Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Variations */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Phrase Variations</h3>
            <button
              className="btn btn-primary text-sm"
              onClick={handleGenerateVariations}
              disabled={loadingVariations}
            >
              {loadingVariations ? 'Generating...' : 'Generate'}
            </button>
          </div>

          {variations ? (
            <div className="space-y-3">
              {variations.variations?.map((v, idx) => (
                <div key={idx} className="p-3 bg-gray-50 rounded-lg">
                  <p className="font-medium">{v.text}</p>
                  <div className="flex gap-2 mt-2">
                    <span className="badge bg-gray-200 text-gray-700">{v.type}</span>
                    <span className={`badge ${v.is_safe ? 'badge-success' : 'badge-danger'}`}>
                      {v.is_safe ? 'Safe' : 'Check Required'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">Click Generate to create phrase variations</p>
          )}
        </div>

        {/* SEO Content */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">SEO Listing</h3>
            <button
              className="btn btn-primary text-sm"
              onClick={handleGenerateSEO}
              disabled={loadingSEO || !phrase.is_safe}
            >
              {loadingSEO ? 'Generating...' : 'Generate SEO'}
            </button>
          </div>

          {!phrase.is_safe ? (
            <p className="text-yellow-600">SEO generation not available for risky phrases</p>
          ) : seoContent ? (
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700">Title</label>
                <p className="mt-1 p-2 bg-gray-50 rounded">{seoContent.title}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Bullet 1</label>
                <p className="mt-1 p-2 bg-gray-50 rounded">{seoContent.bullet_1}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Bullet 2</label>
                <p className="mt-1 p-2 bg-gray-50 rounded">{seoContent.bullet_2}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Description</label>
                <p className="mt-1 p-2 bg-gray-50 rounded text-sm">{seoContent.description}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Backend Keywords</label>
                <p className="mt-1 p-2 bg-gray-50 rounded text-sm font-mono">{seoContent.backend_keywords}</p>
              </div>
              <span className={`badge ${seoContent.is_compliant ? 'badge-success' : 'badge-warning'}`}>
                {seoContent.is_compliant ? 'Compliant' : 'Review Required'}
              </span>
            </div>
          ) : (
            <p className="text-gray-500">Click Generate to create Amazon Merch listing content</p>
          )}
        </div>
      </div>
    </div>
  )
}
