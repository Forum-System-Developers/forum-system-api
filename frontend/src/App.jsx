import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css'
import Login from './pages/login'
import Topics from './pages/topics'
import TopicDetail from './pages/TopicDetail'

function App() {

  return (
    <Router>
      <Routes>
        {/* Login Route */}
        <Route path="/login" element={<Login />} />
          
        {/* Topics Route */}
        <Route path="/topics" element={<Topics />} />

        {/* Topic detail route */}
        <Route path="/topic/:topicId" element={<TopicDetail />} />
      </Routes>
    </Router>
  );
}

export default App;