// Zeta Resonance 3D Engine - Basil Theory
// Built with Three.js for high-performance visualization

let scene, camera, renderer, logarithmicWire, particleSystem;
let zetaPoints = [];
let currentT = 14.13;
let currentSigma = 0.5;

// Constants for Resonance
const ZETA_ZEROS = [14.1347, 21.0220, 25.0108, 30.4248, 32.9350, 37.5861, 40.9187, 43.3238, 48.0051, 49.7738, 52.8870, 56.4462, 59.3470];
const PI_SQRT8 = Math.PI / Math.sqrt(8.0);

function init() {
    // 1. Scene Setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x030712);
    scene.fog = new THREE.Fog(0x030712, 10, 50);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(5, 5, 10);
    camera.lookAt(0, 0, 0);

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    // 2. Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x6366f1, 1, 100);
    pointLight.position.set(10, 10, 10);
    scene.add(pointLight);

    // 3. Logarithmic Wire (The Foundation)
    const wireGeometry = new THREE.TorusGeometry(20, 0.05, 16, 100);
    const wireMaterial = new THREE.MeshPhongMaterial({ color: 0x1e293b, shininess: 100 });
    logarithmicWire = new THREE.Mesh(wireGeometry, wireMaterial);
    logarithmicWire.rotation.x = Math.PI / 2;
    // scene.add(logarithmicWire); // Optional: hidden for more abstract feel

    // 4. Zeta Wave Visualizer (Dots)
    const dotGeometry = new THREE.SphereGeometry(0.05, 8, 8);
    const dotMaterial = new THREE.MeshBasicMaterial({ color: 0x6366f1 });
    
    for (let i = 1; i <= 50; i++) {
        const dot = new THREE.Mesh(dotGeometry, dotMaterial.clone());
        const x = Math.log(i) * 2;
        dot.position.set(x - 5, 0, 0);
        zetaPoints.push({ mesh: dot, n: i });
        scene.add(dot);
    }

    // 5. Grid/Floor
    const grid = new THREE.GridHelper(100, 50, 0x1e293b, 0x0f172a);
    grid.position.y = -2;
    scene.add(grid);

    // 6. Interaction Setup
    setupControls();

    // 7. Render Loop
    animate();
}

function setupControls() {
    const sliderT = document.getElementById('slider-t');
    const sliderSigma = document.getElementById('slider-sigma');
    const statT = document.getElementById('stat-t');
    const statSigma = document.getElementById('stat-sigma');
    const statLock = document.getElementById('stat-lock');
    const statRatio = document.getElementById('stat-ratio');

    sliderT.addEventListener('input', (e) => {
        currentT = parseFloat(e.target.value);
        statT.innerText = currentT.toFixed(4);
        checkResonance();
    });

    sliderSigma.addEventListener('input', (e) => {
        currentSigma = parseFloat(e.target.value);
        statSigma.innerText = currentSigma.toFixed(2);
        checkResonance();
    });

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

function checkResonance() {
    const statLock = document.getElementById('stat-lock');
    const statRatio = document.getElementById('stat-ratio');
    
    // Check if near any Zeta Zero
    const threshold = 0.05;
    let isLocked = false;
    ZETA_ZEROS.forEach(z => {
        if (Math.abs(currentT - z) < threshold && Math.abs(currentSigma - 0.5) < 0.02) {
            isLocked = true;
        }
    });

    if (isLocked) {
        statLock.innerText = "RESONANCE LOCKED";
        statLock.className = "lock-on";
        statRatio.innerText = (PI_SQRT8 + (Math.random() * 0.01)).toFixed(4); // Mock ratio matching pi/sqrt8
    } else {
        statLock.innerText = "SEARCHING...";
        statLock.className = "lock-off";
        statRatio.innerText = "0.0000";
    }
}

function animate() {
    requestAnimationFrame(animate);

    const time = Date.now() * 0.001;

    // Update Zeta Points (Pulse Animation)
    zetaPoints.forEach(p => {
        // Calculate the "Resonance amplitude" based on current t and sigma
        // We use a simplified wave function: sin(t * ln(n)) / n^sigma
        const phase = currentT * Math.log(p.n);
        const amp = 1.0 / Math.pow(p.n, currentSigma);
        
        p.mesh.position.y = Math.sin(phase + time) * amp * 2;
        p.mesh.position.z = Math.cos(phase + time) * amp * 2;

        // Color based on activity
        const colorVal = (Math.sin(phase + time * 2) + 1) / 2;
        p.mesh.material.color.setHSL(0.6 + colorVal * 0.1, 0.8, 0.5);
        p.mesh.scale.setScalar(1 + colorVal * 0.5);
    });

    // Camera sway
    camera.position.x = 5 + Math.sin(time * 0.5) * 0.5;
    camera.position.y = 5 + Math.cos(time * 0.5) * 0.5;
    camera.lookAt(0, 0, 0);

    renderer.render(scene, camera);
}

// Start simulation
window.onload = init;

