import axios from 'axios'

const BASE = 'https://todo-199jiuq4.b4a.run/auth'

export async function register(username, email, password) {
  const { data } = await axios.post(`${BASE}/register`, { username, email, password })
  return data
}

export async function login(username, password) {
  const { data } = await axios.post(`${BASE}/login`, { username, password })
  return data  // { access_token, token_type, username, email }
}
