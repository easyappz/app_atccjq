import instance from './axios';

/**
 * Get all messages
 * @returns {Promise} Array of messages
 */
export const getMessages = async () => {
  const token = localStorage.getItem('token');
  const response = await instance.get('/api/messages/', {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};

/**
 * Send a new message
 * @param {Object} data - Message data
 * @param {string} data.text - Message text
 * @returns {Promise} Created message data
 */
export const sendMessage = async (data) => {
  const token = localStorage.getItem('token');
  const response = await instance.post('/api/messages/', data, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};
