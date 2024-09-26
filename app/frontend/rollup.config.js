import svelte from 'rollup-plugin-svelte';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import livereload from 'rollup-plugin-livereload';
import { terser } from 'rollup-plugin-terser';
import css from 'rollup-plugin-css-only'
 
const production = !process.env.ROLLUP_WATCH;
 
export default {
    input: 'src/main.js',
    output: {
        sourcemap: true,
        format: 'iife',
        name: 'app',
        file: 'public/bundle.js'
    },
    plugins: [
        svelte({
            // enable run-time checks when not in production
            dev: !production,
            // we'll extract any component CSS out into
            // a separate file — better for performance
            emitCss: true
            // css: css => {
            //  css.write('public/bundle.css');
            // }
        }),
       
        // Extract global CSS into a separate file
        css({ output: 'bundle.css' }),
       
        // If you have external dependencies installed from
        // npm, you'll most likely need these plugins. In
        // some cases you'll need additional configuration —
        // consult the documentation for details:
        // https://github.com/rollup/rollup-plugin-commonjs
        resolve({
            browser: true,
            dedupe: importee =>
              importee === 'svelte' ||
              importee.startsWith('svelte/') ||
              importee === 'socket.io-client' ||
              importee.startsWith('socket.io-client/')
          }),
        commonjs(),
 
        // Watch the `public` directory and refresh the
        // browser on changes when not in production
        !production && livereload({
            watch: 'public',
            exts: ['html', 'js', 'css', 'svelte'],
            delay: 200
          }),
        // If we're building for production (npm run build
        // instead of npm run dev), minify
        production && terser()
    ],
    watch: {
        clearScreen: false
    }
};
