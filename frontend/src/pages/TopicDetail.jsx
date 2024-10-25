// TopicDetail.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom'; // Import useParams to access URL parameters

const TopicDetail = () => {
  const { topicId } = useParams(); // Get the topic ID from the URL
  const [topic, setTopic] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/v1/topics/${topicId}`)
      .then(response => {
        setTopic(response.data);
      })
      .catch(error => {
        console.error('Error fetching topic details:', error);
      });
  }, [topicId]); // Dependency array includes topicId to refetch if it changes

  if (!topic) return <div>Loading...</div>; // Handle loading state

  return (
    <div>
      <h1>{topic.title}</h1>
      <p>{topic.content}</p>
      <h2>Replies:</h2>
      <ul>
        {topic.replies.map((reply) => (
          <li key={reply.id}>
            {reply.content}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TopicDetail;
