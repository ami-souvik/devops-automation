import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import { PersistGate } from 'redux-persist/integration/react'
import Router from '@/app-components/router'
import './index.css'
import { persistor, store } from '@/store'

createRoot(document.getElementById('root')!).render(
  // <StrictMode>
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <Router />
      </PersistGate>
    </Provider>
  // </StrictMode>,
)
