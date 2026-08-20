import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

/**
 * Layers from room side outward (index 0 = finishing, last = bearing wall).
 * explodeOffset moves layers apart along X for the cutaway view.
 */
export const LAYERS = [
  {
    id: 'finish',
    name: 'Финиш',
    subtitle: 'Шпаклёвка и краска',
    color: 0xe8e0d4,
    roughness: 0.72,
    metalness: 0.02,
    thickness: 0.08,
    height: 2.55,
    width: 2.2,
    db: 2,
    explodeOffset: 0.95,
  },
  {
    id: 'gkl',
    name: 'Акустический ГКЛ',
    subtitle: 'Утяжелённый лист 12.5 мм',
    color: 0xc9d4c8,
    roughness: 0.8,
    metalness: 0.0,
    thickness: 0.14,
    height: 2.5,
    width: 2.15,
    db: 12,
    explodeOffset: 0.55,
  },
  {
    id: 'wool',
    name: 'Каркас + минвата',
    subtitle: 'Профиль и базальтовая плита',
    color: 0x8fa88f,
    roughness: 0.95,
    metalness: 0.0,
    thickness: 0.55,
    height: 2.48,
    width: 2.1,
    db: 18,
    explodeOffset: 0.15,
    fibrous: true,
  },
  {
    id: 'membrane',
    name: 'Вибромембрана',
    subtitle: 'Демпфирующий слой',
    color: 0x2f3a42,
    roughness: 0.55,
    metalness: 0.15,
    thickness: 0.06,
    height: 2.46,
    width: 2.08,
    db: 8,
    explodeOffset: -0.25,
  },
  {
    id: 'wall',
    name: 'Несущая стена',
    subtitle: 'Бетон / кирпич',
    color: 0x6d7378,
    roughness: 0.92,
    metalness: 0.05,
    thickness: 0.85,
    height: 2.7,
    width: 2.4,
    db: 0,
    explodeOffset: -0.75,
  },
];

const TOTAL_DB = LAYERS.reduce((sum, layer) => sum + layer.db, 0);

function createNoiseTexture(size = 128, contrast = 0.12) {
  const data = new Uint8Array(size * size * 4);
  for (let i = 0; i < size * size; i += 1) {
    const v = Math.floor((0.5 + (Math.random() - 0.5) * contrast) * 255);
    const o = i * 4;
    data[o] = v;
    data[o + 1] = v;
    data[o + 2] = v;
    data[o + 3] = 255;
  }
  const texture = new THREE.DataTexture(data, size, size);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.needsUpdate = true;
  return texture;
}

function createFibrousMaterial(baseColor) {
  const canvas = document.createElement('canvas');
  canvas.width = 128;
  canvas.height = 128;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#7f967f';
  ctx.fillRect(0, 0, 128, 128);
  for (let i = 0; i < 900; i += 1) {
    const x = Math.random() * 128;
    const y = Math.random() * 128;
    ctx.strokeStyle = `rgba(${90 + Math.random() * 40}, ${110 + Math.random() * 30}, ${85 + Math.random() * 25}, 0.35)`;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + (Math.random() - 0.5) * 10, y + (Math.random() - 0.5) * 10);
    ctx.stroke();
  }
  const map = new THREE.CanvasTexture(canvas);
  map.wrapS = THREE.RepeatWrapping;
  map.wrapT = THREE.RepeatWrapping;
  map.repeat.set(3, 4);
  return new THREE.MeshStandardMaterial({
    color: baseColor,
    map,
    roughness: 0.95,
    metalness: 0,
  });
}

export class WallScene {
  constructor(canvas, { onProgressChange } = {}) {
    this.canvas = canvas;
    this.onProgressChange = onProgressChange;
    this.progress = 0;
    this.targetProgress = 0;
    this.autoPlaying = false;
    this.autoDirection = 1;
    this.raycaster = new THREE.Raycaster();
    this.pointer = new THREE.Vector2();
    this.layerMeshes = [];
    this.clock = new THREE.Clock();
    this.disposed = false;

    this.#init();
    this.#buildWall();
    this.#bindEvents();
    this.#animate();
  }

  #init() {
    const { clientWidth: w, clientHeight: h } = this.canvas.parentElement;

    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance',
    });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setSize(w, h, false);
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.05;
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    this.scene = new THREE.Scene();

    this.camera = new THREE.PerspectiveCamera(38, w / h, 0.1, 40);
    this.camera.position.set(3.6, 1.35, 4.2);

    this.controls = new OrbitControls(this.camera, this.canvas);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.06;
    this.controls.minDistance = 2.8;
    this.controls.maxDistance = 8;
    this.controls.minPolarAngle = 0.7;
    this.controls.maxPolarAngle = 1.55;
    this.controls.target.set(0, 1.15, 0);
    this.controls.update();

    const hemi = new THREE.HemisphereLight(0xdde6ea, 0x2a3238, 1.15);
    this.scene.add(hemi);

    const key = new THREE.DirectionalLight(0xfff2e0, 1.35);
    key.position.set(4.5, 6, 3.5);
    key.castShadow = true;
    key.shadow.mapSize.set(1024, 1024);
    key.shadow.camera.near = 1;
    key.shadow.camera.far = 20;
    key.shadow.camera.left = -4;
    key.shadow.camera.right = 4;
    key.shadow.camera.top = 4;
    key.shadow.camera.bottom = -4;
    this.scene.add(key);

    const fill = new THREE.DirectionalLight(0x8eb9b0, 0.55);
    fill.position.set(-3, 2.5, -2);
    this.scene.add(fill);

    const rim = new THREE.DirectionalLight(0xc45c4a, 0.25);
    rim.position.set(-1, 1.5, 4);
    this.scene.add(rim);

    const ground = new THREE.Mesh(
      new THREE.CircleGeometry(4.2, 64),
      new THREE.MeshStandardMaterial({
        color: 0x1c242a,
        roughness: 0.95,
        metalness: 0.05,
      }),
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = 0;
    ground.receiveShadow = true;
    this.scene.add(ground);

    const noiseMap = createNoiseTexture(64, 0.2);
    noiseMap.repeat.set(6, 6);
    const floorAccent = new THREE.Mesh(
      new THREE.RingGeometry(1.6, 2.55, 64),
      new THREE.MeshStandardMaterial({
        color: 0x263038,
        roughness: 1,
        metalness: 0,
        map: noiseMap,
        transparent: true,
        opacity: 0.55,
      }),
    );
    floorAccent.rotation.x = -Math.PI / 2;
    floorAccent.position.y = 0.002;
    this.scene.add(floorAccent);
  }

  #buildWall() {
    this.wallGroup = new THREE.Group();
    this.wallGroup.position.set(0, 0, 0);
    this.scene.add(this.wallGroup);

    let cursorX = 0;
    const stack = [];

    // Build from bearing wall (deepest) to finish so packing is correct when assembled
    const ordered = [...LAYERS].reverse();
    for (const layer of ordered) {
      const material = layer.fibrous
        ? createFibrousMaterial(layer.color)
        : new THREE.MeshStandardMaterial({
            color: layer.color,
            roughness: layer.roughness,
            metalness: layer.metalness,
            map: createNoiseTexture(96, layer.id === 'wall' ? 0.22 : 0.1),
          });

      const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(layer.thickness, layer.height, layer.width),
        material,
      );
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      mesh.userData.layerId = layer.id;
      mesh.userData.baseX = cursorX + layer.thickness / 2;
      mesh.userData.explodeX = mesh.userData.baseX + layer.explodeOffset;
      mesh.position.set(mesh.userData.baseX, layer.height / 2, 0);

      // Cutaway bevel edge highlight via thin darker rim plate on +Z face edge
      const edge = new THREE.Mesh(
        new THREE.BoxGeometry(layer.thickness * 0.98, layer.height * 0.985, 0.012),
        new THREE.MeshStandardMaterial({
          color: 0x10161a,
          roughness: 0.6,
          metalness: 0.2,
          transparent: true,
          opacity: 0.35,
        }),
      );
      edge.position.set(0, 0, layer.width / 2 + 0.004);
      mesh.add(edge);

      this.wallGroup.add(mesh);
      stack.push(mesh);
      cursorX += layer.thickness;
    }

    // Reorder layerMeshes to match LAYERS order (finish → wall)
    this.layerMeshes = LAYERS.map((layer) =>
      stack.find((mesh) => mesh.userData.layerId === layer.id),
    );

    // Center the assembled stack around origin
    const totalThickness = ordered.reduce((s, l) => s + l.thickness, 0);
    this.wallGroup.position.x = -totalThickness / 2;

    // Soft room silhouette behind wall
    const roomHint = new THREE.Mesh(
      new THREE.PlaneGeometry(3.4, 2.9),
      new THREE.MeshStandardMaterial({
        color: 0x243038,
        roughness: 1,
        metalness: 0,
        transparent: true,
        opacity: 0.45,
      }),
    );
    roomHint.position.set(-0.15, 1.35, -1.35);
    this.scene.add(roomHint);

    this.#addStuds();
  }

  #addStuds() {
    const wool = this.layerMeshes.find((m) => m.userData.layerId === 'wool');
    if (!wool) return;

    const studMat = new THREE.MeshStandardMaterial({
      color: 0xb8c0c6,
      metalness: 0.65,
      roughness: 0.35,
    });

    for (const z of [-0.7, 0, 0.7]) {
      const stud = new THREE.Mesh(new THREE.BoxGeometry(0.05, 2.35, 0.05), studMat);
      stud.position.set(0, 0, z);
      stud.castShadow = true;
      wool.add(stud);
    }
  }

  #bindEvents() {
    this._onResize = () => this.#resize();
    window.addEventListener('resize', this._onResize);

    this._onClick = (event) => this.#handleClick(event);
    this.canvas.addEventListener('click', this._onClick);
  }

  #resize() {
    const parent = this.canvas.parentElement;
    if (!parent) return;
    const w = parent.clientWidth;
    const h = parent.clientHeight;
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(w, h, false);
  }

  #handleClick(event) {
    const rect = this.canvas.getBoundingClientRect();
    this.pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    this.raycaster.setFromCamera(this.pointer, this.camera);
    const hits = this.raycaster.intersectObjects(this.layerMeshes, false);
    if (!hits.length) return;

    const id = hits[0].object.userData.layerId;
    const index = LAYERS.findIndex((l) => l.id === id);
    if (index < 0) return;

    // Focus progress so this layer (and outer ones) are separated enough to read
    const focus = (index + 1) / LAYERS.length;
    this.setProgress(Math.max(focus, 0.15));
    this.autoPlaying = false;
  }

  setProgress(value) {
    this.targetProgress = THREE.MathUtils.clamp(value, 0, 1);
    this.autoPlaying = false;
  }

  assemble() {
    this.targetProgress = 0;
    this.autoPlaying = false;
  }

  explode() {
    this.targetProgress = 1;
    this.autoPlaying = false;
  }

  toggleAuto() {
    this.autoPlaying = !this.autoPlaying;
    if (this.autoPlaying) {
      this.autoDirection = this.progress >= 0.98 ? -1 : 1;
    }
    return this.autoPlaying;
  }

  getReductionDb() {
    if (this.progress < 0.08) return TOTAL_DB;
    const visible = new Set(this.getVisibleLayerIds());
    return LAYERS.filter((layer) => visible.has(layer.id)).reduce(
      (sum, layer) => sum + layer.db,
      0,
    );
  }

  getVisibleLayerIds() {
    // Reveal labels as layers separate
    if (this.progress < 0.08) return [];
    const count = Math.ceil(this.progress * LAYERS.length);
    return LAYERS.slice(0, count).map((l) => l.id);
  }

  get totalDb() {
    return TOTAL_DB;
  }

  #applyProgress(p) {
    for (const mesh of this.layerMeshes) {
      const { baseX, explodeX } = mesh.userData;
      mesh.position.x = THREE.MathUtils.lerp(baseX, explodeX, p);
    }

    // Subtle camera breathe with explode
    const desiredZ = THREE.MathUtils.lerp(4.2, 4.8, p);
    this.camera.position.z += (desiredZ - this.camera.position.z) * 0.04;
  }

  #animate() {
    if (this.disposed) return;
    requestAnimationFrame(() => this.#animate());

    const dt = Math.min(this.clock.getDelta(), 0.05);

    if (this.autoPlaying) {
      this.targetProgress += this.autoDirection * dt * 0.22;
      if (this.targetProgress >= 1) {
        this.targetProgress = 1;
        this.autoDirection = -1;
      } else if (this.targetProgress <= 0) {
        this.targetProgress = 0;
        this.autoDirection = 1;
      }
    }

    this.progress = THREE.MathUtils.damp(this.progress, this.targetProgress, 6.5, dt);
    this.#applyProgress(this.progress);

    // Gentle idle sway
    const t = this.clock.elapsedTime;
    this.wallGroup.rotation.y = Math.sin(t * 0.25) * 0.03;

    this.controls.update();
    this.renderer.render(this.scene, this.camera);

    if (this.onProgressChange) {
      this.onProgressChange({
        progress: this.progress,
        db: this.getReductionDb(),
        totalDb: this.totalDb,
        visibleLayerIds: this.getVisibleLayerIds(),
        autoPlaying: this.autoPlaying,
      });
    }
  }

  dispose() {
    this.disposed = true;
    window.removeEventListener('resize', this._onResize);
    this.canvas.removeEventListener('click', this._onClick);
    this.controls.dispose();
    this.renderer.dispose();
  }
}
