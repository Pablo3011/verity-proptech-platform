<script lang="ts">
	import GlassCard from './GlassCard.svelte';
	import { Database, BarChart, Code2, Megaphone, Settings } from 'lucide-svelte';
	import type { Capability } from '$types';
	
	const capabilities: Capability[] = [
		{
			id: '1',
			name: 'Market Research',
			category: 'research',
			confidence: 95,
			learned_at: '2 days ago',
			usage_count: 47
		},
		{
			id: '2',
			name: 'Competitive Analysis',
			category: 'analysis',
			confidence: 92,
			learned_at: '3 days ago',
			usage_count: 35
		},
		{
			id: '3',
			name: 'MVP Development',
			category: 'development',
			confidence: 88,
			learned_at: '1 week ago',
			usage_count: 12
		},
		{
			id: '4',
			name: 'SEO Optimization',
			category: 'marketing',
			confidence: 85,
			learned_at: '1 week ago',
			usage_count: 23
		},
		{
			id: '5',
			name: 'Process Automation',
			category: 'operations',
			confidence: 90,
			learned_at: '5 days ago',
			usage_count: 18
		}
	];
	
	const categoryIcons = {
		research: Database,
		analysis: BarChart,
		development: Code2,
		marketing: Megaphone,
		operations: Settings
	};
	
	const categoryColors = {
		research: 'blue',
		analysis: 'teal',
		development: 'purple',
		marketing: 'amber',
		operations: 'green'
	};
</script>

<GlassCard class="p-6">
	<h3 class="text-lg font-semibold mb-4">AI Capabilities</h3>
	<div class="space-y-3 max-h-[400px] overflow-y-auto custom-scrollbar">
		{#each capabilities as cap}
			<div class="p-3 rounded-lg bg-zinc-900/50 hover:bg-zinc-900/70 transition-colors">
				<div class="flex items-start justify-between mb-2">
					<div class="flex items-center gap-2">
						<svelte:component 
							this={categoryIcons[cap.category]} 
							class="w-4 h-4 text-{categoryColors[cap.category]}-400" 
						/>
						<span class="text-sm font-medium">{cap.name}</span>
					</div>
					<span class="text-xs text-zinc-500">{cap.usage_count}x</span>
				</div>
				<div class="space-y-1">
					<div class="flex items-center justify-between text-xs text-zinc-500">
						<span>Confidence</span>
						<span>{cap.confidence}%</span>
					</div>
					<div class="h-1 bg-zinc-800 rounded-full overflow-hidden">
						<div 
							class="h-full bg-gradient-to-r from-{categoryColors[cap.category]}-500 to-{categoryColors[cap.category]}-400"
							style="width: {cap.confidence}%"
						/>
					</div>
				</div>
			</div>
		{/each}
	</div>
</GlassCard>