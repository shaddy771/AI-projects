import { createOrbitalDial } from './orbital.js'

export function mountApp(root) {
  root.innerHTML = `
    <div class="ambient" data-ambient aria-hidden="true"></div>

    <header class="site-header">
      <a class="logo" href="#top">AERO</a>
      <nav class="nav">
        <a href="#dial">Климат</a>
        <a href="#models">Линейка</a>
        <a class="nav-cta" href="#order">Подобрать</a>
      </nav>
    </header>

    <main id="top">
      <section class="hero" id="dial">
        <div class="hero-center">
          <div class="hero-copy">
            <p class="eyebrow">Orbital · 2034</p>
            <h1>Крути — и&nbsp;комната слушается</h1>
            <p class="lede">
              Одно кольцо вместо десяти экранов. Настрой климат жестом —
              и подбери AERO под свою комнату.
            </p>
          </div>

          <div class="dial-wrap">
            <div class="dial-stage" data-dial-root></div>
            <p class="dial-hint">Крути центральную ручку</p>
            <ul class="hero-points">
              <li data-point="cool">16–19° · охлаждение</li>
              <li data-point="comfort">20–23° · комфорт</li>
              <li data-point="warm">24–30° · тепло</li>
            </ul>
          </div>
        </div>

        <div class="hero-meta">
          <div class="meta-card" data-meta-power>
            <span class="meta-label">Мощность</span>
            <span class="meta-value" data-power>2.8 кВт</span>
          </div>
          <div class="meta-card" data-meta-area>
            <span class="meta-label">Комната</span>
            <span class="meta-value" data-area>до 35 м²</span>
          </div>
          <div class="meta-card" data-meta-noise>
            <span class="meta-label">Тишина</span>
            <span class="meta-value" data-noise>19 dB</span>
          </div>
        </div>
      </section>

      <section class="section models" id="models">
        <div class="section-inner">
          <p class="eyebrow">Линейка</p>
          <h2>Три орбиты — один принцип</h2>
          <ul class="model-list">
            <li>
              <span class="model-name">AERO S9</span>
              <span class="model-spec">до 25 м² · 2.5 кВт</span>
              <span class="model-price">54 900 ₽</span>
            </li>
            <li class="is-focus">
              <span class="model-badge">Выбор</span>
              <span class="model-name">AERO S12</span>
              <span class="model-spec">до 35 м² · 2.8 кВт</span>
              <span class="model-price">62 900 ₽</span>
            </li>
            <li>
              <span class="model-name">AERO S18</span>
              <span class="model-spec">до 50 м² · 5.2 кВт</span>
              <span class="model-price">78 900 ₽</span>
            </li>
          </ul>
        </div>
      </section>

      <section class="section order" id="order">
        <div class="section-inner order-panel">
          <p class="eyebrow">Подбор</p>
          <h2>Сохраним ваш климат</h2>
          <p class="section-lede">
            Оставьте контакт — инженер перезвонит и подберёт AERO под выбранную температуру
            <span data-order-temp>22</span>°C.
          </p>
          <form class="order-form" data-form>
            <label>
              <span>Телефон</span>
              <input type="tel" name="phone" placeholder="+7" required />
            </label>
            <label>
              <span>Комната</span>
              <select name="room" required>
                <option value="" disabled selected>Выберите</option>
                <option value="bedroom">Спальня</option>
                <option value="living">Гостиная</option>
                <option value="office">Кабинет</option>
              </select>
            </label>
            <button class="btn btn-primary" type="submit">Подобрать AERO</button>
          </form>
          <p class="form-note" data-note hidden>Настройки сохранены — скоро свяжемся.</p>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <span>AERO</span>
      <span>Климат · без лишнего интерфейса</span>
    </footer>
  `

  const ambient = root.querySelector('[data-ambient]')
  const orderTemp = root.querySelector('[data-order-temp]')
  const powerEl = root.querySelector('[data-power]')
  const areaEl = root.querySelector('[data-area]')
  const points = root.querySelectorAll('[data-point]')

  createOrbitalDial(root.querySelector('[data-dial-root]'), {
    onChange: (temp, mood) => {
      orderTemp.textContent = String(temp)
      const pointKey = mood.mode === 'hot' ? 'warm' : mood.mode
      points.forEach((el) => {
        el.classList.toggle('is-active', el.dataset.point === pointKey)
      })

      if (temp <= 19) {
        powerEl.textContent = '3.2 кВт'
        areaEl.textContent = 'до 25 м²'
      } else if (temp <= 23) {
        powerEl.textContent = '2.8 кВт'
        areaEl.textContent = 'до 35 м²'
      } else {
        powerEl.textContent = '2.5 кВт'
        areaEl.textContent = 'до 25 м²'
      }
    },
  })

  initAmbientPointer(root)
  initForm(root)
  initReveal(root)
}

function initAmbientPointer(root) {
  const ambient = root.querySelector('[data-ambient]')
  if (!ambient) return

  window.addEventListener(
    'pointermove',
    (event) => {
      const x = (event.clientX / window.innerWidth) * 100
      const y = (event.clientY / window.innerHeight) * 100
      ambient.style.setProperty('--mx', `${x}%`)
      ambient.style.setProperty('--my', `${y}%`)
    },
    { passive: true }
  )
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
  const items = root.querySelectorAll('.section, .hero-meta, .model-list li')
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
    { threshold: 0.12 }
  )

  items.forEach((el) => io.observe(el))
}
