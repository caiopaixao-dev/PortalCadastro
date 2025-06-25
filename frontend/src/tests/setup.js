import { expect, afterEach, beforeAll } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// Estender expect com matchers do jest-dom
expect.extend(matchers);

// Cleanup após cada teste
afterEach(() => {
  cleanup();
});

// Configuração global antes de todos os testes
beforeAll(() => {
  // Mock do IntersectionObserver
  global.IntersectionObserver = class IntersectionObserver {
    constructor() {}
    disconnect() {}
    observe() {}
    unobserve() {}
  };

  // Mock do ResizeObserver
  global.ResizeObserver = class ResizeObserver {
    constructor() {}
    disconnect() {}
    observe() {}
    unobserve() {}
  };

  // Mock do matchMedia
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: (query) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: () => {},
      removeListener: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => {},
    }),
  });

  // Mock do scrollTo
  window.scrollTo = () => {};

  // Mock do alert
  window.alert = () => {};

  // Mock do confirm
  window.confirm = () => true;

  // Mock do prompt
  window.prompt = () => 'test';

  // Mock do console para testes mais limpos
  const originalConsoleError = console.error;
  console.error = (...args) => {
    // Ignorar erros específicos do React em testes
    if (
      typeof args[0] === 'string' &&
      args[0].includes('Warning: ReactDOM.render is no longer supported')
    ) {
      return;
    }
    originalConsoleError.call(console, ...args);
  };
});

