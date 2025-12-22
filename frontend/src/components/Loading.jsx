import { Loader2 } from 'lucide-react'

export default function Loading({ text = 'Loading...' }) {
  return (
    <div className="flex items-center justify-center py-12">
      <div className="text-center">
        <Loader2 size={32} className="animate-spin text-gray-400 mx-auto" />
        <p className="mt-3 text-sm text-gray-500">{text}</p>
      </div>
    </div>
  )
}
