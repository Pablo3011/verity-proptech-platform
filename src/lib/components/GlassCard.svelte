<script lang="ts">
	import { cn } from '$utils/cn';
	
	let className = '';
	export { className as class };
</script>

<div class={cn('glass', className)}>
	<slot />
</div>

<style>
	.glass {
		background: rgba(255, 255, 255, 0.05);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}
</style>