/* ============================================
   SMARTLAB HUB — Core JavaScript
   API Client, Auth, Utils
   ============================================ */

const API = (() => {
  const BASE = '';  // Same-origin Django backend

  function getToken() { return localStorage.getItem('slh_access'); }
  function getRefreshToken() { return localStorage.getItem('slh_refresh'); }
  function saveTokens(access, refresh) {
    localStorage.setItem('slh_access', access);
    if (refresh) localStorage.setItem('slh_refresh', refresh);
  }
  function clearTokens() {
    localStorage.removeItem('slh_access');
    localStorage.removeItem('slh_refresh');
    localStorage.removeItem('slh_user');
  }

  function saveUser(user) { localStorage.setItem('slh_user', JSON.stringify(user)); }
  function getUser() {
    try { return JSON.parse(localStorage.getItem('slh_user')); } catch { return null; }
  }

  async function request(method, path, data = null, retry = true) {
    const headers = { 'Content-Type': 'application/json' };
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const opts = { method, headers };
    if (data && method !== 'GET') opts.body = JSON.stringify(data);

    let url = `${BASE}${path}`;
    if (data && method === 'GET') {
      const params = new URLSearchParams(data);
      url += `?${params}`;
    }

    try {
      const res = await fetch(url, opts);

      if (res.status === 401 && retry) {
        // Try refresh
        const refreshed = await refreshAccessToken();
        if (refreshed) return request(method, path, data, false);
        clearTokens();
        window.location.href = '/login';
        return null;
      }

      const ct = res.headers.get('content-type') || '';
      if (ct.includes('application/json')) {
        const json = await res.json();
        if (!res.ok) throw { status: res.status, data: json };
        return json;
      }
      
      // Handle non-JSON responses
      const text = await res.text();
      if (!res.ok) throw { status: res.status, data: { detail: text || `HTTP ${res.status}` } };
      return text;
    } catch (err) {
      if (err.status) throw err;
      throw { status: 0, data: { detail: 'Network error. Is the server running?' } };
    }
  }

  async function refreshAccessToken() {
    const refresh = getRefreshToken();
    if (!refresh) return false;
    try {
      const res = await fetch(`${BASE}/api/auth/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh })
      });
      if (!res.ok) return false;
      const data = await res.json();
      saveTokens(data.access, null);
      return true;
    } catch { return false; }
  }

  return {
    // Auth
    async login(username, password) {
      const data = await request('POST', '/api/auth/login/', { username, password });
      saveTokens(data.access, data.refresh);
      const user = await request('GET', '/api/users/profile/me/');
      saveUser(user);
      return user;
    },

    async register(userData) {
      return request('POST', '/api/users/register/', userData);
    },

    logout() { clearTokens(); window.location.href = '/login'; },

    getUser,
    isAuthenticated() { return !!getToken(); },

    // Users
    users: {
      profile: () => request('GET', '/api/users/profile/me/'),
      updateProfile: (data) => request('PATCH', '/api/users/profile/me/', data),
      list: () => request('GET', '/api/users/list/'),
      approveVendor: (id) => request('POST', `/api/users/approve-vendor/${id}/`),
    },

    // Catalog
    catalog: {
      list: (filters = {}) => request('GET', '/api/catalog/equipment/', filters),
      get: (id) => request('GET', `/api/catalog/equipment/${id}/`),
      // Vendor
      myEquipment: () => request('GET', '/api/catalog/manage/'),
      create: (data) => request('POST', '/api/catalog/manage/', data),
      update: (id, data) => request('PATCH', `/api/catalog/manage/${id}/`, data),
      delete: (id) => request('DELETE', `/api/catalog/manage/${id}/`),
    },

    // Inventory
    inventory: {
      list: () => request('GET', '/api/inventory/'),
      get: (id) => request('GET', `/api/inventory/${id}/`),
      checkIn: (id, data) => request('POST', `/api/inventory/${id}/check_in/`, data),
      create: (data) => request('POST', '/api/inventory/', data),
      update: (id, data) => request('PATCH', `/api/inventory/${id}/`, data),
    },

    // Bookings
    bookings: {
      list: () => request('GET', '/api/bookings/'),
      get: (id) => request('GET', `/api/bookings/${id}/`),
      create: (data) => request('POST', '/api/bookings/', data),
      cancel: (id) => request('PATCH', `/api/bookings/${id}/`, { status: 'CANCELLED' }),
    },

    // Feedback & Incidents
    feedback: {
      reviews: () => request('GET', '/api/feedback/reviews/'),
      submitReview: (data) => request('POST', '/api/feedback/reviews/', data),
      incidents: () => request('GET', '/api/feedback/incidents/'),
      reportIncident: (data) => request('POST', '/api/feedback/incidents/', data),
      dashboard: () => request('GET', '/api/feedback/dashboard/'),
    },

    // Analysis (Admin)
    analysis: {
      dashboard: () => request('GET', '/api/analysis/dashboard/'),
    }
  };
})();

// ── TOAST NOTIFICATIONS ──
const Toast = (() => {
  let container;

  function getContainer() {
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    return container;
  }

  function show(message, type = 'info', duration = 4000) {
    const c = getContainer();
    const icons = { success: '✓', error: '✕', info: 'ℹ', warning: '⚠' };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span style="font-size:16px">${icons[type]}</span><span>${message}</span>`;
    c.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100px)';
      toast.style.transition = 'all 0.3s';
      setTimeout(() => toast.remove(), 300);
    }, duration);

    return toast;
  }

  return {
    success: (msg) => show(msg, 'success'),
    error: (msg) => show(msg, 'error'),
    info: (msg) => show(msg, 'info'),
    warning: (msg) => show(msg, 'warning'),
  };
})();

// ── MODAL MANAGEMENT ──
function openModal(id) {
  const overlay = document.getElementById(id);
  if (overlay) overlay.classList.add('active');
}

function closeModal(id) {
  const overlay = document.getElementById(id);
  if (overlay) overlay.classList.remove('active');
}

// Close modal on overlay click
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('active');
  }
});

// ── SIDEBAR ACTIVE STATE ──
function setActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(item => {
    const href = item.getAttribute('href');
    if (href && (path === href || (href !== '/' && path.startsWith(href)))) {
      item.classList.add('active');
    }
  });
}

// ── USER HEADER ──
function renderUserHeader() {
  const user = API.getUser();
  if (!user) return;

  const avatarEl = document.getElementById('user-avatar');
  const nameEl = document.getElementById('user-name');
  const roleEl = document.getElementById('user-role');

  if (avatarEl) {
    const initials = (user.first_name?.[0] || '') + (user.last_name?.[0] || '') || user.username?.[0]?.toUpperCase() || 'U';
    avatarEl.textContent = initials;
  }
  if (nameEl) nameEl.textContent = user.first_name ? `${user.first_name} ${user.last_name}` : user.username;
  if (roleEl) roleEl.textContent = user.role || 'User';
}

// ── FORMAT HELPERS ──
function fmtDate(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-KE', { day: 'numeric', month: 'short', year: 'numeric' });
}

function fmtDateTime(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleString('en-KE', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function fmtKES(amount) {
  if (amount == null) return '—';
  return `KES ${Number(amount).toLocaleString('en-KE', { minimumFractionDigits: 0 })}`;
}

function statusBadge(status) {
  const map = {
    'AVAILABLE': 'available', 'RENTED': 'rented', 'SOLD': 'completed',
    'MAINTENANCE': 'maintenance', 'CALIBRATION': 'maintenance', 'DAMAGED': 'damaged',
    'PENDING': 'pending', 'CONFIRMED': 'confirmed', 'COMPLETED': 'completed',
    'CANCELLED': 'cancelled', 'ACTIVE': 'active', 'OVERDUE': 'overdue',
  };
  const cls = map[status] || 'pending';
  return `<span class="status-badge ${cls}">${status.replace(/_/g, ' ')}</span>`;
}

// ── DONUT CHART (SVG) ──
function drawDonut(svgId, segments, total) {
  const svg = document.getElementById(svgId);
  if (!svg) return;

  const cx = 60, cy = 60, r = 48, strokeW = 16;
  const circumference = 2 * Math.PI * r;
  let offset = 0;

  svg.innerHTML = '';
  const bg = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  bg.setAttribute('cx', cx); bg.setAttribute('cy', cy); bg.setAttribute('r', r);
  bg.setAttribute('fill', 'none'); bg.setAttribute('stroke', '#151d35');
  bg.setAttribute('stroke-width', strokeW);
  svg.appendChild(bg);

  segments.forEach(seg => {
    const pct = total > 0 ? seg.value / total : 0;
    const dash = pct * circumference;
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', cx); circle.setAttribute('cy', cy); circle.setAttribute('r', r);
    circle.setAttribute('fill', 'none'); circle.setAttribute('stroke', seg.color);
    circle.setAttribute('stroke-width', strokeW);
    circle.setAttribute('stroke-dasharray', `${dash} ${circumference - dash}`);
    circle.setAttribute('stroke-dashoffset', circumference - offset * circumference);
    circle.setAttribute('transform', `rotate(-90 ${cx} ${cy})`);
    circle.setAttribute('stroke-linecap', 'round');
    svg.appendChild(circle);
    offset += pct;
  });
}

// ── BAR CHART (CSS) ──
function drawBarChart(containerId, data, maxVal) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const max = maxVal || Math.max(...data.map(d => d.value), 1);
  container.innerHTML = data.map(d => `
    <div class="bar-wrap">
      <div class="bar" style="height:${(d.value/max)*100}%; background:${d.color || 'var(--primary)'}; opacity:0.85;" data-value="${d.label}: ${d.value}"></div>
      <span class="bar-label">${d.label}</span>
    </div>
  `).join('');
}

// ── DROPDOWN TOGGLES ──
document.addEventListener('click', (e) => {
  // Notifications
  const notifBtn = e.target.closest('#notif-btn');
  const notifDrop = document.getElementById('notif-dropdown');
  if (notifBtn && notifDrop) {
    notifDrop.classList.toggle('open');
    document.getElementById('user-dropdown')?.classList.remove('open');
    return;
  }

  // User dropdown
  const userBtn = e.target.closest('#user-menu-btn');
  const userDrop = document.getElementById('user-dropdown');
  if (userBtn && userDrop) {
    userDrop.classList.toggle('open');
    notifDrop?.classList.remove('open');
    return;
  }

  // Close all dropdowns
  if (!e.target.closest('.header-actions')) {
    notifDrop?.classList.remove('open');
    userDrop?.classList.remove('open');
  }
});

// ── PAGE INIT ──
document.addEventListener('DOMContentLoaded', () => {
  setActiveNav();
  renderUserHeader();

  // Mobile sidebar toggle
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const sidebar = document.querySelector('.app-sidebar');
  if (mobileMenuBtn && sidebar) {
    mobileMenuBtn.addEventListener('click', () => sidebar.classList.toggle('mobile-open'));
  }

  // Logout
  document.querySelectorAll('[data-action="logout"]').forEach(el => {
    el.addEventListener('click', () => API.logout());
  });
});

// ── REDIRECT IF NOT AUTH ──
function requireAuth(allowedRoles = null) {
  if (!API.isAuthenticated()) {
    window.location.href = '/login';
    return null;
  }
  const user = API.getUser();
  if (allowedRoles && user && !allowedRoles.includes(user.role)) {
    Toast.error('Access denied for your role.');
    return null;
  }
  return user;
}

async function doLogin() {
  const errEl = document.getElementById('login-err');
  if (errEl) {
    errEl.classList.add('hidden');
    errEl.textContent = '';
  }

  const username = document.getElementById('login-username')?.value.trim();
  const password = document.getElementById('login-password')?.value;

  if (!username || !password) {
    if (errEl) {
      errEl.textContent = 'Please enter both username and password.';
      errEl.classList.remove('hidden');
    }
    return;
  }

  try {
    await API.login(username, password);
    window.location.href = '/dashboard';
  } catch (err) {
    const message = err?.data?.detail || 'Login failed. Check your credentials and try again.';
    if (errEl) {
      errEl.textContent = message;
      errEl.classList.remove('hidden');
    } else {
      Toast.error(message);
    }
  }
}

async function doRegister() {
  const errEl = document.getElementById('register-err');
  if (errEl) {
    errEl.classList.add('hidden');
    errEl.textContent = '';
  }

  const data = {
    username: document.getElementById('reg-username')?.value.trim(),
    email: document.getElementById('reg-email')?.value.trim(),
    password: document.getElementById('reg-password')?.value,
    first_name: document.getElementById('reg-firstname')?.value.trim(),
    last_name: document.getElementById('reg-lastname')?.value.trim(),
    organization: document.getElementById('reg-org')?.value.trim(),
    role: typeof selectedRole !== 'undefined' ? selectedRole : 'STUDENT',
  };

  if (!data.username || !data.email || !data.password) {
    if (errEl) {
      errEl.textContent = 'Username, email, and password are required.';
      errEl.classList.remove('hidden');
    }
    return;
  }

  if (data.role === 'VENDOR') {
    data.pickup_location = document.getElementById('reg-pickup')?.value.trim();
    data.dropoff_location = document.getElementById('reg-dropoff')?.value.trim();
  }

  try {
    await API.register(data);
    Toast.success('Registration successful! Please sign in.');
    switchTab('login');
  } catch (err) {
    const errorData = err.response?.data || err.data;
    
    let message = 'Registration failed. Please try again.';

    // 2. Parse Django's field-specific errors if they exist
    if (errorData && typeof errorData === 'object') {
        // If Django sent a specific error message string array
        message = Object.entries(errorData)
            .map(([field, errors]) => {
                // Capitalize field name and join errors (e.g., "Email: This field is required.")
                const fieldName = field.charAt(0).toUpperCase() + field.slice(1);
                const fieldErrors = Array.isArray(errors) ? errors.join(' ') : errors;
                return `${fieldName}: ${fieldErrors}`;
            })
            .join('\n'); // Separates multiple field errors with a new line
    } else if (typeof errorData === 'string') {
        message = errorData;
    }

    if (errEl) {
      errEl.textContent = message;
      errEl.classList.remove('hidden');
    } else {
      Toast.error(message);
    }
  }
}  

// Export for global use
window.API = API;
window.Toast = Toast;
window.openModal = openModal;
window.closeModal = closeModal;
window.fmtDate = fmtDate;
window.fmtDateTime = fmtDateTime;
window.fmtKES = fmtKES;
window.statusBadge = statusBadge;
window.drawDonut = drawDonut;
window.drawBarChart = drawBarChart;
window.requireAuth = requireAuth;
window.doLogin = doLogin;
window.doRegister = doRegister;
