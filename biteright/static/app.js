/**
 * BiteRight — app.js
 * UI helpers only: User session, Cart, Toast, Nav, dish card, etc.
 * API calls (getRestaurants, getMenu, etc.) live in api.js — import from there.
 */

// ── User Session ───────────────────────────────────────────────────────────
export const User = {
  get:   ()  => JSON.parse(localStorage.getItem('br_user') || 'null'),
  set:   (u) => localStorage.setItem('br_user', JSON.stringify(u)),
  clear: ()  => localStorage.removeItem('br_user'),
  id:    ()  => User.get()?.id ?? null,
  name:  ()  => User.get()?.name ?? 'Guest',
};

// ── Auth Guard ─────────────────────────────────────────────────────────────
export function requireAuth() {
  if (!User.get()) {
    const returnTo = encodeURIComponent(location.pathname + location.search);
    location.replace(`/login.html?next=${returnTo}`);
    return false;
  }
  return true;
}

// ── Cart ───────────────────────────────────────────────────────────────────
export const Cart = {
  get:   ()      => JSON.parse(localStorage.getItem('br_cart') || '[]'),
  save:  (items) => { localStorage.setItem('br_cart', JSON.stringify(items)); Cart._notify(); },

  add(dish, restaurantId, restaurantName) {
    const items = Cart.get();
    const idx   = items.findIndex(i => i.id === dish.id);
    if (idx >= 0) { items[idx].qty += 1; }
    else          { items.push({ ...dish, qty: 1, restaurantId, restaurantName }); }
    Cart.save(items);
  },

  remove(dishId)          { Cart.save(Cart.get().filter(i => i.id !== dishId)); },

  updateQty(dishId, qty) {
    if (qty <= 0) { Cart.remove(dishId); return; }
    const items = Cart.get();
    const idx   = items.findIndex(i => i.id === dishId);
    if (idx >= 0) { items[idx].qty = qty; Cart.save(items); }
  },

  clear: () => { localStorage.removeItem('br_cart'); Cart._notify(); },
  total: () => Cart.get().reduce((s, i) => s + i.price * i.qty, 0),
  count: () => Cart.get().reduce((s, i) => s + i.qty, 0),

  _notify() {
    document.querySelectorAll('.cart-badge').forEach(el => {
      el.textContent = Cart.count();
    });
    const fc = document.querySelector('.float-cart');
    if (fc) {
      if (Cart.count() > 0) {
        fc.classList.add('visible');
        const cc = fc.querySelector('.fc-count');
        const ct = fc.querySelector('.fc-total');
        if (cc) cc.textContent = Cart.count();
        if (ct) ct.textContent = `₹${Cart.total()}`;
      } else {
        fc.classList.remove('visible');
      }
    }
  },

  init() { Cart._notify(); },
};

// ── Toast ──────────────────────────────────────────────────────────────────
let _toastContainer;
function getToastContainer() {
  if (!_toastContainer) {
    _toastContainer = document.createElement('div');
    _toastContainer.className = 'toast-container';
    document.body.appendChild(_toastContainer);
  }
  return _toastContainer;
}

export function toast(msg, type = 'info', duration = 3000) {
  const icons  = { success: '✓', error: '✕', info: 'ℹ', cart: '🛒' };
  const colors = { success: '#2ECC71', error: '#E74C3C', info: '#FF4D00', cart: '#FF4D00' };
  const tc = getToastContainer();
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.innerHTML = `<span style="color:${colors[type]};font-weight:700">${icons[type] || '·'}</span><span>${msg}</span>`;
  tc.appendChild(el);
  setTimeout(() => {
    el.style.animation = 'toastOut 0.3s ease forwards';
    setTimeout(() => el.remove(), 300);
  }, duration);
}

// ── Nav ────────────────────────────────────────────────────────────────────
export function renderNav(activePage = '') {
  const user  = User.get();
  const pages = [
    { href: '/index.html',           label: 'Home' },
    { href: '/restaurants.html',     label: 'Restaurants' },
    { href: '/recommendations.html', label: 'For You' },
    { href: '/orders.html',          label: 'Orders' },
  ];
  const links = pages.map(p =>
    `<a href="${p.href}" class="${activePage === p.href ? 'active' : ''}">${p.label}</a>`
  ).join('');

  const userArea = user
    ? `<span style="font-size:0.82rem;color:var(--text2)">Hi, ${user.name.split(' ')[0]} 👋</span>
       <a href="/login.html" class="btn btn-ghost btn-sm">Profile</a>`
    : `<a href="/login.html" class="btn btn-ghost btn-sm">Sign in</a>`;

  return `
  <nav class="nav">
    <a href="/index.html" class="nav-logo">🔥<span>Bite</span>Right</a>
    <div class="nav-links">${links}</div>
    <div class="nav-right" style="display:flex;align-items:center;gap:10px">
      ${userArea}
      <a href="/cart.html" class="nav-cart-btn">
        🛒 Cart <span class="cart-badge">0</span>
      </a>
    </div>
  </nav>`;
}

// ── Float Cart ─────────────────────────────────────────────────────────────
export function renderFloatCart() {
  return `
  <a href="/cart.html" class="float-cart">
    🛒 <span class="fc-count">0</span> items &nbsp;·&nbsp; <span class="fc-total">₹0</span> &nbsp;→ View Cart
  </a>`;
}

// ── Mood / Time Config ─────────────────────────────────────────────────────
export const MOODS = [
  { id: 'comfort',    emoji: '🤗', label: 'Comfort',    color: '#FF6B2B' },
  { id: 'healthy',    emoji: '🥗', label: 'Healthy',    color: '#2ECC71' },
  { id: 'spicy',      emoji: '🌶️', label: 'Spicy',      color: '#E74C3C' },
  { id: 'cheat_meal', emoji: '🍔', label: 'Cheat Meal', color: '#FFBE00' },
];

export const TIMES = [
  { id: 'morning',    label: 'Morning',    emoji: '🌅' },
  { id: 'afternoon',  label: 'Afternoon',  emoji: '☀️' },
  { id: 'night',      label: 'Night',      emoji: '🌙' },
  { id: 'late_night', label: 'Late Night', emoji: '🦉' },
];

// ── Dish Card ──────────────────────────────────────────────────────────────
export function dishCard(dish, restaurantId, restaurantName, opts = {}) {
  const isVeg    = dish.is_veg === true;
  const scoreTag = dish.score != null
    ? `<span class="tag tag-score">⭐ ${dish.score}</span>` : '';
  const allergyBtn = opts.showAllergy
    ? `<button class="btn btn-ghost btn-sm allergy-check"
         data-ingredients="${dish.ingredients || ''}">🔍 Allergy</button>` : '';
  
  const rankBadge = opts.rank 
    ? `<div style="position:absolute;top:10px;right:10px;background:rgba(14,12,10,.8);border:1px solid var(--border);border-radius:50px;padding:3px 10px;font-size:.75rem;font-weight:700;color:var(--accent);z-index:2">#${opts.rank}</div>`
    : '';

  return `
  <div class="card dish-card fade-up" data-id="${dish.id}">
    <div class="dish-img-wrap">
      <div class="dish-img-placeholder">${isVeg ? '🥦' : '🍗'}</div>
      <div class="dish-dot ${isVeg ? 'veg' : 'nonveg'}"></div>
      ${rankBadge}
    </div>
    <div class="dish-body">
      <div class="flex-between mb-8">
        <h3 class="dish-name">${dish.name}</h3>${scoreTag}
      </div>
      <div class="dish-tags mb-8">
        <span class="tag ${isVeg ? 'tag-veg' : 'tag-nonveg'}">${isVeg ? '🌿 Veg' : '🍖 Non-veg'}</span>
        ${dish.category_name ? `<span class="tag tag-mood">${dish.category_name}</span>` : ''}
      </div>
      <p class="text-xs text-muted mb-12" style="height:2.4rem; overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;">
        ${dish.description || 'Delicious freshly prepared meal.'}
      </p>
      
      <div class="ingredients-wrap mb-10 hidden" id="ing-${dish.id}">
        <div style="font-size:0.75rem; color:var(--text2); padding:10px; background:var(--bg2); border-radius:8px; border:1px dashed var(--border); line-height:1.4">
          <b style="color:var(--text)">🛒 Ingredients:</b><br>${dish.ingredients || 'Secret recipe!'}
        </div>
      </div>

      <div class="flex-between align-center mb-12">
        <p class="dish-price" style="margin:0; font-size:1.1rem">₹${dish.price}</p>
        <button class="btn btn-ghost btn-sm view-ing" data-id="${dish.id}" style="font-size:0.7rem; color:var(--primary)">View Ingredients</button>
      </div>

      <div class="dish-actions">
        <button class="btn btn-primary btn-sm add-to-cart" style="flex:1"
          data-id="${dish.id}" data-name="${dish.name}" data-price="${dish.price}"
          data-diet="${dish.diet_tags || ''}" data-mood="${dish.category_name || ''}"
          data-ingredients="${dish.ingredients || ''}"
          data-restaurant-id="${restaurantId}"
          data-restaurant-name="${restaurantName || ''}">
          + Add
        </button>
        ${allergyBtn}
      </div>
    </div>
  </div>`;
}

// ── Cart button event binding ──────────────────────────────────────────────
export function bindCartButtons(container) {
  container.addEventListener('click', e => {
    // Ingredients Toggle
    const ingBtn = e.target.closest('.view-ing');
    if (ingBtn) {
      const id  = ingBtn.dataset.id;
      const box = document.getElementById(`ing-${id}`);
      if (box) {
        box.classList.toggle('hidden');
        ingBtn.textContent = box.classList.contains('hidden') ? 'View Ingredients' : 'Hide Ingredients';
      }
    }

    const btn = e.target.closest('.add-to-cart');
    if (btn) {
      const dish = {
        id:          +btn.dataset.id,
        name:         btn.dataset.name,
        price:       +btn.dataset.price,
        diet_tags:    btn.dataset.diet,
        mood_tags:    btn.dataset.mood,
        ingredients:  btn.dataset.ingredients,
      };
      Cart.add(dish, btn.dataset.restaurantId, btn.dataset.restaurantName);
      toast(`${dish.name} added to cart!`, 'cart');
      btn.textContent = '✓ Added';
      btn.classList.replace('btn-primary', 'btn-secondary');
      setTimeout(() => {
        btn.textContent = '+ Add';
        btn.classList.replace('btn-secondary', 'btn-primary');
      }, 1500);
    }

    const allergyBtn = e.target.closest('.allergy-check');
    if (allergyBtn) {
      const user        = User.get();
      const ingredients = allergyBtn.dataset.ingredients.toLowerCase();
      const allergy     = (user?.allergies || '').toLowerCase().trim();
      if (!allergy) { toast('No allergies on file. Update your profile.', 'info'); return; }
      const allergens = allergy.split(',').map(a => a.trim()).filter(Boolean);
      const found     = allergens.filter(a => ingredients.includes(a));
      found.length
        ? toast(`⚠️ Contains: ${found.join(', ')}`, 'error', 5000)
        : toast('✓ Safe for your allergies!', 'success');
    }
  });
}

// ── Currency formatter ─────────────────────────────────────────────────────
export const fmt = (n) => `₹${Number(n).toLocaleString('en-IN')}`;
