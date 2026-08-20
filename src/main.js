import './style.css';
import { WallScene, LAYERS } from './wallScene.js';

const app = document.querySelector('#app');

app.innerHTML = `
  <section class="hero" aria-label="Главный блок ТИШЬ">
    <div class="hero__atmosphere" aria-hidden="true"></div>

    <div class="hero__copy">
      <p class="brand">ТИШ<span>Ь</span></p>
      <h1 class="hero__headline">Стена, которая слышит меньше вас</h1>
      <p class="hero__lead">
        Соберите шумоизоляцию в разрезе — и сразу увидите, на сколько децибел тише станет квартира.
      </p>
      <div class="hero__cta">
        <button class="btn btn--primary" type="button" data-action="consult">Рассчитать объект</button>
        <button class="btn btn--ghost" type="button" data-action="demo">Посмотреть слои</button>
      </div>
    </div>

    <div class="hero__stage">
      <canvas id="wall-canvas" aria-label="Интерактивная стена в разрезе"></canvas>

      <div class="stage-ui">
        <div class="noise-meter" aria-live="polite">
          <div class="noise-meter__label" id="db-label">Шум снижен на</div>
          <div class="noise-meter__value"><strong id="db-value">0</strong><span>дБ</span></div>
          <div class="noise-meter__bar">
            <div class="noise-meter__fill" id="db-fill"></div>
          </div>
        </div>

        <div class="layer-hints" id="layer-hints">
          ${LAYERS.map(
            (layer) => `
            <div class="layer-hint" data-layer="${layer.id}">
              <div class="layer-hint__name">${layer.name}</div>
              <div class="layer-hint__db">${
                layer.db > 0 ? `+${layer.db} дБ к тишине` : 'База конструкции'
              }</div>
            </div>
          `,
          ).join('')}
        </div>

        <div class="controls">
          <div class="controls__row">
            <span class="controls__label">Разрез стены</span>
            <input
              class="slider"
              id="explode-slider"
              type="range"
              min="0"
              max="100"
              value="0"
              aria-label="Собрать или разобрать стену"
            />
          </div>
          <div class="controls__row">
            <span class="controls__label">Действия</span>
            <div class="controls__actions">
              <button class="chip" type="button" id="btn-assemble">Собрать</button>
              <button class="chip" type="button" id="btn-explode">Разобрать</button>
              <button class="chip" type="button" id="btn-auto">Автопоказ</button>
            </div>
          </div>
          <p class="hint-line">Тяните мышью, чтобы вращать · клик по слою — фокус на нём</p>
        </div>
      </div>
    </div>
  </section>
`;

const canvas = document.querySelector('#wall-canvas');
const slider = document.querySelector('#explode-slider');
const dbValue = document.querySelector('#db-value');
const dbLabel = document.querySelector('#db-label');
const dbFill = document.querySelector('#db-fill');
const btnAssemble = document.querySelector('#btn-assemble');
const btnExplode = document.querySelector('#btn-explode');
const btnAuto = document.querySelector('#btn-auto');
const layerHints = [...document.querySelectorAll('.layer-hint')];

let sliderLocked = false;
let displayedDb = 0;

const scene = new WallScene(canvas, {
  onProgressChange({ progress, db, totalDb, visibleLayerIds, autoPlaying }) {
    if (!sliderLocked) {
      slider.value = String(Math.round(progress * 100));
      slider.style.setProperty('--progress', `${progress * 100}%`);
    }

    displayedDb += (db - displayedDb) * 0.14;
    const shown = Math.round(displayedDb);
    dbValue.textContent = String(shown);
    dbLabel.textContent =
      progress < 0.08 ? 'Шум снижен на' : 'Вклад видимых слоёв';
    dbFill.style.width = `${totalDb ? (shown / totalDb) * 100 : 0}%`;

    const visible = new Set(visibleLayerIds);
    for (const hint of layerHints) {
      hint.classList.toggle('is-visible', visible.has(hint.dataset.layer));
    }

    btnAuto.classList.toggle('is-active', autoPlaying);
    btnAssemble.classList.toggle('is-active', progress < 0.05 && !autoPlaying);
    btnExplode.classList.toggle('is-active', progress > 0.95 && !autoPlaying);
  },
});

slider.addEventListener('pointerdown', () => {
  sliderLocked = true;
});
slider.addEventListener('pointerup', () => {
  sliderLocked = false;
});
slider.addEventListener('input', () => {
  const value = Number(slider.value) / 100;
  slider.style.setProperty('--progress', `${slider.value}%`);
  scene.setProgress(value);
});

btnAssemble.addEventListener('click', () => scene.assemble());
btnExplode.addEventListener('click', () => scene.explode());
btnAuto.addEventListener('click', () => {
  scene.toggleAuto();
});

document.querySelector('[data-action="demo"]').addEventListener('click', () => {
  scene.explode();
});

document.querySelector('[data-action="consult"]').addEventListener('click', () => {
  document.querySelector('.controls')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
});

// Gentle intro: assemble → slight explode so layers are discoverable
requestAnimationFrame(() => {
  scene.setProgress(0);
  setTimeout(() => scene.setProgress(0.42), 700);
});
