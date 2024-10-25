import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Topics = () => {
  const [topics, setTopics] = useState([]);

  // Fetch topics from FastAPI
  useEffect(() => {
    axios.get('http://localhost:8000/api/v1/topics/')  // Replace with your FastAPI endpoint
      .then(response => {
        setTopics(response.data);  // Set the topics in the state
      })
      .catch(error => {
        console.error('Error fetching topics:', error);
      });
  }, []);

  return (
    <div>
      <h1>Topics</h1>
      <ul>
        {topics.map((topic) => (
          <li key={topic.id}>{topic.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default Topics;
