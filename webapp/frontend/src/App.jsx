import Dashboard from './components/Dashboard'
import { Toaster } from 'react-hot-toast'

function App() {
  return (
    <>
      <Dashboard />
      <Toaster position="top-right" toastOptions={{
        style: {
          background: '#1a1a2e',
          color: '#f1f5f9',
          border: '1px solid #2d2d4e',
        },
      }} />
    </>
  )
}

export default App