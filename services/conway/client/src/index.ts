// TODO: refactor to use state object for ctx etc.

import { Life, init } from "wasm-conway";
import { memory } from "wasm-conway/conway_bg.wasm";

init()

const CELL_SIZE = 16; // px
const GRID_COLOR = "#CCCCCC";
const DEAD_COLOR = "#FFFFFF";
const ALIVE_COLOR = "#000000";
const [WIDTH, HEIGHT] = [32, 32];

const life = Life.new(WIDTH, HEIGHT);

const canvas = <HTMLCanvasElement>document.getElementById("life-canvas");
canvas.height = (CELL_SIZE + 1) * HEIGHT + 1;
canvas.width = (CELL_SIZE + 1) * WIDTH + 1;

const drawGrid = (ctx: CanvasRenderingContext2D) => {
    ctx.beginPath();
    ctx.strokeStyle = GRID_COLOR;
    // Vertical lines.
    for (let i = 0; i <= WIDTH; i++) {
        ctx.moveTo(i * (CELL_SIZE + 1) + 1, 0);
        ctx.lineTo(i * (CELL_SIZE + 1) + 1, (CELL_SIZE + 1) * HEIGHT + 1);
    }
    // Horizontal lines.
    for (let j = 0; j <= HEIGHT; j++) {
        ctx.moveTo(0, j * (CELL_SIZE + 1) + 1);
        ctx.lineTo((CELL_SIZE + 1) * WIDTH + 1, j * (CELL_SIZE + 1) + 1);
    }
    ctx.stroke();
};

const getIndex = (row: number, column: number) => {
    return row * WIDTH + column;
};

const drawCells = (ctx: CanvasRenderingContext2D) => {
    const cellsPtr = life.cells();
    const cells = new Uint8Array(memory.buffer, cellsPtr, WIDTH * HEIGHT);
    ctx.beginPath();
    for (let row = 0; row < HEIGHT; row++) {
        for (let col = 0; col < WIDTH; col++) {
            const idx = getIndex(row, col);
            ctx.fillStyle = cells[idx] ? ALIVE_COLOR : DEAD_COLOR;
            ctx.fillRect(
                col * (CELL_SIZE + 1) + 1,
                row * (CELL_SIZE + 1) + 1,
                CELL_SIZE,
                CELL_SIZE
            );
        }
    }
    ctx.stroke();
};

const ctx = canvas.getContext("2d");

canvas.addEventListener("click", event => {
    const boundingRect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / boundingRect.width;
    const scaleY = canvas.height / boundingRect.height;
    const canvasLeft = (event.clientX - boundingRect.left) * scaleX;
    const canvasTop = (event.clientY - boundingRect.top) * scaleY;
    const x = Math.min(Math.floor(canvasLeft / (CELL_SIZE + 1)), WIDTH - 1);
    const y = Math.min(Math.floor(canvasTop / (CELL_SIZE + 1)), HEIGHT - 1);
    life.toggle_xy(x, y);
    drawCells(ctx);
});

let animationId: number | null = null;

const renderLoop = () => {
    life.tick();
    drawCells(ctx);
    animationId = requestAnimationFrame(renderLoop);
};

const isPaused = () => (animationId === null);

const playPauseButton = document.getElementById("play-pause");

const play = () => {
    playPauseButton.textContent = "⏸";
    renderLoop();
};

const pause = () => {
    playPauseButton.textContent = "▶";
    cancelAnimationFrame(animationId);
    animationId = null;
};

playPauseButton.addEventListener("click", _ => {
    if (isPaused()) {
        play();
    } else {
        pause();
    }
});

drawGrid(ctx);
drawCells(ctx);
playPauseButton.textContent = "▶";
