/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				glass: {
					bg: 'rgba(255, 255, 255, 0.05)',
					border: 'rgba(255, 255, 255, 0.1)',
					hover: 'rgba(255, 255, 255, 0.08)'
				},
				primary: {
					50: '#f0f9ff',
					100: '#e0f2fe',
					200: '#bae6fd',
					300: '#7dd3fc',
					400: '#38bdf8',
					500: '#0ea5e9',
					600: '#0284c7',
					700: '#0369a1',
					800: '#075985',
					900: '#0c4a6e'
				}
			},
			backdropBlur: {
				xs: '2px',
				glass: '20px'
			},
			animation: {
				'pulse-glow': 'pulse-glow 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
				'float': 'float 6s ease-in-out infinite',
				'slide-up': 'slide-up 0.5s ease-out'
			},
			keyframes: {
				'pulse-glow': {
					'0%, 100%': { opacity: 1, boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)' },
					'50%': { opacity: 0.7, boxShadow: '0 0 40px rgba(59, 130, 246, 0.8)' }
				},
				'float': {
					'0%, 100%': { transform: 'translateY(0px)' },
					'50%': { transform: 'translateY(-10px)' }
				},
				'slide-up': {
					'0%': { transform: 'translateY(20px)', opacity: 0 },
					'100%': { transform: 'translateY(0)', opacity: 1 }
				}
			}
		}
	},
	plugins: []
};