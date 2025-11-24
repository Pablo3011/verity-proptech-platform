import { writable } from 'svelte/store';
import type { Opportunity } from '$types';

export const opportunities = writable<Opportunity[]>([]);
export const loading = writable<boolean>(false);
export const error = writable<string | null>(null);