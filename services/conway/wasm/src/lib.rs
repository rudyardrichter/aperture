extern crate console_error_panic_hook;

mod utils;

use std::panic;

use wasm_bindgen::prelude::*;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[wasm_bindgen]
pub struct Life {
    width: usize,
    height: usize,
    cells: Vec<bool>,
}

impl Life {
    fn get(&self, i: usize) -> bool {
        self.cells[i]
    }

    fn xy_to_index(&self, (x, y): (usize, usize)) -> usize {
        x + y * self.width
    }

    fn is_live_next(&self, i: usize) -> bool {
        let n_neighbors = [
            self.width * (self.height - 1) - 1,
            self.width * (self.height - 1),
            self.width * (self.height - 1) + 1,
            self.width * self.height - 1,
            self.width * self.height + 1,
            self.width * (self.height + 1) - 1,
            self.width * (self.height + 1),
            self.width * (self.height + 1) + 1,
        ]
        .iter()
        .filter(|&j| self.get((i + j) % (self.width * self.height)))
        .count();
        matches!((self.get(i), n_neighbors), (true, 2) | (_, 3))
    }
}

#[wasm_bindgen]
impl Life {
    pub fn new(width: usize, height: usize) -> Self {
        Self {
            width,
            height,
            cells: vec![false; width * height],
        }
    }

    pub fn width(&self) -> usize {
        self.width
    }

    pub fn height(&self) -> usize {
        self.height
    }

    pub fn cells(&self) -> *const bool {
        self.cells.as_ptr()
    }

    pub fn tick(&mut self) {
        self.cells = (0..self.cells.len())
            .map(|i| self.is_live_next(i))
            .collect()
    }

    pub fn toggle_xy(&mut self, x: usize, y: usize) {
        let i = self.xy_to_index((x, y));
        if let Some(cell) = self.cells.get_mut(i) {
            *cell = !*cell;
        }
    }
}

#[wasm_bindgen]
pub fn init() {
    panic::set_hook(Box::new(console_error_panic_hook::hook));
}
