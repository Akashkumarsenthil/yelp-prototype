import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export const authAPI = {
  signup: (data) => api.post('/auth/signup', data),
  login: (data) => api.post('/auth/login', data),
};

export const userAPI = {
  getProfile: () => api.get('/users/me'),
  updateProfile: (data) => api.put('/users/me', data),
  uploadPicture: (file) => {
    const fd = new FormData();
    fd.append('file', file);
    return api.post('/users/me/picture', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
  },
};

export const preferencesAPI = {
  get: () => api.get('/preferences/'),
  update: (data) => api.put('/preferences/', data),
};

export const restaurantAPI = {
  list: (params) => api.get('/restaurants/', { params }),
  get: (id) => api.get(`/restaurants/${id}`),
  create: (data) => api.post('/restaurants/', data),
  update: (id, data) => api.put(`/restaurants/${id}`, data),
  claim: (id) => api.post(`/restaurants/${id}/claim`),
  uploadPhoto: (id, file) => {
    const fd = new FormData();
    fd.append('file', file);
    return api.post(`/restaurants/${id}/photos`, fd, { headers: { 'Content-Type': 'multipart/form-data' } });
  },
};

export const reviewAPI = {
  getForRestaurant: (id) => api.get(`/reviews/restaurant/${id}`),
  create: (data) => api.post('/reviews/', data),
  update: (id, data) => api.put(`/reviews/${id}`, data),
  delete: (id) => api.delete(`/reviews/${id}`),
  getMine: () => api.get('/reviews/user/me'),
};

export const favouriteAPI = {
  list: () => api.get('/favourites/'),
  add: (id) => api.post(`/favourites/${id}`),
  remove: (id) => api.delete(`/favourites/${id}`),
  check: (id) => api.get(`/favourites/check/${id}`),
};

export const ownerAPI = {
  getRestaurants: () => api.get('/owner/restaurants'),
  getReviews: (id) => api.get(`/owner/restaurants/${id}/reviews`),
  getDashboard: () => api.get('/owner/dashboard'),
};

export const chatAPI = {
  send: (data) => api.post('/ai-assistant/chat', data),
};

export const historyAPI = {
  get: () => api.get('/history/'),
};

export default api;
