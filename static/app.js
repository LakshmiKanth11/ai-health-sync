// ============================================================
//  AI Health Sync — Frontend App (calls Flask REST API)
// ============================================================

const API = '';   // same origin
let sessionId = null;
let currentSpecialty = 'general';
let selectedDoctor = null;
let selectedSlot = null;
let selectedDate = null;

// ── Screen Router ─────────────────────────────────────────────
function showScreen(name) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(`screen-${name}`).classList.add('active');
  if (name === 'chat' && !sessionId) initChat();
  if (name === 'booking') loadDoctors('all');
  window.scrollTo(0, 0);
}

// ── Chat ──────────────────────────────────────────────────────
function initChat() {
  sessionId = 'sess-' + Date.now();
  document.getElementById('chat-messages').innerHTML = '';
  updateSidebarSymptoms([]);
  callChatAPI('Hello');   // trigger greeting
}

function resetChat() {
  sessionId = 'sess-' + Date.now();
  document.getElementById('chat-messages').innerHTML = '';
  updateSidebarSymptoms([]);
  callChatAPI('Hello');
}

function handleInputKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function sendQuick(text) {
  showScreen('chat');
  if (!sessionId) { initChat(); setTimeout(() => sendQuick(text), 1200); return; }
  document.getElementById('chat-input').value = text;
  sendMessage();
}

function sendMessage() {
  const input = document.getElementById('chat-input');
  const msg = (input.value || '').trim();
  if (!msg) return;
  if (!sessionId) { initChat(); return; }

  appendMessage('user', msg, '👤');
  input.value = '';
  input.style.height = 'auto';

  const typing = appendTyping();
  document.getElementById('send-btn').disabled = true;

  callChatAPI(msg, typing);
}

async function callChatAPI(message, typingEl = null) {
  if (!sessionId) sessionId = 'sess-' + Date.now();
  try {
    const res = await fetch(`${API}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message }),
    });
    const data = await res.json();
    if (typingEl) typingEl.remove();
    document.getElementById('send-btn').disabled = false;
    handleBotResponse(data);
  } catch (err) {
    if (typingEl) typingEl.remove();
    document.getElementById('send-btn').disabled = false;
    appendMessage('bot', '<p>⚠️ Could not connect to the server. Please ensure Flask is running on port 5000.</p>', '🤖');
  }
}

function handleBotResponse(data) {
  const type = data.type;

  if (type === 'greeting') {
    const html = `
      <p>${md(data.message)}</p>
      <div class="bot-option-grid">
        ${data.quick_options.map(o => `<button class="quick-btn" onclick="sendQuick('${o}')">${o}</button>`).join('')}
      </div>
      <p class="bot-hint">Or type your own symptoms below 👇</p>`;
    appendMessage('bot', html, '🤖');
    return;
  }

  if (type === 'emergency') {
    const html = `
      <div class="emergency-card">
        <div class="emergency-icon">🆘</div>
        <h3>EMERGENCY — Seek Immediate Help</h3>
        <p>Your symptoms may indicate a <strong>life-threatening condition</strong>.</p>
        <div class="emergency-actions">
          <a href="tel:112" class="emergency-btn">📞 Call 112</a>
          <a href="tel:102" class="emergency-btn secondary">🚑 Call 102</a>
        </div>
        <p>Go to the nearest Emergency Room immediately.</p>
      </div>`;
    appendMessage('bot', html, '🤖');
    return;
  }

  if (type === 'followup') {
    const tags = (data.detected || []).map(s => `<span class="symptom-tag">${s}</span>`).join('');
    const html = `<div>${md(data.message)}</div><div style="margin-top:8px">${tags}</div>`;
    appendMessage('bot', html, '🤖');
    updateSidebarSymptoms(data.detected || []);
    return;
  }

  if (type === 'clarify' || type === 'info') {
    appendMessage('bot', `<p>${md(data.message)}</p>`, '🤖');
    return;
  }

  if (type === 'diagnosis') {
    const { results, detected_symptoms, user_age } = data;
    updateSidebarSymptoms(detected_symptoms || []);

    if (!results || results.length === 0) {
      appendMessage('bot', '<p>I couldn\'t find a clear pattern. Please consult a General Physician.</p>', '🤖');
      return;
    }

    const top = results[0];
    const others = results.slice(1);
    const urgencyColors = { low: '#4ade80', moderate: '#fbbf24', high: '#f97316', critical: '#ef4444' };
    const urgencyIcons = { low: '✅', moderate: '⚠️', high: '🚨', critical: '🆘' };
    const urg = top.urgency;
    const ageStr = user_age ? ` · Age: ${user_age}` : '';

    let html = `
      <div class="diagnosis-card">
        <div class="diagnosis-header">
          <span class="diag-emoji">${top.emoji}</span>
          <div>
            <div class="diag-title">ML Analysis Complete${ageStr}</div>
            <div class="diag-sub">${(detected_symptoms || []).length} symptom(s) detected · RandomForest classifier</div>
          </div>
        </div>
        <div class="symptoms-detected">
          <span class="label">NLP Detected Symptoms:</span>
          ${(detected_symptoms || []).map(s => `<span class="symptom-tag">${s}</span>`).join('')}
        </div>
        <div class="primary-diagnosis">
          <div class="diag-row">
            <span class="diag-label">Top Condition</span>
            <span class="diag-cond">${top.emoji} ${top.name}</span>
          </div>
          <div class="confidence-bar-wrap">
            <div class="confidence-bar" style="width:${top.confidence}%"></div>
          </div>
          <div class="confidence-text">ML Confidence: <strong>${top.confidence}%</strong></div>
          <div class="diag-desc">${top.description}</div>
        </div>
        <div class="urgency-badge" style="border-color:${urgencyColors[urg]};color:${urgencyColors[urg]}">
          ${urgencyIcons[urg]} Urgency: <strong>${urg.toUpperCase()}</strong>
        </div>
        <div class="advice-box">
          <span class="advice-label">💡 Advice</span>
          <p>${top.advice}</p>
        </div>`;

    if (others.length > 0) {
      html += `<div class="alt-conditions"><span class="label">Other Possibilities:</span><div class="alt-list">`;
      others.forEach(r => {
        html += `<div class="alt-item"><span>${r.emoji} ${r.name}</span><span class="alt-conf">${r.confidence}%</span></div>`;
      });
      html += `</div></div>`;
    }

    html += `<p class="disclaimer">⚕️ AI assessment only. Not a substitute for professional medical advice.</p>
      <button class="book-appointment-btn" onclick="openBookingForSpecialty('${top.specialty}')">
        📅 Book Appointment with ${top.specialty.replace(/_/g, ' ')} specialist
      </button>
    </div>`;

    appendMessage('bot', html, '🤖');
  }
}

// ── Helpers ───────────────────────────────────────────────────
function appendMessage(role, html, avatar) {
  const wrap = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = `message ${role}`;
  const time = new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  div.innerHTML = `
    <div class="msg-avatar">${avatar}</div>
    <div>
      <div class="msg-bubble">${html}</div>
      <div class="msg-time">${time}</div>
    </div>`;
  wrap.appendChild(div);
  wrap.scrollTop = wrap.scrollHeight;
  return div;
}

function appendTyping() {
  const wrap = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = 'message bot';
  div.innerHTML = `
    <div class="msg-avatar">🤖</div>
    <div class="msg-bubble">
      <div class="typing-indicator">
        <div class="dot"></div><div class="dot"></div><div class="dot"></div>
      </div>
    </div>`;
  wrap.appendChild(div);
  wrap.scrollTop = wrap.scrollHeight;
  return div;
}

function updateSidebarSymptoms(list) {
  const el = document.getElementById('sidebar-symptoms');
  if (!el) return;
  if (!list || list.length === 0) {
    el.innerHTML = '<span style="color:var(--text-muted);font-size:.8rem">None yet</span>';
  } else {
    el.innerHTML = list.map(s => `<span class="symptom-tag">${s}</span>`).join('');
  }
}

// Very basic markdown bold
function md(text) {
  return (text || '').replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
}

// ── Booking ───────────────────────────────────────────────────
function openBookingForSpecialty(specialty) {
  currentSpecialty = specialty;
  showScreen('booking');
  // Activate matching chip
  document.querySelectorAll('.filter-chip').forEach(c => {
    c.classList.toggle('active', c.textContent.toLowerCase().includes(specialty.replace('_', ' ').split(' ')[0]));
  });
  loadDoctors(specialty);
}

async function loadDoctors(specialty) {
  currentSpecialty = specialty;
  const res = await fetch(`${API}/api/doctors?specialty=${specialty}`);
  const doctors = await res.json();
  renderDoctors(doctors);
}

function filterDoctors(specialty, el) {
  document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  loadDoctors(specialty);
}

function renderDoctors(doctors) {
  const el = document.getElementById('doctors-list');
  selectedDoctor = null; selectedSlot = null; selectedDate = null;
  document.getElementById('booking-form-section').innerHTML = `
    <div class="select-doctor-prompt">
      <div style="font-size:3rem;margin-bottom:1rem">👈</div>
      <h3>Select a Doctor</h3>
      <p>Choose from the list to see available slots.</p>
    </div>`;

  el.innerHTML = doctors.map(d => `
    <div class="doctor-card" id="doc-${d.id}" onclick="selectDoctor(${JSON.stringify(d).split('"').join('&quot;')})">
      <div class="doc-avatar" style="background:${d.color}20;color:${d.color}">${d.avatar}</div>
      <div class="doc-info">
        <div class="doc-name">${d.name}</div>
        <div class="doc-title">${d.title}</div>
        <div class="doc-location">📍 ${d.location}</div>
        <div class="doc-meta">
          <span class="doc-rating">⭐ ${d.rating}</span>
          <span class="doc-exp">${d.exp} yrs</span>
          <span class="doc-fee">₹${d.fee}</span>
        </div>
      </div>
      <div class="doc-select-icon">›</div>
    </div>`).join('');
}

function selectDoctor(doc) {
  selectedDoctor = doc;
  document.querySelectorAll('.doctor-card').forEach(c => c.classList.remove('selected'));
  document.getElementById(`doc-${doc.id}`)?.classList.add('selected');
  renderBookingForm(doc);
  document.getElementById('booking-form-section').scrollIntoView({ behavior: 'smooth' });
}

function renderBookingForm(doc) {
  const today = new Date().toISOString().split('T')[0];
  const maxDate = new Date(Date.now() + 30 * 864e5).toISOString().split('T')[0];

  document.getElementById('booking-form-section').innerHTML = `
    <div class="booking-form-card">
      <div class="booking-doc-header">
        <div class="booking-doc-avatar" style="background:${doc.color}20;color:${doc.color}">${doc.avatar}</div>
        <div><h3>${doc.name}</h3><p>${doc.title} · ₹${doc.fee}</p></div>
      </div>
      <div class="form-group">
        <label>📅 Select Date</label>
        <input type="date" id="appt-date" min="${today}" max="${maxDate}" onchange="selectedDate=this.value">
      </div>
      <div class="form-group">
        <label>⏰ Time Slot</label>
        <div class="slots-grid">
          ${doc.slots.map(s => `<button class="slot-btn" onclick="selectSlot('${s}',this)">${s}</button>`).join('')}
        </div>
      </div>
      <div class="form-group">
        <label>👤 Your Full Name</label>
        <input type="text" id="appt-name" placeholder="Enter your name" oninput="this.classList.remove('error')">
      </div>
      <div class="form-group">
        <label>📱 Phone Number</label>
        <input type="tel" id="appt-phone" placeholder="+91 XXXXX XXXXX" oninput="this.classList.remove('error')">
      </div>
      <div class="form-group">
        <label>📝 Reason for Visit</label>
        <textarea id="appt-reason" placeholder="Brief description of your symptoms or reason…" rows="3"></textarea>
      </div>
      <button class="book-btn" onclick="submitBooking()">✅ Confirm Appointment</button>
    </div>`;
}

function selectSlot(slot, el) {
  selectedSlot = slot;
  document.querySelectorAll('.slot-btn').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
}

async function submitBooking() {
  const name = document.getElementById('appt-name')?.value.trim();
  const phone = document.getElementById('appt-phone')?.value.trim();
  const reason = document.getElementById('appt-reason')?.value.trim();
  let valid = true;

  if (!name) { document.getElementById('appt-name').classList.add('error'); valid = false; }
  if (!phone || phone.length < 7) { document.getElementById('appt-phone').classList.add('error'); valid = false; }
  if (!selectedSlot) { showToast('Please select a time slot', 'warn'); valid = false; }
  if (!selectedDate) { showToast('Please select a date', 'warn'); valid = false; }
  if (!valid) { showToast('Fill in all required fields', 'error'); return; }

  try {
    const res = await fetch(`${API}/api/book`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        doctor_id: selectedDoctor.id,
        patient_name: name, patient_phone: phone,
        appt_date: selectedDate, appt_slot: selectedSlot,
        reason: reason || 'General consultation',
      }),
    });
    const data = await res.json();
    if (data.success) showConfirmation(data.appointment);
    else showToast('Booking failed: ' + (data.error || 'unknown'), 'error');
  } catch (e) {
    showToast('Server error. Please try again.', 'error');
  }
}

function showConfirmation(appt) {
  const dateStr = new Date(appt.date).toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  document.getElementById('booking-form-section').innerHTML = `
    <div class="confirmation-card">
      <div class="confirm-icon">✅</div>
      <h2 class="confirm-title">Appointment Confirmed!</h2>
      <p class="confirm-sub">Your appointment was successfully booked.</p>
      <div class="confirm-details">
        <div class="confirm-row"><span>👨‍⚕️ Doctor</span><strong>${appt.doctor.name}</strong></div>
        <div class="confirm-row"><span>🏥 Specialty</span><strong>${appt.doctor.title}</strong></div>
        <div class="confirm-row"><span>📅 Date</span><strong>${dateStr}</strong></div>
        <div class="confirm-row"><span>⏰ Time</span><strong>${appt.slot}</strong></div>
        <div class="confirm-row"><span>👤 Patient</span><strong>${appt.patient_name}</strong></div>
        <div class="confirm-row"><span>📍 Location</span><strong>${appt.doctor.location}</strong></div>
        <div class="confirm-row"><span>💰 Fee</span><strong>₹${appt.doctor.fee}</strong></div>
      </div>
      <div class="confirm-id">Booking ID: #${String(appt.id).padStart(8, '0')}</div>
      <div class="confirm-actions">
        <button class="btn-primary" onclick="showScreen('chat')">🔄 New Assessment</button>
        <button class="btn-secondary" onclick="showAllAppointments()">📋 My Appointments</button>
      </div>
    </div>`;
  showToast('Appointment booked successfully! 🎉', 'success');
}

async function showAllAppointments() {
  const res = await fetch(`${API}/api/appointments`);
  const list = await res.json();

  const modal = document.createElement('div');
  modal.className = 'modal-overlay';
  modal.id = 'appt-modal';

  const body = list.length === 0
    ? '<p style="color:var(--text-muted);text-align:center;padding:2rem">No appointments booked yet.</p>'
    : list.map(a => {
      const d = new Date(a.date).toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric' });
      const slotsJson = JSON.stringify(a.doctor?.slots || []).replace(/"/g, '&quot;');
      return `<div class="history-item" id="hi-${a.id}">
              <div class="hi-avatar" style="background:${a.doctor?.color || '#8b5cf6'}20;color:${a.doctor?.color || '#8b5cf6'}">${a.doctor?.avatar || '?'}</div>
              <div class="hi-info">
                <div class="hi-doc">${a.doctor?.name || 'Unknown'}</div>
                <div class="hi-meta">📅 ${d} · ⏰ ${a.slot}</div>
                <div class="hi-patient">👤 ${a.patient_name} · 📱 ${a.patient_phone}</div>
                ${a.reason ? `<div class="hi-reason">📝 ${a.reason}</div>` : ''}
              </div>
              <div class="hi-actions">
                <span class="hi-status">✅ Confirmed</span>
                <div class="hi-btns">
                  <button class="hi-edit-btn" onclick="openEditModal(${a.id},'${a.date}','${a.slot}',${JSON.stringify(a.reason || '').replace(/"/g, '&quot;')},${slotsJson})">✏️ Edit</button>
                  <button class="hi-cancel-btn" onclick="confirmCancel(${a.id})">🗑️ Cancel</button>
                </div>
              </div>
            </div>`;
    }).join('');

  modal.innerHTML = `
    <div class="modal-box" style="max-width:600px">
      <div class="modal-header">
        <h3>📋 My Appointments</h3>
        <button onclick="document.getElementById('appt-modal').remove()">✕</button>
      </div>
      <div class="modal-body" id="modal-body-content">${body}</div>
    </div>`;
  document.body.appendChild(modal);
}

// ── Cancel ────────────────────────────────────────────────────
function confirmCancel(apptId) {
  // Inline confirm inside the modal
  const existing = document.getElementById(`confirm-${apptId}`);
  if (existing) { existing.remove(); return; }

  const row = document.getElementById(`hi-${apptId}`);
  const confirm = document.createElement('div');
  confirm.id = `confirm-${apptId}`;
  confirm.className = 'cancel-confirm-bar';
  confirm.innerHTML = `
      <span>⚠️ Cancel this appointment?</span>
      <div style="display:flex;gap:8px">
        <button class="confirm-yes-btn" onclick="doCancel(${apptId})">Yes, Cancel</button>
        <button class="confirm-no-btn"  onclick="document.getElementById('confirm-${apptId}').remove()">Keep It</button>
      </div>`;
  row.after(confirm);
}

async function doCancel(apptId) {
  try {
    const res = await fetch(`${API}/api/appointments/${apptId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      document.getElementById(`hi-${apptId}`)?.remove();
      document.getElementById(`confirm-${apptId}`)?.remove();
      showToast('Appointment cancelled successfully.', 'success');
      // Show empty state if no more appointments
      const body = document.getElementById('modal-body-content');
      if (body && !body.querySelector('.history-item')) {
        body.innerHTML = '<p style="color:var(--text-muted);text-align:center;padding:2rem">No appointments booked yet.</p>';
      }
    } else {
      showToast(data.error || 'Failed to cancel.', 'error');
    }
  } catch (e) {
    showToast('Server error. Try again.', 'error');
  }
}

// ── Edit ──────────────────────────────────────────────────────
function openEditModal(apptId, currentDate, currentSlot, currentReason, slots) {
  // Remove any existing edit modal
  document.getElementById('edit-modal')?.remove();

  const today = new Date().toISOString().split('T')[0];
  const maxDate = new Date(Date.now() + 30 * 864e5).toISOString().split('T')[0];
  const slotBtns = (slots || []).map(s =>
    `<button class="slot-btn ${s === currentSlot ? 'active' : ''}" onclick="editSelectSlot('${s}',this)">${s}</button>`
  ).join('');

  const modal = document.createElement('div');
  modal.className = 'modal-overlay';
  modal.id = 'edit-modal';
  modal.innerHTML = `
    <div class="modal-box" style="max-width:440px">
      <div class="modal-header">
        <h3>✏️ Edit Appointment</h3>
        <button onclick="document.getElementById('edit-modal').remove()">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>📅 New Date</label>
          <input type="date" id="edit-date" min="${today}" max="${maxDate}" value="${currentDate}"
                 onchange="editSelectedDate=this.value">
        </div>
        <div class="form-group">
          <label>⏰ New Time Slot</label>
          <div class="slots-grid">${slotBtns}</div>
        </div>
        <div class="form-group">
          <label>📝 Reason for Visit</label>
          <textarea id="edit-reason" rows="3">${currentReason || ''}</textarea>
        </div>
        <div style="display:flex;gap:10px;margin-top:1rem">
          <button class="book-btn" style="flex:1" onclick="submitEdit(${apptId})">💾 Save Changes</button>
          <button class="book-btn" style="flex:0 0 auto;background:var(--bg-secondary);color:var(--text-secondary)" onclick="document.getElementById('edit-modal').remove()">Cancel</button>
        </div>
      </div>
    </div>`;
  document.body.appendChild(modal);

  // Init edit slot tracking
  window.editSelectedSlot = currentSlot;
  window.editSelectedDate = currentDate;
}

function editSelectSlot(slot, el) {
  window.editSelectedSlot = slot;
  document.querySelectorAll('#edit-modal .slot-btn').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
}

async function submitEdit(apptId) {
  const date = window.editSelectedDate;
  const slot = window.editSelectedSlot;
  const reason = document.getElementById('edit-reason')?.value.trim();

  if (!date) { showToast('Please select a date', 'warn'); return; }
  if (!slot) { showToast('Please select a time slot', 'warn'); return; }

  try {
    const res = await fetch(`${API}/api/appointments/${apptId}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ appt_date: date, appt_slot: slot, reason }),
    });
    const data = await res.json();
    if (data.success) {
      document.getElementById('edit-modal').remove();
      showToast('Appointment updated successfully! ✅', 'success');
      // Refresh the appointments modal
      document.getElementById('appt-modal')?.remove();
      setTimeout(showAllAppointments, 300);
    } else {
      showToast(data.error || 'Update failed.', 'error');
    }
  } catch (e) {
    showToast('Server error. Try again.', 'error');
  }
}

// ── Toast ─────────────────────────────────────────────────────
function showToast(msg, type = 'info') {
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.textContent = msg;
  document.getElementById('toast-container').appendChild(t);
  requestAnimationFrame(() => { requestAnimationFrame(() => t.classList.add('show')); });
  setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 400); }, 3500);
}

// ── Init ──────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  showScreen('landing');
});
