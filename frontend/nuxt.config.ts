import tailwindcss from '@tailwindcss/vite';

export default defineNuxtConfig({
	compatibilityDate: '2024-08-12',
	devtools: { enabled: true },
	srcDir: '.',
	modules: ['@nuxt/eslint', 'nuxt-typed-router'],
	css: ['~/public/css/main.css'],
	vite: {
		plugins: [tailwindcss()],
	},
});
