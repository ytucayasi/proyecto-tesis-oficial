/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",  // Busca en todos los archivos HTML y TypeScript
    "./src/**/*.component.{html,ts}" // Específicamente para componentes Angular
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}