/**
 * BiteRight — api.js
 * All API calls live here. Import from this file, NOT from app.js.
 */

const BASE = '/api';

// ── Shared fetch helper ────────────────────────────────────────────────────
async function apiFetch(url, options = {}) {
  let res;
  try {
    res = await fetch(url, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options,
    });
  } catch (networkErr) {
    throw new Error('Network error — is the server running?');
  }

  let json;
  try {
    json = await res.json();
  } catch {
    throw new Error(`Server returned non-JSON (HTTP ${res.status})`);
  }

  if (!res.ok) {
    const msg =
      json?.message ||
      json?.detail ||
      (json?.errors ? JSON.stringify(json.errors) : null) ||
      `HTTP ${res.status}`;
    throw new Error(msg);
  }

  return json;
}

// ── Users ──────────────────────────────────────────────────────────────────
/**
 * POST /api/users/
 * Returns the user object { id, name, email, ... }
 */
export async function createUser(payload) {
  const json = await apiFetch(`${BASE}/users/`, {
    method: 'POST',
    body:   JSON.stringify(payload),
  });
  return json.data ?? json;
}

export async function getAddresses(userId) {
  const json = await apiFetch(`${BASE}/users/${userId}/addresses/`);
  return Array.isArray(json) ? json : (json.data ?? json.results ?? []);
}


// ── Restaurants ────────────────────────────────────────────────────────────
export async function getRestaurants() {
  const json = await apiFetch(`${BASE}/restaurants/`);
  return Array.isArray(json) ? json : (json.data ?? json.results ?? []);
}

export async function getRestaurant(id) {
  const json = await apiFetch(`${BASE}/restaurants/${id}/`);
  return json.data ?? json;
}

export async function getReviews(restaurantId) {
  const json = await apiFetch(`${BASE}/restaurants/${restaurantId}/reviews/`);
  return Array.isArray(json) ? json : (json.data ?? json.results ?? []);
}

// ── Menu ───────────────────────────────────────────────────────────────────
export async function getMenu(restaurantId) {
  const json = await apiFetch(`${BASE}/restaurants/${restaurantId}/menu/`);
  return Array.isArray(json) ? json : (json.data ?? json.results ?? []);
}

// ── Recommendations ────────────────────────────────────────────────────────
export async function getRecommendations(userId, restaurantId, mood = '', time = '') {
  const params = new URLSearchParams();
  if (mood) params.set('mood', mood);
  if (time) params.set('time', time);
  const qs   = params.toString() ? `?${params}` : '';
  const json = await apiFetch(`${BASE}/recommendations/${userId}/${restaurantId}/${qs}`);
  return json;
}

// ── Search ─────────────────────────────────────────────────────────────────
export async function searchMenu(query) {
  const json = await apiFetch(`${BASE}/search-menu/?q=${encodeURIComponent(query)}`);
  return Array.isArray(json) ? json : (json.data ?? json.results ?? []);
}

// ── Orders ─────────────────────────────────────────────────────────────────
/**
 * POST /api/orders/
 * Payload: { user, restaurant, total_price, items:[{menu_item, quantity}] }
 */
export async function createOrder(cartItems, userId, restaurantId, totalPrice) {
  const payload = {
    user:        userId,
    restaurant:  restaurantId ?? null,
    total_price: totalPrice,
    items: cartItems.map(item => ({
      menu_item: item.id,
      quantity:  item.qty ?? 1,
    })),
  };
  return apiFetch(`${BASE}/orders/`, {
    method: 'POST',
    body:   JSON.stringify(payload),
  });
}

/**
 * GET /api/orders/?user=<id>
 * Returns array of orders.
 */
export async function getOrders(userId) {
  const json = await apiFetch(`${BASE}/orders/?user=${userId}`);
  return Array.isArray(json) ? json : (json.data ?? json.results ?? []);
}
