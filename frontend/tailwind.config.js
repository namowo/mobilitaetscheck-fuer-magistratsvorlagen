/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['selector', '[data-mode="dark"]'],
  content: [
    './index.html',
    './src/*.{js,ts,vue}',
    './src/**/*.{js,ts,vue}',
    './src/**/**/*.{js,ts,vue}'
  ],
  theme: {
    fontFamily: {
      sans: ['Helvetica', 'Arial', 'sans-serif']
    },
    extend: {
      colors: {
        blue: {
          DEFAULT: 'rgb(var(--primary-900) / <alpha-value>)',
          100: 'rgb(var(--primary-100) / <alpha-value>)',
          200: 'rgb(var(--primary-200) / <alpha-value>)',
          300: 'rgb(var(--primary-300) / <alpha-value>)',
          400: 'rgb(var(--primary-400) / <alpha-value>)',
          500: 'rgb(var(--primary-500) / <alpha-value>)',
          600: 'rgb(var(--primary-600) / <alpha-value>)',
          700: 'rgb(var(--primary-700) / <alpha-value>)',
          800: 'rgb(var(--primary-800) / <alpha-value>)',
          900: 'rgb(var(--primary-900) / <alpha-value>)'
        },
        red: {
          DEFAULT: '#E05A47',
          100: '#fbe9e7',
          200: '#f3beb6',
          300: '#eb9286',
          400: '#e26755',
          500: '#da3b25',
          600: '#aa2e1d',
          700: '#792114',
          800: '#49140c',
          900: '#180704'
        }
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            ul: {
              listStyleType: 'disc',
              paddingLeft: '1.25em',
              marginTop: '0.5em',
              marginBottom: '0.5em'
            },
            ol: {
              listStyleType: 'decimal',
              paddingLeft: '1.25em',
              marginTop: '0.5em',
              marginBottom: '0.5em'
            },
            li: {
              marginTop: '0.25em',
              marginBottom: '0.25em'
            },
            p: {
              marginTop: '0.5em',
              marginBottom: '0.5em'
            }
          }
        }
      })
    }
  },
  plugins: []
}
