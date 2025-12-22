import { TrendingUp, TrendingDown } from 'lucide-react'

export default function StatsCard({ title, value, icon: Icon, change, changeType }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-2xl font-semibold text-gray-900 mt-1">{value}</p>
          {change !== undefined && (
            <div className={`flex items-center gap-1 text-sm mt-2 ${
              changeType === 'positive' ? 'text-green-600' :
              changeType === 'negative' ? 'text-red-600' :
              'text-gray-500'
            }`}>
              {changeType === 'positive' && <TrendingUp size={14} />}
              {changeType === 'negative' && <TrendingDown size={14} />}
              <span>{change}</span>
            </div>
          )}
        </div>
        {Icon && (
          <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
            <Icon size={20} className="text-gray-600" />
          </div>
        )}
      </div>
    </div>
  )
}
