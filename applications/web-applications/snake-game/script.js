const GRID_SIZE = 20;
const TILE_COUNT = 20;
const START_SPEED = 150;
const STORAGE_KEY = 'snake-best-score';

class SnakeGame {
    constructor() {
        this.canvas = document.getElementById('game-board');
        this.ctx = this.canvas.getContext('2d');
        this.scoreEl = document.getElementById('score');
        this.bestScoreEl = document.getElementById('best-score');
        this.stateEl = document.getElementById('game-state');
        this.overlayEl = document.getElementById('overlay');
        this.startButton = document.getElementById('start-button');
        this.pauseButton = document.getElementById('pause-button');
        this.restartButton = document.getElementById('restart-button');

        this.bestScore = this.loadBestScore();
        this.intervalId = null;

        this.bindEvents();
        this.reset();
        this.updateBestScore();
        this.draw();
    }

    bindEvents() {
        document.addEventListener('keydown', (event) => this.handleKeydown(event));
        this.startButton.addEventListener('click', () => this.start());
        this.pauseButton.addEventListener('click', () => this.togglePause());
        this.restartButton.addEventListener('click', () => this.restart());
    }

    reset() {
        this.snake = [
            { x: 10, y: 10 },
            { x: 9, y: 10 },
            { x: 8, y: 10 }
        ];
        this.direction = { x: 1, y: 0 };
        this.nextDirection = { x: 1, y: 0 };
        this.food = this.generateFood();
        this.score = 0;
        this.speed = START_SPEED;
        this.isRunning = false;
        this.isPaused = false;
        this.hasStarted = false;
        this.isGameOver = false;

        this.updateScore();
        this.setState('Ready');
        this.setOverlay('Press Start', 'Eat food, grow the snake, and survive as long as you can.', true);
        this.pauseButton.textContent = 'Pause';
    }

    restart() {
        this.stopLoop();
        this.reset();
        this.draw();
    }

    start() {
        if (this.isRunning) {
            return;
        }

        if (this.isGameOver) {
            this.reset();
            this.draw();
        }

        if (!this.hasStarted) {
            this.hasStarted = true;
        }

        this.isRunning = true;
        this.isPaused = false;
        this.pauseButton.textContent = 'Pause';
        this.setState('Running');
        this.hideOverlay();
        this.startLoop();
    }

    togglePause() {
        if (!this.hasStarted) {
            return;
        }

        if (this.isPaused) {
            this.isPaused = false;
            this.isRunning = true;
            this.pauseButton.textContent = 'Pause';
            this.setState('Running');
            this.hideOverlay();
            this.startLoop();
            return;
        }

        if (this.isRunning) {
            this.isPaused = true;
            this.isRunning = false;
            this.pauseButton.textContent = 'Resume';
            this.setState('Paused');
            this.setOverlay('Paused', 'Press Space or Resume to continue.');
            this.stopLoop();
        }
    }

    handleKeydown(event) {
        const key = event.key.toLowerCase();
        const directionMap = {
            arrowup: { x: 0, y: -1 },
            w: { x: 0, y: -1 },
            arrowdown: { x: 0, y: 1 },
            s: { x: 0, y: 1 },
            arrowleft: { x: -1, y: 0 },
            a: { x: -1, y: 0 },
            arrowright: { x: 1, y: 0 },
            d: { x: 1, y: 0 }
        };

        if (key === ' ') {
            event.preventDefault();
            if (!this.hasStarted) {
                this.start();
            } else {
                this.togglePause();
            }
            return;
        }

        const newDirection = directionMap[key];
        if (!newDirection) {
            return;
        }

        event.preventDefault();

        const isReverseMove =
            newDirection.x === -this.direction.x && newDirection.y === -this.direction.y;

        if (!isReverseMove) {
            this.nextDirection = newDirection;
        }

        if (!this.hasStarted) {
            this.start();
        }
    }

    startLoop() {
        this.stopLoop();
        this.intervalId = window.setInterval(() => {
            this.tick();
        }, this.speed);
    }

    stopLoop() {
        if (this.intervalId) {
            window.clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    tick() {
        this.direction = this.nextDirection;

        const head = { ...this.snake[0] };
        head.x += this.direction.x;
        head.y += this.direction.y;

        if (this.isCollision(head)) {
            this.gameOver();
            return;
        }

        this.snake.unshift(head);

        if (head.x === this.food.x && head.y === this.food.y) {
            this.score += 1;
            this.updateScore();
            this.food = this.generateFood();
            this.increaseSpeed();
        } else {
            this.snake.pop();
        }

        this.draw();
    }

    isCollision(head) {
        const hitWall =
            head.x < 0 || head.x >= TILE_COUNT || head.y < 0 || head.y >= TILE_COUNT;

        if (hitWall) {
            return true;
        }

        return this.snake.some((segment) => segment.x === head.x && segment.y === head.y);
    }

    increaseSpeed() {
        const nextSpeed = Math.max(70, START_SPEED - this.score * 4);
        if (nextSpeed !== this.speed) {
            this.speed = nextSpeed;
            if (this.isRunning) {
                this.startLoop();
            }
        }
    }

    gameOver() {
        this.stopLoop();
        this.isRunning = false;
        this.isPaused = false;
        this.isGameOver = true;
        this.pauseButton.textContent = 'Pause';
        this.setState('Game Over');
        this.updateBestScore(true);
        this.setOverlay('Game Over', `Final score: ${this.score}. Press Restart or Start Game to play again.`);
    }

    generateFood() {
        let food;

        do {
            food = {
                x: Math.floor(Math.random() * TILE_COUNT),
                y: Math.floor(Math.random() * TILE_COUNT)
            };
        } while (this.snake?.some((segment) => segment.x === food.x && segment.y === food.y));

        return food;
    }

    updateScore() {
        this.scoreEl.textContent = String(this.score);
        this.updateBestScore();
    }

    updateBestScore(forceSave = false) {
        if (this.score > this.bestScore) {
            this.bestScore = this.score;
            forceSave = true;
        }

        if (forceSave) {
            this.saveBestScore();
        }

        this.bestScoreEl.textContent = String(this.bestScore);
    }

    setState(value) {
        this.stateEl.textContent = value;
    }

    setOverlay(title, text, show = true) {
        this.overlayEl.querySelector('.overlay-title').textContent = title;
        this.overlayEl.querySelector('.overlay-text').textContent = text;

        if (show) {
            this.overlayEl.classList.remove('is-hidden');
        } else {
            this.overlayEl.classList.add('is-hidden');
        }
    }

    hideOverlay() {
        this.overlayEl.classList.add('is-hidden');
    }

    loadBestScore() {
        try {
            return Number.parseInt(window.localStorage.getItem(STORAGE_KEY), 10) || 0;
        } catch {
            return 0;
        }
    }

    saveBestScore() {
        try {
            window.localStorage.setItem(STORAGE_KEY, String(this.bestScore));
        } catch {
            // Ignore storage failures so gameplay still works in restricted browsers.
        }
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.drawFood();
        this.drawSnake();
    }

    drawSnake() {
        this.snake.forEach((segment, index) => {
            const color = index === 0 ? '#7df9a7' : '#2ec96d';
            this.ctx.fillStyle = color;
            this.ctx.fillRect(
                segment.x * GRID_SIZE + 1,
                segment.y * GRID_SIZE + 1,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            );
        });
    }

    drawFood() {
        this.ctx.fillStyle = '#ffb703';
        this.ctx.beginPath();
        this.ctx.arc(
            this.food.x * GRID_SIZE + GRID_SIZE / 2,
            this.food.y * GRID_SIZE + GRID_SIZE / 2,
            GRID_SIZE / 2.8,
            0,
            Math.PI * 2
        );
        this.ctx.fill();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SnakeGame();
});
