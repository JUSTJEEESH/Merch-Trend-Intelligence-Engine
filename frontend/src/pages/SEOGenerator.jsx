import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { generateSEO, validateListing, getForbiddenWords } from '../api/client'
import Loading from '../components/Loading'

export default function SEOGenerator() {
  const [phrase, setPhrase] = useState('')
  const [niche, setNiche] = useState('')
  const [tone, setTone] = useState('neutral')
  const [result, setResult] = useState(null)
  const [generating, setGenerating] = useState(false)

  const [customTitle, setCustomTitle] = useState('')
  const [validationResult, setValidationResult] = useState(null)

  const { data: forbidden } = useQuery({
    queryKey: ['forbiddenWords'],
    queryFn: getForbiddenWords,
  })

  const handleGenerate = async () => {
    if (!phrase.trim()) return
    setGenerating(true)
    try {
      const res = await generateSEO({ phrase, niche: niche || undefined, tone })
      setResult(res)
    } catch (error) {
      console.error('Generation failed:', error)
    }
    setGenerating(false)
  }

  const handleValidate = async () => {
    if (!customTitle.trim()) return
    try {
      const res = await validateListing({ title: customTitle })
      setValidationResult(res)
    } catch (error) {
      console.error('Validation failed:', error)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">SEO Generator</h1>
        <p className="text-gray-500 mt-1">Generate Amazon Merch-compliant listing content</p>
      </div>

      {/* Generator Form */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Generate Listing Content</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Phrase</label>
            <input
              type="text"
              className="input"
              placeholder="Enter your phrase..."
              value={phrase}
              onChange={(e) => setPhrase(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Niche (optional)</label>
            <select
              className="input"
              value={niche}
              onChange={(e) => setNiche(e.target.value)}
            >
              <option value="">General</option>
              <option value="fitness">Fitness</option>
              <option value="coffee">Coffee</option>
              <option value="dogs">Dogs</option>
              <option value="cats">Cats</option>
              <option value="nursing">Nursing</option>
              <option value="teaching">Teaching</option>
              <option value="gaming">Gaming</option>
              <option value="fishing">Fishing</option>
              <option value="parenting">Parenting</option>
              <option value="programming">Programming</option>
            </select>
          </div>
        </div>

        <div className="flex gap-4 items-end">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tone</label>
            <select
              className="input"
              value={tone}
              onChange={(e) => setTone(e.target.value)}
            >
              <option value="neutral">Neutral</option>
              <option value="funny">Funny</option>
              <option value="sarcastic">Sarcastic</option>
              <option value="proud">Proud</option>
            </select>
          </div>

          <button
            className="btn btn-primary"
            onClick={handleGenerate}
            disabled={generating || !phrase.trim()}
          >
            {generating ? 'Generating...' : 'Generate SEO Content'}
          </button>
        </div>
      </div>

      {/* Generated Result */}
      {result && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Generated Listing</h2>
            <span className={`badge ${result.is_compliant ? 'badge-success' : 'badge-warning'}`}>
              {result.is_compliant ? 'Compliant' : 'Review Required'}
            </span>
          </div>

          {result.warnings?.length > 0 && (
            <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="font-medium text-yellow-800 mb-1">Warnings:</p>
              <ul className="list-disc list-inside text-yellow-700 text-sm">
                {result.warnings.map((w, i) => <li key={i}>{w}</li>)}
              </ul>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-sm font-medium text-gray-700">Title (max 80 chars)</label>
                <span className="text-xs text-gray-500">{result.title?.length || 0}/80</span>
              </div>
              <div className="flex gap-2">
                <input
                  type="text"
                  className="input flex-1"
                  value={result.title}
                  readOnly
                />
                <button
                  className="btn btn-secondary text-sm"
                  onClick={() => copyToClipboard(result.title)}
                >
                  Copy
                </button>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-sm font-medium text-gray-700">Bullet 1 (max 256 chars)</label>
                <span className="text-xs text-gray-500">{result.bullet_1?.length || 0}/256</span>
              </div>
              <div className="flex gap-2">
                <input
                  type="text"
                  className="input flex-1"
                  value={result.bullet_1}
                  readOnly
                />
                <button
                  className="btn btn-secondary text-sm"
                  onClick={() => copyToClipboard(result.bullet_1)}
                >
                  Copy
                </button>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-sm font-medium text-gray-700">Bullet 2 (max 256 chars)</label>
                <span className="text-xs text-gray-500">{result.bullet_2?.length || 0}/256</span>
              </div>
              <div className="flex gap-2">
                <input
                  type="text"
                  className="input flex-1"
                  value={result.bullet_2}
                  readOnly
                />
                <button
                  className="btn btn-secondary text-sm"
                  onClick={() => copyToClipboard(result.bullet_2)}
                >
                  Copy
                </button>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-sm font-medium text-gray-700">Description (max 2000 chars)</label>
                <span className="text-xs text-gray-500">{result.description?.length || 0}/2000</span>
              </div>
              <div className="flex gap-2">
                <textarea
                  className="input flex-1"
                  rows={4}
                  value={result.description}
                  readOnly
                />
                <button
                  className="btn btn-secondary text-sm self-start"
                  onClick={() => copyToClipboard(result.description)}
                >
                  Copy
                </button>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-sm font-medium text-gray-700">Backend Keywords (max 250 chars)</label>
                <span className="text-xs text-gray-500">{result.backend_keywords?.length || 0}/250</span>
              </div>
              <div className="flex gap-2">
                <input
                  type="text"
                  className="input flex-1 font-mono text-sm"
                  value={result.backend_keywords}
                  readOnly
                />
                <button
                  className="btn btn-secondary text-sm"
                  onClick={() => copyToClipboard(result.backend_keywords)}
                >
                  Copy
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Validator */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Validate Custom Title</h2>
          <div className="space-y-4">
            <input
              type="text"
              className="input"
              placeholder="Enter a title to validate..."
              value={customTitle}
              onChange={(e) => setCustomTitle(e.target.value)}
            />
            <button
              className="btn btn-secondary"
              onClick={handleValidate}
            >
              Validate
            </button>

            {validationResult && (
              <div className={`p-3 rounded-lg ${
                validationResult.is_compliant ? 'bg-green-50' : 'bg-red-50'
              }`}>
                <p className={`font-medium ${
                  validationResult.is_compliant ? 'text-green-800' : 'text-red-800'
                }`}>
                  {validationResult.is_compliant ? '✅ Title is compliant' : '❌ Issues found'}
                </p>
                {validationResult.issues?.length > 0 && (
                  <ul className="list-disc list-inside text-red-700 text-sm mt-2">
                    {validationResult.issues.map((issue, i) => (
                      <li key={i}>{issue}</li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Forbidden Words */}
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Forbidden Words</h2>
          {forbidden ? (
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Product Words (not allowed in titles)</p>
                <div className="flex flex-wrap gap-1">
                  {forbidden.restricted_product_words?.map((word, i) => (
                    <span key={i} className="badge badge-danger">{word}</span>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700 mb-2">Forbidden Terms</p>
                <div className="flex flex-wrap gap-1 max-h-40 overflow-y-auto">
                  {forbidden.forbidden?.slice(0, 30).map((word, i) => (
                    <span key={i} className="badge bg-gray-100 text-gray-700">{word}</span>
                  ))}
                  {forbidden.forbidden?.length > 30 && (
                    <span className="text-gray-500 text-sm">+{forbidden.forbidden.length - 30} more</span>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <Loading text="Loading..." />
          )}
        </div>
      </div>
    </div>
  )
}
