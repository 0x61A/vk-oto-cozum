const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '../assets/js/software-menu.js'), 'utf8');
function setup() {
  const handlers = {};
  const attributes = {};
  const classes = new Set(['hidden', 'md:hidden']);
  let focused = false;
  const button = {
    setAttribute: (name, value) => { attributes[name] = value; },
    addEventListener: (name, handler) => { handlers['button:' + name] = handler; },
    focus: () => { focused = true; }
  };
  const menu = {
    id: 'mobile-menu',
    classList: {
      contains: (name) => classes.has(name),
      toggle: (name, force) => force ? classes.add(name) : classes.delete(name)
    },
    addEventListener: (name, handler) => { handlers['menu:' + name] = handler; }
  };
  const document = {
    getElementById: (id) => id === 'mobile-menu-btn' ? button : id === 'mobile-menu' ? menu : null,
    addEventListener: (name, handler) => { handlers['document:' + name] = handler; }
  };
  vm.runInNewContext(source, { document });
  return { handlers, attributes, classes, focused: () => focused };
}

test('menu opens and closes while preserving desktop hiding class', () => {
  const state = setup();
  assert.equal(state.attributes['aria-expanded'], 'false');
  assert.equal(state.attributes['aria-controls'], 'mobile-menu');
  state.handlers['button:click']();
  assert.equal(state.attributes['aria-expanded'], 'true');
  assert.equal(state.classes.has('hidden'), false);
  assert.equal(state.classes.has('md:hidden'), true);
  state.handlers['button:click']();
  assert.equal(state.attributes['aria-expanded'], 'false');
  assert.equal(state.classes.has('hidden'), true);
});

test('Escape closes the menu and restores focus', () => {
  const state = setup();
  state.handlers['button:click']();
  state.handlers['document:keydown']({ key: 'Escape' });
  assert.equal(state.classes.has('hidden'), true);
  assert.equal(state.focused(), true);
});

test('a navigation link closes the menu, without intercepting navigation', () => {
  const state = setup();
  state.handlers['button:click']();
  state.handlers['menu:click']({ target: { closest: () => ({ tagName: 'A' }) } });
  assert.equal(state.attributes['aria-expanded'], 'false');
});

test('missing navigation elements are harmless', () => {
  assert.doesNotThrow(() => vm.runInNewContext(source, { document: { getElementById: () => null } }));
});
