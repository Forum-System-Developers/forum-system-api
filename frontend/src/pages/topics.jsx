import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './topics.css';

const Topics = () => {
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/v1/topics/public')
      .then(response => {
        setTopics(response.data);
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
          <li key={topic.id}>
            <h2>{topic.title}</h2>
            <ul>
              {topic.replies.map((reply) => (
                <li key={reply.id}>
                  {reply.content}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Topics;
