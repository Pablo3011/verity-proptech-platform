<script lang="ts">
	import GlassCard from './GlassCard.svelte';
	import { CheckCircle2, AlertCircle, Clock } from 'lucide-svelte';
	import type { MetaProofEntry } from '$types';
	
	const entries: MetaProofEntry[] = [
		{
			id: '1',
			timestamp: '2024-11-24 17:23:45',
			action: 'Market Research Completed',
			agent: 'Research Agent',
			result: 'Identified 47 new opportunities in SaaS sector',
			verified: true
		},
		{
			id: '2',
			timestamp: '2024-11-24 16:45:12',
			action: 'Competitive Analysis',
			agent: 'Analysis Agent',
			result: 'Low competition detected in AI customer service market',
			verified: true
		},
		{
			id: '3',
			timestamp: '2024-11-24 15:30:22',
			action: 'Revenue Model Validation',
			agent: 'Financial Agent',
			result: 'Projected ARR: $500K - $2M with 80% confidence',
			verified: true
		},
		{
			id: '4',
			timestamp: '2024-11-24 14:15:08',
			action: 'Capability Learning',
			agent: 'Self-Learning Module',
			result: 'Acquired new skill: SEO Optimization',
			verified: false
		}
	];
</script>

<GlassCard class="p-6">
	<div class="flex items-center justify-between mb-4">
		<h3 class="text-lg font-semibold">Meta-Proof Log</h3>
		<span class="text-xs text-zinc-500">Verity Built Verity</span>
	</div>
	
	<div class="space-y-2 max-h-[300px] overflow-y-auto custom-scrollbar">
		{#each entries as entry}
			<div class="p-3 rounded-lg bg-zinc-900/30 border border-zinc-800/50 hover:border-zinc-700 transition-colors">
				<div class="flex items-start gap-3">
					<div class="mt-0.5">
						{#if entry.verified}
							<CheckCircle2 class="w-4 h-4 text-green-400" />
						{:else}
							<Clock class="w-4 h-4 text-amber-400" />
						{/if}
					</div>
					<div class="flex-1 min-w-0">
						<div class="flex items-center gap-2 mb-1">
							<span class="text-sm font-medium">{entry.action}</span>
							<span class="text-xs px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400">
								{entry.agent}
							</span>
						</div>
						<p class="text-xs text-zinc-400 mb-1">{entry.result}</p>
						<p class="text-xs text-zinc-600">{entry.timestamp}</p>
					</div>
				</div>
			</div>
		{/each}
	</div>
</GlassCard>