import { useState } from 'react'
import { generateSEO } from '../api/client'
import {
  FileText,
  Loader2,
  Copy,
  Check,
  Sparkles,
  CheckCircle,
  AlertCircle,
} from 'lucide-react'

const NICHES = [
  { value: '', label: 'General' },
  { value: 'fitness', label: 'Fitness' },
  { value: 'coffee', label: 'Coffee' },
  { value: 'dogs', label: 'Dogs' },
  { value: 'cats', label: 'Cats' },
  { value: 'nursing', label: 'Nursing' },
  { value: 'teaching', label: 'Teaching' },
  { value: 'gaming', label: 'Gaming' },
  { value: 'fishing', label: 'Fishing' },
  { value: 'parenting', label: 'Parenting' },
]

const TONES = [
  { value: 'neutral', label: 'Neutral' },
  { value: 'funny', label: 'Funny' },
  { value: 'sarcastic', label: 'Sarcastic' },
  { value: 'proud', label: 'Proud' },
]

export default function SEOGenerator() {
  const [phrase, setPhrase] = useState('')
  const [niche, setNiche] = useState('')
  const [tone, setTone] = useState('neutral')
  const [result, setResult] = useState(null)
  const [generating, setGenerating] = useState(false)
  const [copiedField, setCopiedField] = useState(null)

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

  const copyToClipboard = (text, field) => {
    navigator.clipboard.writeText(text)
    setCopiedField(field)
    setTimeout(() => setCopiedField(null), 1500)
  }

  const Field = ({ label, value, maxLength, field, multiline = false }) => (
    <div>
      <div className="flex items-center justify-between mb-2">
        <label className="text-sm font-medium text-zinc-400">{label}</label>
        <span className={`text-xs ${
          value?.length > maxLength ? 'text-red-400' : 'text-zinc-600'
        }`}>
          {value?.length || 0}/{maxLength}
        </span>
      </div>
      <div className="flex gap-2">
        {multiline ? (
          <textarea
            className="input flex-1 resize-none"
            rows={3}
            value={value || ''}
            readOnly
          />
        ) : (
          <input
            type="text"
            className="input flex-1"
            value={value || ''}
            readOnly
          />
        )}
        <button
          className="btn btn-secondary shrink-0"
          onClick={() => copyToClipboard(value, field)}
        >
          {copiedField === field ? (
            <Check size={16} className="text-emerald-400" />
          ) : (
            <Copy size={16} />
          )}
        </button>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-zinc-100">SEO Builder</h1>
        <p className="text-zinc-500 text-sm mt-1">Generate Amazon Merch-compliant listing content</p>
      </div>

      {/* Generator Form */}
      <div className="bg-zinc-900 rounded-xl border border-zinc-800 p-5">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles size={18} className="text-blue-400" />
          <h2 className="text-base font-semibold text-zinc-200">Generate Listing</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-zinc-400 mb-2">Phrase</label>
            <input
              type="text"
              className="input"
              placeholder="Enter your phrase..."
              value={phrase}
              onChange={(e) => setPhrase(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-400 mb-2">Niche</label>
            <select
              className="input"
              value={niche}
              onChange={(e) => setNiche(e.target.value)}
            >
              {NICHES.map(n => (
                <option key={n.value} value={n.value}>{n.label}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-400 mb-2">Tone</label>
            <select
              className="input"
              value={tone}
              onChange={(e) => setTone(e.target.value)}
            >
              {TONES.map(t => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </select>
          </div>
        </div>

        <button
          className="btn btn-primary"
          onClick={handleGenerate}
          disabled={generating || !phrase.trim()}
        >
          {generating ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              <span>Generating...</span>
            </>
          ) : (
            <>
              <FileText size={18} />
              <span>Generate SEO Content</span>
            </>
          )}
        </button>
      </div>

      {/* Generated Result */}
      {result && (
        <div className="bg-zinc-900 rounded-xl border border-zinc-800 p-5">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <FileText size={18} className="text-blue-400" />
              <h2 className="text-base font-semibold text-zinc-200">Generated Listing</h2>
            </div>
            <div className={`flex items-center gap-2 text-sm ${
              result.is_compliant ? 'text-emerald-400' : 'text-amber-400'
            }`}>
              {result.is_compliant ? (
                <>
                  <CheckCircle size={16} />
                  <span>Compliant</span>
                </>
              ) : (
                <>
                  <AlertCircle size={16} />
                  <span>Review Required</span>
                </>
              )}
            </div>
          </div>

          {result.warnings?.length > 0 && (
            <div className="mb-6 p-4 bg-amber-500/10 border border-amber-500/30 rounded-xl">
              <p className="text-sm font-medium text-amber-400 mb-2">Warnings:</p>
              <ul className="text-sm text-amber-300 space-y-1">
                {result.warnings.map((w, i) => <li key={i}>- {w}</li>)}
              </ul>
            </div>
          )}

          <div className="space-y-4">
            <Field label="Title" value={result.title} maxLength={80} field="title" />
            <Field label="Bullet 1" value={result.bullet_1} maxLength={256} field="bullet1" />
            <Field label="Bullet 2" value={result.bullet_2} maxLength={256} field="bullet2" />
            <Field label="Description" value={result.description} maxLength={2000} field="description" multiline />
            <Field label="Backend Keywords" value={result.backend_keywords} maxLength={250} field="keywords" />
          </div>

          {/* Copy All Button */}
          <div className="mt-6 pt-4 border-t border-zinc-800">
            <button
              className="btn btn-secondary"
              onClick={() => {
                const all = `Title: ${result.title}\n\nBullet 1: ${result.bullet_1}\n\nBullet 2: ${result.bullet_2}\n\nDescription: ${result.description}\n\nKeywords: ${result.backend_keywords}`
                copyToClipboard(all, 'all')
              }}
            >
              {copiedField === 'all' ? (
                <>
                  <Check size={16} className="text-emerald-400" />
                  <span className="text-emerald-400">Copied All!</span>
                </>
              ) : (
                <>
                  <Copy size={16} />
                  <span>Copy All Fields</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!result && !generating && (
        <div className="text-center py-16">
          <div className="w-16 h-16 bg-zinc-900 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-zinc-800">
            <FileText size={28} className="text-zinc-600" />
          </div>
          <h3 className="text-base font-medium text-zinc-300 mb-2">No listing generated yet</h3>
          <p className="text-zinc-500 text-sm">Enter a phrase above and click generate</p>
        </div>
      )}
    </div>
  )
}
