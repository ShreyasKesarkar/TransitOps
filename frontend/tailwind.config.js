/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#e8f1ff',
          100: '#cddfff',
          200: '#a2c3ff',
          300: '#75a5ff',
          400: '#4f88ff',
          500: '#2f6eff',
          600: '#1f56e0',
          700: '#1b46b3',
          800: '#173a8d',
          900: '#132f72',
        },
        surface: '#0b1220',
        panel: '#111a2e',
        line: '#22304a',
      },
      boxShadow: {
        panel: '0 20px 60px rgba(0, 0, 0, 0.28)',
      },
    },
  },
  plugins: [],
};