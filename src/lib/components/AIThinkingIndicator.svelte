<script lang="ts">
	import { onMount } from 'svelte';
	import { Brain } from 'lucide-svelte';
	
	let status: 'idle' | 'thinking' | 'researching' | 'building' = 'thinking';
	let progress = 0;
	let currentTask = 'Analyzing market trends...';
	
	const tasks = [
		'Analyzing market trends...',
		'Researching opportunities...',
		'Validating business models...',
		'Calculating revenue potential...'
	];
	
	let taskIndex = 0;
	
	onMount(() => {
		const interval = setInterval(() => {
			progress = (progress + 5) % 100;
			
			if (progress === 0) {
				taskIndex = (taskIndex + 1) % tasks.length;
				currentTask = tasks[taskIndex];
			}
		}, 200);
		
		return () => clearInterval(interval);
	});
	
	const statusColors = {
		idle: 'text-zinc-400',
		thinking: 'text-blue-400',
		researching: 'text-teal-400',
		building: 'text-purple-400'
	};
</script>

<div class="glass p-4 flex items-center gap-3">
	<div class="relative">
		<div class="absolute inset-0 animate-pulse-glow rounded-full" class:glow-blue={status === 'thinking'} class:glow-teal={status === 'researching'} />
		<Brain class="w-6 h-6 {statusColors[status]} relative z-10" />
	</div>
	<div class="flex-1 min-w-0">
		<p class="text-sm font-medium mb-1">AI Status: {status}</p>
		<p class="text-xs text-zinc-400 truncate">{currentTask}</p>
		<div class="mt-2 h-1 bg-zinc-800 rounded-full overflow-hidden">
			<div 
				class="h-full bg-gradient-to-r from-blue-500 to-teal-500 transition-all duration-200"
				style="width: {progress}%"
			/>
		</div>
	</div>
</div>

<style>
	.glow-blue {
		box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
	}
	
	.glow-teal {
		box-shadow: 0 0 20px rgba(20, 184, 166, 0.5);
	}
</style>