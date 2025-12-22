import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { exportPhrases, getExportFiles, downloadExport, deleteExportFile } from '../api/client'
import Loading from '../components/Loading'

export default function Export() {
  const [format, setFormat] = useState('csv')
  const [filters, setFilters] = useState({
    is_safe: true,
    min_trend_score: '',
    niche: '',
  })
  const [includeMetrics, setIncludeMetrics] = useState(true)

  const queryClient = useQueryClient()

  const { data: files, isLoading } = useQuery({
    queryKey: ['exportFiles'],
    queryFn: getExportFiles,
  })

  const exportMutation = useMutation({
    mutationFn: (data) => exportPhrases(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['exportFiles'])
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (filename) => deleteExportFile(filename),
    onSuccess: () => {
      queryClient.invalidateQueries(['exportFiles'])
    },
  })

  const handleExport = () => {
    exportMutation.mutate({
      format,
      filters: {
        is_safe: filters.is_safe,
        min_trend_score: filters.min_trend_score ? parseFloat(filters.min_trend_score) : undefined,
        niche: filters.niche || undefined,
      },
      include_metrics: includeMetrics,
    })
  }

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Export Data</h1>
        <p className="text-gray-500 mt-1">Export phrases and SEO content to CSV or JSON</p>
      </div>

      {/* Export Form */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Export Phrases</h2>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Format</label>
            <select
              className="input"
              value={format}
              onChange={(e) => setFormat(e.target.value)}
            >
              <option value="csv">CSV</option>
              <option value="json">JSON</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Safety Filter</label>
            <select
              className="input"
              value={filters.is_safe ? 'safe' : 'all'}
              onChange={(e) => setFilters(prev => ({
                ...prev,
                is_safe: e.target.value === 'safe'
              }))}
            >
              <option value="safe">Safe Only</option>
              <option value="all">All Phrases</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Min Trend Score</label>
            <input
              type="number"
              className="input"
              placeholder="0"
              min="0"
              max="100"
              value={filters.min_trend_score}
              onChange={(e) => setFilters(prev => ({
                ...prev,
                min_trend_score: e.target.value
              }))}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Niche</label>
            <input
              type="text"
              className="input"
              placeholder="Any niche"
              value={filters.niche}
              onChange={(e) => setFilters(prev => ({
                ...prev,
                niche: e.target.value
              }))}
            />
          </div>
        </div>

        <div className="flex items-center gap-4">
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={includeMetrics}
              onChange={(e) => setIncludeMetrics(e.target.checked)}
              className="rounded border-gray-300"
            />
            <span className="text-sm text-gray-700">Include metrics data</span>
          </label>

          <button
            className="btn btn-primary ml-auto"
            onClick={handleExport}
            disabled={exportMutation.isPending}
          >
            {exportMutation.isPending ? 'Exporting...' : 'Export'}
          </button>
        </div>

        {exportMutation.isSuccess && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-800">
              ✅ Export complete! {exportMutation.data?.record_count} records exported to{' '}
              <strong>{exportMutation.data?.filename}</strong>
            </p>
          </div>
        )}
      </div>

      {/* Export Files */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Export Files</h2>

        {isLoading ? (
          <Loading />
        ) : files?.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="text-left p-3">Filename</th>
                  <th className="text-left p-3">Size</th>
                  <th className="text-left p-3">Created</th>
                  <th className="text-left p-3">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {files.map((file) => (
                  <tr key={file.filename} className="hover:bg-gray-50">
                    <td className="p-3">
                      <span className="font-mono text-sm">{file.filename}</span>
                    </td>
                    <td className="p-3 text-gray-500">{formatFileSize(file.size)}</td>
                    <td className="p-3 text-gray-500">
                      {new Date(file.created).toLocaleString()}
                    </td>
                    <td className="p-3">
                      <div className="flex gap-2">
                        <a
                          href={downloadExport(file.filename)}
                          className="btn btn-primary text-sm py-1 px-3"
                          download
                        >
                          Download
                        </a>
                        <button
                          className="btn btn-danger text-sm py-1 px-3"
                          onClick={() => deleteMutation.mutate(file.filename)}
                          disabled={deleteMutation.isPending}
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">
            No export files yet. Create an export above.
          </p>
        )}
      </div>

      {/* Export Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card bg-blue-50 border-blue-200">
          <h3 className="font-medium text-blue-800 mb-2">CSV Format</h3>
          <p className="text-sm text-blue-700 mb-2">
            Best for spreadsheet applications like Excel or Google Sheets.
          </p>
          <p className="text-sm text-blue-700">
            Includes: ID, text, normalized text, niche, frequency, trend score, risk score, safety status, and more.
          </p>
        </div>

        <div className="card bg-green-50 border-green-200">
          <h3 className="font-medium text-green-800 mb-2">JSON Format</h3>
          <p className="text-sm text-green-700 mb-2">
            Best for programmatic use or importing into other tools.
          </p>
          <p className="text-sm text-green-700">
            Full structured data with nested metrics when included.
          </p>
        </div>
      </div>
    </div>
  )
}
