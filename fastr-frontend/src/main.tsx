import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import Options from './Options.tsx'
import './index.css'

const isOptionsPage = window.location.pathname.includes('options.html')
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {isOptionsPage ? <Options /> : <App />}
  </StrictMode>,
)
