const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 게임 상태
let gameState = 'menu'; // menu, playing, gameover, success
let selectedAircraft = 0;
let aircrafts = [
  { name: 'Boeing 737', img: 'resources/boeing_737.png' },
  { name: 'Airbus A320', img: 'resources/airbus_a320.png' },
  { name: 'Cessna 172', img: 'resources/cessna_172.png' }
];
let hazardsList = [
  { name: 'Apple', img: 'resources/apple.png' },
  { name: 'Google', img: 'resources/google.png' },
  { name: 'Tesla', img: 'resources/tesla.png' },
  { name: 'Microsoft', img: 'resources/microsoft.png' },
  { name: 'Amazon', img: 'resources/amazon.png' },
  { name: 'Police', img: 'resources/police.png' }
];

let player = { x: 370, y: 500, w: 60, h: 30, speed: 5, img: null };
let hazards = [];
let startTime = 0;
let elapsed = 0;
let score = 0;
let collided = false;

// 이미지 로딩
function loadImage(src) {
  const img = new Image();
  img.src = src;
  return img;
}

// 메뉴 화면
function drawMenu() {
  ctx.clearRect(0, 0, 800, 600);
  ctx.font = '36px Arial';
  ctx.fillStyle = '#222';
  ctx.fillText('Select Your Aircraft', 240, 120);
  aircrafts.forEach((ac, i) => {
    ctx.fillStyle = (i === selectedAircraft) ? '#0077ff' : '#222';
    ctx.fillText(ac.name, 320, 200 + i * 60);
  });
  ctx.font = '20px Arial';
  ctx.fillStyle = '#444';
  ctx.fillText('Use UP/DOWN and ENTER to select', 250, 400);
}

// 게임 초기화
function startGame() {
  player.img = loadImage(aircrafts[selectedAircraft].img);
  player.x = 370; player.y = 500;
  hazards = [];
  for (let i = 0; i < 3; i++) {
    let hz = hazardsList[Math.floor(Math.random() * hazardsList.length)];
    let x = 100 + Math.random() * 600;
    let y = 150 + Math.random() * 300;
    hazards.push({ ...hz, x, y, img: loadImage(hz.img) });
  }
  startTime = Date.now();
  collided = false;
  gameState = 'playing';
}

// 게임 화면
function drawGame() {
  ctx.clearRect(0, 0, 800, 600);
  // 활주로
  ctx.fillStyle = '#aaa';
  ctx.fillRect(100, 500, 600, 60);
  ctx.font = '24px Arial';
  ctx.fillStyle = '#333';
  ctx.fillText('Haneda Airport', 320, 580);

  // 장애물
  hazards.forEach(hz => {
    if (hz.img.complete) ctx.drawImage(hz.img, hz.x - 24, hz.y - 24, 48, 48);
    else {
      ctx.fillStyle = 'red';
      ctx.beginPath();
      ctx.arc(hz.x, hz.y, 24, 0, Math.PI * 2);
      ctx.fill();
    }
  });

  // 비행기
  if (player.img && player.img.complete) ctx.drawImage(player.img, player.x, player.y, player.w, player.h);

  // 타이머
  elapsed = Math.floor((Date.now() - startTime) / 1000);
  ctx.font = '20px Arial';
  ctx.fillStyle = '#0077ff';
  ctx.fillText(`Time: ${elapsed}s`, 680, 40);
}

// 게임 오버/성공 화면
function drawEnd(success) {
  ctx.clearRect(0, 0, 800, 600);
  ctx.font = '48px Arial';
  ctx.fillStyle = success ? '#0a0' : '#c00';
  ctx.fillText(success ? 'Takeoff Success!' : 'Game Over!', 220, 250);
  ctx.font = '32px Arial';
  ctx.fillStyle = '#222';
  ctx.fillText(`Time: ${elapsed}s`, 320, 320);
  ctx.fillText(`Score: ${score}`, 320, 370);
  ctx.font = '20px Arial';
  ctx.fillText('Press ENTER to restart', 300, 450);
}

// 충돌 체크
function checkCollision() {
  for (let hz of hazards) {
    if (player.x + player.w / 2 > hz.x - 24 &&
        player.x + player.w / 2 < hz.x + 24 &&
        player.y + player.h / 2 > hz.y - 24 &&
        player.y + player.h / 2 < hz.y + 24) {
      collided = true;
      return true;
    }
  }
  return false;
}

// 점수 계산
function calcScore() {
  return Math.max(0, 1000 - elapsed * 100 + hazards.length * 200);
}

// 키보드 이벤트
document.addEventListener('keydown', function(e) {
  if (gameState === 'menu') {
    if (e.key === 'ArrowUp') selectedAircraft = (selectedAircraft + aircrafts.length - 1) % aircrafts.length;
    if (e.key === 'ArrowDown') selectedAircraft = (selectedAircraft + 1) % aircrafts.length;
    if (e.key === 'Enter') startGame();
  } else if (gameState === 'playing') {
    if (e.key === 'ArrowLeft') player.x -= player.speed;
    if (e.key === 'ArrowRight') player.x += player.speed;
    if (e.key === 'ArrowUp') player.y -= player.speed;
    if (e.key === 'ArrowDown') player.y += player.speed;
    if (e.key === ' ') gameState = 'takeoff'; // 스페이스바로 이륙 시도
  } else if (gameState === 'gameover' || gameState === 'success') {
    if (e.key === 'Enter') {
      gameState = 'menu';
      selectedAircraft = 0;
    }
  }
});

// 메인 루프
function loop() {
  if (gameState === 'menu') drawMenu();
  else if (gameState === 'playing') {
    drawGame();
    if (checkCollision()) {
      gameState = 'gameover';
      score = 0;
      setTimeout(() => {}, 1000);
    } else if (gameState === 'takeoff' && player.y < 100) {
      score = calcScore();
      gameState = 'success';
    }
  } else if (gameState === 'gameover') drawEnd(false);
  else if (gameState === 'success') drawEnd(true);
  requestAnimationFrame(loop);
}
loop();
