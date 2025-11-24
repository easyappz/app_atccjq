import instance from './axios';

/**
 * Register a new user
 * @param {Object} data - Registration data
 * @param {string} data.username - Username
 * @param {string} data.password - Password
 * @returns {Promise} Response with token and user data
 */
export const register = async (data) => {
  const response = await instance.post('/api/register/', data);
  return response.data;
};

/**
 * Login user
 * @param {Object} data - Login credentials
 * @param {string} data.username - Username
 * @param {string} data.password - Password
 * @returns {Promise} Response with token and user data
 */
export const login = async (data) => {
  const response = await instance.post('/api/login/', data);
  return response.data;
};

/**
 * Get current user profile
 * @returns {Promise} User profile data
 */
export const getProfile = async () => {
  const token = localStorage.getItem('token');
  const response = await instance.get('/api/profile/', {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  return response.data;
};
