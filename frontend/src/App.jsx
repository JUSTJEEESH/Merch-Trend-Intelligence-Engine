import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Phrases from './pages/Phrases'
import Patterns from './pages/Patterns'
import PhraseDetail from './pages/PhraseDetail'
import Trademarks from './pages/Trademarks'
import SEOGenerator from './pages/SEOGenerator'
import Export from './pages/Export'
import Scraping from './pages/Scraping'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="phrases" element={<Phrases />} />
          <Route path="phrases/:id" element={<PhraseDetail />} />
          <Route path="patterns" element={<Patterns />} />
          <Route path="trademarks" element={<Trademarks />} />
          <Route path="seo" element={<SEOGenerator />} />
          <Route path="export" element={<Export />} />
          <Route path="scraping" element={<Scraping />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
