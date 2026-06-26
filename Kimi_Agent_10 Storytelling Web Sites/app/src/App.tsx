import { Routes, Route } from 'react-router'
import Layout from './components/Layout'
import Home from './pages/Home'
import Heroes from './pages/Heroes'
import Developers from './pages/Developers'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/heroes" element={<Heroes />} />
        <Route path="/developers" element={<Developers />} />
      </Routes>
    </Layout>
  )
}
