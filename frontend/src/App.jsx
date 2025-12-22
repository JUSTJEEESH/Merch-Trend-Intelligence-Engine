import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Trademarks from './pages/Trademarks'
import SEOGenerator from './pages/SEOGenerator'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="trademarks" element={<Trademarks />} />
          <Route path="seo" element={<SEOGenerator />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
