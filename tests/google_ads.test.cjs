const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'assets/js/google-ads.js'), 'utf8');

function setup() {
  const handlers = {};
  const appendedScripts = [];
  const document = {
    baseURI: 'https://vkotocozum.com/',
    querySelector: () => null,
    createElement: () => ({}),
    head: { appendChild: (script) => appendedScripts.push(script) },
    addEventListener: (name, handler) => { handlers[name] = handler; }
  };
  const window = {};
  vm.runInNewContext(source, { document, window, URL, Set, Object, Date });
  return { document, window, handlers, appendedScripts };
}

function click(state, href) {
  state.handlers.click({
    target: { closest: (selector) => selector === 'a[href]' ? { href } : null }
  });
}

function dataLayerEntry(entry) {
  return Array.from(entry, (item) => {
    if (item && typeof item === 'object' && !(item instanceof Date)) {
      return { ...item };
    }
    return item;
  });
}

test('loads and configures the Google Ads tag once', () => {
  const state = setup();
  assert.equal(state.appendedScripts.length, 1);
  assert.equal(state.appendedScripts[0].async, true);
  assert.equal(state.appendedScripts[0].src,
    'https://www.googletagmanager.com/gtag/js?id=AW-789474599');
  assert.deepEqual(dataLayerEntry(state.window.dataLayer[1]),
    ['config', 'AW-789474599']);
});

test('attributes the software WhatsApp number to the 0551 conversion', () => {
  const state = setup();
  click(state, 'https://wa.me/905518652667?text=Merhaba');
  assert.deepEqual(dataLayerEntry(state.window.dataLayer.at(-1)), [
    'event',
    'conversion',
    { send_to: 'AW-789474599/7yumCPfDtYodEKfaufgC' }
  ]);
});

test('attributes the service WhatsApp number to the 0546 conversion', () => {
  const state = setup();
  click(state, 'https://wa.me/905462436828');
  assert.deepEqual(dataLayerEntry(state.window.dataLayer.at(-1)), [
    'event',
    'conversion',
    { send_to: 'AW-789474599/KzsWCI3ur4odEKfaufgC' }
  ]);
});

test('ignores other links and unknown WhatsApp numbers', () => {
  const state = setup();
  const before = state.window.dataLayer.length;
  click(state, 'tel:+905518652667');
  click(state, 'https://wa.me/905550000000');
  click(state, 'https://example.com/?phone=905518652667');
  assert.equal(state.window.dataLayer.length, before);
});

test('every public page loads the shared tracking script exactly once', () => {
  const pages = fs.readdirSync(root)
    .filter((name) => name.endsWith('.html'))
    .map((name) => path.join(root, name));
  const serviceRoot = path.join(root, 'hizmetler');
  for (const entry of fs.readdirSync(serviceRoot, { withFileTypes: true })) {
    if (entry.isDirectory()) pages.push(path.join(serviceRoot, entry.name, 'index.html'));
  }

  for (const page of pages) {
    const html = fs.readFileSync(page, 'utf8');
    const includes = html.match(/<script src="\/assets\/js\/google-ads\.js" defer><\/script>/g) || [];
    assert.equal(includes.length, 1, path.relative(root, page));
  }
});
