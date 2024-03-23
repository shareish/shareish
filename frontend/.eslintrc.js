module.exports = {
  'root': true,

  'env': {
    'node': true
  },

  'extends': [
    'plugin:vue/essential'
  ],

  rules: {
    // 'brace-style': ['error', 'stroustrup'],
    // 'array-bracket-spacing': ['error', 'never'],
    // 'camelcase': ['error', {allow: ['$_veeValidate']}],
    // 'no-console': ['off']
  },

  'parserOptions': {
    'parser': 'babel-eslint'
  },

  overrides: [
    {
      files: [
        '**/__tests__/*.{j,t}s?(x)',
        '**/tests/unit/**/*.spec.{j,t}s?(x)'
      ],
      env: {
        jest: true
      }
    }
  ]
};
