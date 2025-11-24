import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMessages, sendMessage } from '../../api/messages';
import './styles.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [messageText, setMessageText] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    loadMessages();
  }, [navigate]);

  const loadMessages = async () => {
    try {
      setLoading(true);
      const data = await getMessages();
      setMessages(data);
    } catch (error) {
      console.error('Failed to load messages:', error);
      if (error.response?.status === 401) {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!messageText.trim() || sending) return;

    try {
      setSending(true);
      const newMessage = await sendMessage({ text: messageText });
      setMessages([...messages, newMessage]);
      setMessageText('');
    } catch (error) {
      console.error('Failed to send message:', error);
      if (error.response?.status === 401) {
        navigate('/login');
      }
    } finally {
      setSending(false);
    }
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
  };

  return (
    <div className="chat-container" data-easytag="id1-react/src/components/Chat/index.jsx">
      <div className="chat-header">
        <h1 className="chat-title">Групповой чат</h1>
        <button
          className="profile-button"
          onClick={() => navigate('/profile')}
        >
          Профиль
        </button>
      </div>

      <div className="chat-messages">
        {loading ? (
          <div className="loading-message">Загрузка сообщений...</div>
        ) : messages.length === 0 ? (
          <div className="empty-message">Пока нет сообщений. Будьте первым!</div>
        ) : (
          messages.map((message) => (
            <div key={message.id} className="message-item">
              <div className="message-bubble">
                <div className="message-author">{message.author}</div>
                <div className="message-text">{message.text}</div>
                <div className="message-time">{formatTime(message.created_at)}</div>
              </div>
            </div>
          ))
        )}
      </div>

      <form className="chat-form" onSubmit={handleSendMessage}>
        <input
          type="text"
          className="message-input"
          placeholder="Введите сообщение..."
          value={messageText}
          onChange={(e) => setMessageText(e.target.value)}
          disabled={sending}
        />
        <button
          type="submit"
          className="send-button"
          disabled={!messageText.trim() || sending}
        >
          {sending ? 'Отправка...' : 'Отправить'}
        </button>
      </form>
    </div>
  );
};

export default Chat;
