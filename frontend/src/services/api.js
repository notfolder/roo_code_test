import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
})

// 保存済みトークンをヘッダへ設定
const token = localStorage.getItem('token')
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

export default api
