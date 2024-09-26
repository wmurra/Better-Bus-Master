import { writable } from 'svelte/store';
import io from 'socket.io-client';
import merge from 'lodash/merge';
var socket = io.connect('http://'+ document.domain + ':' + location.port);
export default socket;

export const modelStore = writable({});

export function update(field, data = undefined){
    socket.emit("update", field, data);
};

socket.on('render', (changes) => {
    modelStore.update(currentModel => {
        return changes;
    });
});

socket.emit('get_model')