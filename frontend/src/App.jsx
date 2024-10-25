import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Login from './pages/login'
import Topics from './pages/topics'

function App() {
  const [count, setCount] = useState(0);

  return (
    <Router>
      <Routes>
        {/* Login Route */}
        <Route path="/login" element={<Login />} />
          
        {/* Topics Route */}
        <Route path="/topics" element={<Topics />} />
      </Routes>
    </Router>
  );
}

export default App;