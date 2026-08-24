export function mountApp(root) {
  root.innerHTML = `
    <header class="site-header">
      <a class="logo" href="#top" aria-label="SILENCIO — на главную">SILENCIO</a>
      <nav class="nav" aria-label="Основная навигация">
        <a href="#how">Как это работает</a>
        <a href="#systems">Системы</a>
        <a class="nav-cta" href="#cta">Рассчитать</a>
      </nav>
    </header>

    <main id="top">
      <section class="hero" aria-label="До и после шумоизоляции">
        <div
          class="compare"
          data-compare
          style="--pos: 52%"
        >
          <div class="compare-layer compare-after">
            <img
              src="/room-after.png"
              alt="Та же гостиная после акустической отделки — тёплый спокойный свет"
              draggable="false"
            />
            <span class="compare-tag compare-tag-after">После</span>
          </div>

          <div class="compare-layer compare-before" data-before>
            <img
              src="/room-before.png"
              alt="Гостиная до шумоизоляции — холодный городской свет и шум за окном"
              draggable="false"
            />
            <span class="compare-tag compare-tag-before">До</span>
          </div>

          <div class="compare-divider" aria-hidden="true">
            <button
              class="compare-handle"
              type="button"
              data-handle
              aria-label="Сдвиньте, чтобы сравнить до и после"
            >
              <span class="compare-handle-arrows" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="18" height="18">
                  <path d="M14 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M10 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
            </button>
          </div>

          <input
            class="compare-range"
            data-range
            type="range"
            min="4"
            max="96"
            value="52"
            aria-label="Сравнение: до и после шумоизоляции"
          />
        </div>

        <div class="hero-copy">
          <p class="brand-mark">SILENCIO</p>
          <h1>Тишина, которую видно</h1>
          <p class="lede">
            Сдвиньте линию — и комната затихает. Шумоизоляция для стен, пола и потолка без потери стиля.
          </p>
          <div class="cta-row">
            <a class="btn btn-primary" href="#cta">Увидеть разницу</a>
            <a class="btn btn-ghost" href="#systems">Смотреть системы</a>
          </div>
        </div>

        <div class="hero-hint" aria-hidden="true">
          <span>Тяните</span>
          <span class="hero-hint-line"></span>
        </div>
      </section>

      <section class="section section-how" id="how">
        <div class="section-inner">
          <p class="eyebrow">Как это работает</p>
          <h2>Один жест — два состояния комнаты</h2>
          <p class="section-copy">
            Слева — привычный городской шум. Справа — та же планировка после панелей SILENCIO.
            Разница не в фильтре: в материале, плотности и правильном монтаже.
          </p>
        </div>
      </section>

      <section class="section section-systems" id="systems">
        <div class="section-inner">
          <p class="eyebrow">Системы</p>
          <h2>Три уровня тишины под вашу задачу</h2>
          <ul class="systems-list">
            <li>
              <span class="system-name">Soft Wall</span>
              <span class="system-meta">панели · NRC до 0.85</span>
              <span class="system-desc">Для спальни и кабинета: убирает эхо и бытовой шум.</span>
            </li>
            <li>
              <span class="system-name">Dense Frame</span>
              <span class="system-meta">каркас · ΔRw до 18 дБ</span>
              <span class="system-desc">Для стен к соседям и лифтовым шахтам.</span>
            </li>
            <li>
              <span class="system-name">Floor Quiet</span>
              <span class="system-meta">подложка · ударный шум</span>
              <span class="system-desc">Для шагов сверху и жёстких перекрытий.</span>
            </li>
          </ul>
        </div>
      </section>

      <section class="section section-cta" id="cta">
        <div class="section-inner cta-panel">
          <p class="eyebrow">Расчёт</p>
          <h2>Подберём тишину под вашу комнату</h2>
          <p class="section-copy">
            Расскажите площадь, источник шума и бюджет — пришлём схему и смету за один день.
          </p>
          <form class="cta-form" data-form>
            <label>
              <span>Площадь, м²</span>
              <input type="number" name="area" min="5" max="200" placeholder="24" required />
            </label>
            <label>
              <span>Главный шум</span>
              <select name="noise" required>
                <option value="" disabled selected>Выберите</option>
                <option value="neighbors">Соседи / шаги</option>
                <option value="street">Улица / окна</option>
                <option value="tech">Лифт / трубы</option>
              </select>
            </label>
            <button class="btn btn-primary" type="submit">Получить расчёт</button>
          </form>
          <p class="form-note" data-note hidden>Заявка принята — вернёмся с расчётом.</p>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <span>SILENCIO</span>
      <span>Шумоизоляция для спокойного дома</span>
    </footer>
  `

  initCompare(root)
  initForm(root)
  initReveal(root)
}

function initCompare(root) {
  const compare = root.querySelector('[data-compare]')
  const range = root.querySelector('[data-range]')
  const handle = root.querySelector('[data-handle]')
  if (!compare || !range) return

  const setPos = (value) => {
    const clamped = Math.min(96, Math.max(4, Number(value)))
    compare.style.setProperty('--pos', `${clamped}%`)
    range.value = String(clamped)
    compare.dataset.side = clamped < 40 ? 'after' : clamped > 60 ? 'before' : 'mid'
  }

  setPos(range.value)

  range.addEventListener('input', (e) => setPos(e.target.value))

  let dragging = false

  const posFromEvent = (event) => {
    const rect = compare.getBoundingClientRect()
    const clientX = 'touches' in event ? event.touches[0].clientX : event.clientX
    return ((clientX - rect.left) / rect.width) * 100
  }

  const onMove = (event) => {
    if (!dragging) return
    event.preventDefault()
    setPos(posFromEvent(event))
  }

  const stop = () => {
    dragging = false
    compare.classList.remove('is-dragging')
  }

  const start = (event) => {
    dragging = true
    compare.classList.add('is-dragging')
    setPos(posFromEvent(event))
  }

  handle?.addEventListener('pointerdown', (event) => {
    handle.setPointerCapture?.(event.pointerId)
    start(event)
  })

  compare.addEventListener('pointerdown', (event) => {
    if (event.target === range) return
    if (event.target.closest('.hero-copy, .cta-row, a, button:not([data-handle])')) return
    start(event)
  })

  window.addEventListener('pointermove', onMove, { passive: false })
  window.addEventListener('pointerup', stop)
  window.addEventListener('pointercancel', stop)

  // Soft intro: slide from noisy toward quiet once
  requestAnimationFrame(() => {
    compare.classList.add('is-ready')
    let frame = 0
    const from = 78
    const to = 52
    const tick = () => {
      frame += 1
      const t = Math.min(1, frame / 48)
      const eased = 1 - Math.pow(1 - t, 3)
      setPos(from + (to - from) * eased)
      if (t < 1) requestAnimationFrame(tick)
    }
    setTimeout(() => requestAnimationFrame(tick), 500)
  })
}

function initForm(root) {
  const form = root.querySelector('[data-form]')
  const note = root.querySelector('[data-note]')
  if (!form) return

  form.addEventListener('submit', (event) => {
    event.preventDefault()
    form.hidden = true
    if (note) note.hidden = false
  })
}

function initReveal(root) {
  const items = root.querySelectorAll('.section, .systems-list li')
  if (!('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('is-visible'))
    return
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
          io.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.18 }
  )

  items.forEach((el) => io.observe(el))
}
