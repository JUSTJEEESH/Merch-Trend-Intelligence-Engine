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
  AlertTriangle,
  Info,
} from 'lucide-react'

// Niches matching backend vocabulary
const NICHES = [
  { value: '', label: 'General' },
  { value: 'coffee', label: '☕ Coffee' },
  { value: 'dogs', label: '🐕 Dogs' },
  { value: 'cats', label: '🐱 Cats' },
  { value: 'fitness', label: '💪 Fitness' },
  { value: 'nursing', label: '👩‍⚕️ Nursing' },
  { value: 'teaching', label: '📚 Teaching' },
  { value: 'mom', label: '👩 Mom' },
  { value: 'dad', label: '👨 Dad' },
  { value: 'gaming', label: '🎮 Gaming' },
  { value: 'fishing', label: '🎣 Fishing' },
  { value: 'hunting', label: '🦌 Hunting' },
  { value: 'beer', label: '🍺 Beer' },
  { value: 'wine', label: '🍷 Wine' },
  { value: 'anxiety', label: '💙 Anxiety/Mental Health' },
  { value: 'introvert', label: '📖 Introvert' },
  { value: 'sarcasm', label: '😏 Sarcasm' },
]

// Styles matching backend DESIGN_STYLES
const STYLES = [
  { value: 'funny', label: 'Funny' },
  { value: 'sarcastic', label: 'Sarcastic' },
  { value: 'motivational', label: 'Motivational' },
  { value: 'cute', label: 'Cute' },
  { value: 'vintage', label: 'Vintage' },
  { value: 'bold', label: 'Bold' },
  { value: 'minimal', label: 'Minimal' },
]

// Amazon's exact character limits
const LIMITS = {
  title: 60,
  brand: 50,
  bullet_1: 256,
  bullet_2: 256,
  description_min: 75,
  description_max: 2000,
  keywords: 250,
}

export default function SEOGenerator() {
  const [phrase, setPhrase] = useState('')
  const [niche, setNiche] = useState('')
  const [style, setStyle] = useState('funny')
  const [result, setResult] = useState(null)
  const [generating, setGenerating] = useState(false)
  const [copiedField, setCopiedField] = useState(null)

  const handleGenerate = async () => {
    if (!phrase.trim()) return
    setGenerating(true)
    try {
      const res = await generateSEO({ phrase, niche: niche || undefined, tone: style })
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

  // Field component with character count and compliance indicator
  const Field = ({ label, field, limit, isBytes = false, minLength = 0, multiline = false }) => {
    if (!result || !result[field]) return null

    const data = result[field]
    const text = data.text || ''
    const length = isBytes ? data.byte_count : data.length
    const displayLimit = isBytes ? data.limit : limit
    const isCompliant = data.compliant

    // For description, show min-max range
    const isDescription = field === 'description'
    const lengthDisplay = isDescription
      ? `${length} (min ${LIMITS.description_min})`
      : `${length}/${displayLimit}`

    return (
      <div className="bg-zinc-800/50 rounded-xl p-4 border border-zinc-700/50">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <label className="text-sm font-semibold text-zinc-200">{label}</label>
            {isCompliant ? (
              <CheckCircle size={14} className="text-emerald-400" />
            ) : (
              <AlertCircle size={14} className="text-red-400" />
            )}
          </div>
          <span className={`text-xs font-mono px-2 py-0.5 rounded ${
            isCompliant ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'
          }`}>
            {lengthDisplay}{isBytes ? ' bytes' : ' chars'}
          </span>
        </div>
        <div className="flex gap-2">
          {multiline ? (
            <textarea
              className="input flex-1 resize-none bg-zinc-900 border-zinc-700 text-sm"
              rows={5}
              value={text}
              readOnly
            />
          ) : (
            <input
              type="text"
              className="input flex-1 bg-zinc-900 border-zinc-700 text-sm"
              value={text}
              readOnly
            />
          )}
          <button
            className="btn btn-secondary shrink-0 h-fit"
            onClick={() => copyToClipboard(text, field)}
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
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-zinc-100">SEO Builder</h1>
        <p className="text-zinc-500 text-sm mt-1">Generate Amazon Merch-compliant listing content</p>
      </div>

      {/* Amazon TOS Notice */}
      <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
        <div className="flex items-start gap-3">
          <Info size={18} className="text-blue-400 mt-0.5 shrink-0" />
          <div className="text-sm">
            <p className="font-medium text-blue-300 mb-1">Amazon TOS Compliant</p>
            <p className="text-blue-200/70">
              Generated content describes the <strong>design only</strong> — no promotional language,
              suggested uses, product quality claims, or special effects claims.
            </p>
          </div>
        </div>
      </div>

      {/* Generator Form */}
      <div className="bg-zinc-900 rounded-xl border border-zinc-800 p-5">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles size={18} className="text-blue-400" />
          <h2 className="text-base font-semibold text-zinc-200">Generate Listing</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-zinc-400 mb-2">
              Design Phrase <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              className="input"
              placeholder="e.g., But First, Coffee"
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
            <label className="block text-sm font-medium text-zinc-400 mb-2">Style</label>
            <select
              className="input"
              value={style}
              onChange={(e) => setStyle(e.target.value)}
            >
              {STYLES.map(s => (
                <option key={s.value} value={s.value}>{s.label}</option>
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
          {/* Header with validation status */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <FileText size={18} className="text-blue-400" />
              <h2 className="text-base font-semibold text-zinc-200">Generated Listing</h2>
              <span className="text-xs text-zinc-500 bg-zinc-800 px-2 py-1 rounded">
                {result.niche} • {result.style}
              </span>
            </div>
            <div className={`flex items-center gap-2 text-sm px-3 py-1.5 rounded-lg ${
              result.validation?.is_compliant
                ? 'bg-emerald-500/20 text-emerald-400'
                : 'bg-amber-500/20 text-amber-400'
            }`}>
              {result.validation?.is_compliant ? (
                <>
                  <CheckCircle size={16} />
                  <span>{result.validation.checks_passed}/{result.validation.total_checks} Checks Passed</span>
                </>
              ) : (
                <>
                  <AlertTriangle size={16} />
                  <span>{result.validation?.checks_passed || 0}/{result.validation?.total_checks || 7} Checks Passed</span>
                </>
              )}
            </div>
          </div>

          {/* Validation Issues */}
          {result.validation?.issues?.length > 0 && (
            <div className="mb-6 p-4 bg-amber-500/10 border border-amber-500/30 rounded-xl">
              <p className="text-sm font-medium text-amber-400 mb-2">Issues Found:</p>
              <ul className="text-sm text-amber-300 space-y-1">
                {result.validation.issues.map((issue, i) => <li key={i}>• {issue}</li>)}
              </ul>
            </div>
          )}

          {/* Amazon Format Fields */}
          <div className="space-y-4">
            {/* Title & Brand Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Field
                label="Title"
                field="title"
                limit={LIMITS.title}
              />
              <Field
                label="Brand"
                field="brand"
                limit={LIMITS.brand}
              />
            </div>

            {/* Bullet Points */}
            <Field
              label="Feature Bullet 1"
              field="bullet_1"
              limit={LIMITS.bullet_1}
            />
            <Field
              label="Feature Bullet 2"
              field="bullet_2"
              limit={LIMITS.bullet_2}
            />

            {/* Description */}
            <Field
              label="Product Description"
              field="description"
              limit={LIMITS.description_max}
              minLength={LIMITS.description_min}
              multiline
            />

            {/* Keywords */}
            <Field
              label="Backend Keywords"
              field="keywords"
              limit={LIMITS.keywords}
              isBytes
            />
          </div>

          {/* Copy All Button */}
          <div className="mt-6 pt-4 border-t border-zinc-800 flex justify-between items-center">
            <div className="text-xs text-zinc-500">
              Amazon Format: Title (60) • Brand (50) • Bullets (256 each) • Description (75-2000) • Keywords (250 bytes)
            </div>
            <button
              className="btn btn-secondary"
              onClick={() => {
                const all = `TITLE:\n${result.title?.text || ''}\n\nBRAND:\n${result.brand?.text || ''}\n\nBULLET 1:\n${result.bullet_1?.text || ''}\n\nBULLET 2:\n${result.bullet_2?.text || ''}\n\nDESCRIPTION:\n${result.description?.text || ''}\n\nKEYWORDS:\n${result.keywords?.text || ''}`
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
          <p className="text-zinc-500 text-sm max-w-md mx-auto">
            Enter your design phrase above. The generator will create Amazon TOS-compliant
            content that describes only the design — no promotional language.
          </p>
        </div>
      )}

      {/* Character Limits Reference */}
      <div className="bg-zinc-900/50 rounded-xl border border-zinc-800 p-4">
        <h3 className="text-sm font-semibold text-zinc-300 mb-3">Amazon Character Limits</h3>
        <div className="grid grid-cols-2 md:grid-cols-6 gap-3 text-xs">
          <div className="bg-zinc-800/50 rounded-lg p-2 text-center">
            <div className="text-zinc-400">Title</div>
            <div className="text-zinc-200 font-mono font-semibold">60 chars</div>
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-2 text-center">
            <div className="text-zinc-400">Brand</div>
            <div className="text-zinc-200 font-mono font-semibold">50 chars</div>
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-2 text-center">
            <div className="text-zinc-400">Bullet 1</div>
            <div className="text-zinc-200 font-mono font-semibold">256 chars</div>
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-2 text-center">
            <div className="text-zinc-400">Bullet 2</div>
            <div className="text-zinc-200 font-mono font-semibold">256 chars</div>
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-2 text-center">
            <div className="text-zinc-400">Description</div>
            <div className="text-zinc-200 font-mono font-semibold">75-2000</div>
          </div>
          <div className="bg-zinc-800/50 rounded-lg p-2 text-center">
            <div className="text-zinc-400">Keywords</div>
            <div className="text-zinc-200 font-mono font-semibold">250 bytes</div>
          </div>
        </div>
      </div>
    </div>
  )
}
