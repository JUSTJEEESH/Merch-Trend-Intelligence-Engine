import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function TrendChart({ data, title }) {
  return (
    <div className="card">
      <h3 className="text-lg font-medium mb-4">{title}</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => new Date(value).toLocaleDateString()}
            />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip
              labelFormatter={(value) => new Date(value).toLocaleDateString()}
            />
            <Line
              type="monotone"
              dataKey="trend_score"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
              name="Trend Score"
            />
            <Line
              type="monotone"
              dataKey="frequency"
              stroke="#22c55e"
              strokeWidth={2}
              dot={false}
              name="Frequency"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
