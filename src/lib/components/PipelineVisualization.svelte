<script lang="ts">
	import GlassCard from './GlassCard.svelte';
	import { Search, Brain, Code, Rocket, TrendingUp } from 'lucide-svelte';
	import type { PipelineStage } from '$types';
	
	const stages: PipelineStage[] = [
		{
			id: '1',
			name: 'Discovery',
			description: 'Finding opportunities',
			opportunities: 47,
			color: 'blue'
		},
		{
			id: '2',
			name: 'Analysis',
			description: 'Validating markets',
			opportunities: 23,
			color: 'teal'
		},
		{
			id: '3',
			name: 'Planning',
			description: 'Building strategies',
			opportunities: 12,
			color: 'purple'
		},
		{
			id: '4',
			name: 'Development',
			description: 'Creating products',
			opportunities: 5,
			color: 'amber'
		},
		{
			id: '5',
			name: 'Launch',
			description: 'Going to market',
			opportunities: 2,
			color: 'green'
		}
	];
	
	const icons = [Search, Brain, Code, Rocket, TrendingUp];
</script>

<GlassCard class="p-6">
	<h3 class="text-lg font-semibold mb-4">Autonomous Pipeline</h3>
	<div class="space-y-3">
		{#each stages as stage, i}
			<div class="group">
				<div class="flex items-center gap-3 mb-2">
					<div class="p-2 rounded-lg bg-{stage.color}-500/10 group-hover:bg-{stage.color}-500/20 transition-colors">
						<svelte:component this={icons[i]} class="w-4 h-4 text-{stage.color}-400" />
					</div>
					<div class="flex-1">
						<div class="flex items-center justify-between">
							<span class="text-sm font-medium">{stage.name}</span>
							<span class="text-sm font-bold text-{stage.color}-400">{stage.opportunities}</span>
						</div>
						<p class="text-xs text-zinc-500">{stage.description}</p>
					</div>
				</div>
				{#if i < stages.length - 1}
					<div class="ml-5 h-6 w-0.5 bg-gradient-to-b from-{stage.color}-500/50 to-{stages[i+1].color}-500/50" />
				{/if}
			</div>
		{/each}
	</div>
</GlassCard>