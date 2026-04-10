const API_BASE = import.meta.env.VITE_API_BASE || "/api";

const defaultHeaders = () => ({
  "Content-Type": "application/json",
});

const authHeaders = () => {
  const token = localStorage.getItem("asset_token");
  return {
    ...defaultHeaders(),
    Authorization: token ? `Bearer ${token}` : undefined,
  };
};

const request = async (path, init = {}) => {
  const res = await fetch(`${API_BASE}${path}`, init);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json();
};

export const login = (payload) =>
  request("/auth/login", {
    method: "POST",
    headers: defaultHeaders(),
    body: JSON.stringify(payload),
  });

export const listItems = () =>
  request("/items", {
    headers: authHeaders(),
  });

export const createItem = (payload) =>
  request("/items", {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });

export const updateItem = (id, payload) =>
  request(`/items/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });

export const loanItem = (id, payload) =>
  request(`/items/${id}/loan`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });

export const returnItem = (id) =>
  request(`/items/${id}/return`, {
    method: "POST",
    headers: authHeaders(),
  });

export const listUsers = () =>
  request("/users", {
    headers: authHeaders(),
  });

export const createUser = (payload) =>
  request("/users", {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });

export const updateUser = (id, payload) =>
  request(`/users/${id}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });

export const deleteUser = (id) =>
  request(`/users/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
