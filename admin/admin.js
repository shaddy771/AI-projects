const $ = (s) => document.querySelector(s);
const loginScreen = $("#login-screen");
const app = $("#app");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(opts.headers || {}) },
    credentials: "same-origin",
    ...opts,
  });
  if (res.status === 401) {
    loginScreen.hidden = false;
    app.hidden = true;
    throw new Error("auth");
  }
  return res;
}

$("#login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const password = $("#password").value;
  const res = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
    credentials: "same-origin",
  });
  if (res.ok) {
    loginScreen.hidden = true;
    app.hidden = false;
    loadAll();
  } else if (res.status === 429) {
    alert("Слишком много попыток. Подождите 5 минут.");
  } else {
    alert("Неверный пароль");
  }
});

$("#btn-logout").addEventListener("click", async () => {
  await fetch("/api/logout", { method: "POST", credentials: "same-origin" });
  loginScreen.hidden = false;
  app.hidden = true;
});

$("#btn-rebuild").addEventListener("click", async () => {
  $("#log").hidden = false;
  $("#log").textContent = "Сборка сайта...";
  const res = await api("/api/rebuild", { method: "POST" });
  const data = await res.json();
  $("#log").textContent = data.output || (data.ok ? "Готово!" : "Ошибка");
  if (data.ok) loadStats();
});

$("#btn-cancel").addEventListener("click", () => {
  $("#editor").hidden = true;
});

$("#edit-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const slug = $("#edit-slug").value;
  const body = {
    title: $("#edit-title").value,
    desc: $("#edit-desc").value,
    date: $("#edit-date").value,
    status: $("#edit-status").value,
    img: $("#edit-img").value,
    keywords: $("#edit-keywords").value,
    content: $("#edit-content").value,
  };
  await api(`/api/articles/${encodeURIComponent(slug)}`, { method: "PATCH", body: JSON.stringify(body) });
  $("#editor").hidden = true;
  loadArticles();
  loadStats();
});

$("#search").addEventListener("input", () => renderArticles(window._articles || []));

async function loadStats() {
  const res = await api("/api/stats");
  const s = await res.json();
  $("#stats").innerHTML = `
    <div class="stat"><div class="stat__num">${escapeHtml(s.total)}</div><div class="stat__label">Всего статей</div></div>
    <div class="stat"><div class="stat__num">${escapeHtml(s.published)}</div><div class="stat__label">Опубликовано</div></div>
    <div class="stat"><div class="stat__num">${escapeHtml(s.scheduled)}</div><div class="stat__label">Запланировано</div></div>
    <div class="stat"><div class="stat__num">${escapeHtml(s.next_publish || "—")}</div><div class="stat__label">След. публикация</div></div>`;
}

async function loadArticles() {
  const res = await api("/api/articles");
  window._articles = await res.json();
  renderArticles(window._articles);
}

function renderArticles(list) {
  const q = ($("#search").value || "").toLowerCase();
  const filtered = list.filter((a) => !q || a.title.toLowerCase().includes(q) || a.slug.includes(q));
  $("#articles-count").textContent = `(${filtered.length})`;
  const tbody = $("#articles-body");
  tbody.innerHTML = filtered.map((a) => {
    const cls = a.status === "published" ? "badge--pub" : a.status === "draft" ? "badge--draft" : "badge--sched";
    const label = a.status === "published" ? "Опубликовано" : a.status === "draft" ? "Черновик" : "Запланировано";
    return `<tr>
      <td>${escapeHtml(a.date)}</td>
      <td>${escapeHtml(a.title)}</td>
      <td><span class="badge ${cls}">${label}</span></td>
      <td><button class="btn btn--sm" data-slug="${escapeHtml(a.slug)}">Изм.</button></td>
    </tr>`;
  }).join("");
  tbody.querySelectorAll("button[data-slug]").forEach((btn) => {
    btn.addEventListener("click", () => openEditor(btn.dataset.slug));
  });
}

async function openEditor(slug) {
  const res = await api(`/api/articles/${encodeURIComponent(slug)}`);
  const a = await res.json();
  $("#edit-slug").value = a.slug;
  $("#edit-title").value = a.title;
  $("#edit-desc").value = a.desc || "";
  $("#edit-date").value = a.date;
  $("#edit-status").value = a.status || "scheduled";
  $("#edit-img").value = a.img || "door-unlock";
  $("#edit-keywords").value = a.keywords || "";
  $("#edit-content").value = a.content || "";
  $("#editor").hidden = false;
  $("#editor").scrollIntoView({ behavior: "smooth" });
}

function loadAll() {
  loadStats();
  loadArticles();
}

loadAll().catch(() => {});
