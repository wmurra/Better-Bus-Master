import App from './App.svelte';
import './global.css';
import { setBasePath } from '@shoelace-style/shoelace/dist/utilities/base-path.js'
import '@shoelace-style/shoelace/dist/themes/light.css';

async function initializeApp() {
	setBasePath('/node_modules/@shoelace-style/shoelace/dist')
	const app = new App({
		target: document.body,
	});	
}
initializeApp()