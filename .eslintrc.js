module.exports = {
  env: {
    browser: true,
    es6: true
  },
  extends: [
    'standard',
    'eslint:recommended'
  ],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly'
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module'
  },
  rules: {
    "semi": [2, 'always'],
    "indent": ["error", 4],
    "camelcase": "off"
  }
}
