<script lang="ts">
	import GlassCard from '$components/GlassCard.svelte';
	import AIThinkingIndicator from '$components/AIThinkingIndicator.svelte';
	import OpportunityCard from '$components/OpportunityCard.svelte';
	import PipelineVisualization from '$components/PipelineVisualization.svelte';
	import CapabilityRegistry from '$components/CapabilityRegistry.svelte';
	import MetaProofLog from '$components/MetaProofLog.svelte';
	import { Brain, Sparkles, TrendingUp, Zap } from 'lucide-svelte';

	const stats = [
		{ label: 'Opportunities Found', value: '47', icon: TrendingUp, color: 'blue' },
		{ label: 'AI Agents Active', value: '12', icon: Brain, color: 'teal' },
		{ label: 'Businesses Generated', value: '8', icon: Sparkles, color: 'purple' },
		{ label: 'Revenue Potential', value: '$2.3M', icon: Zap, color: 'amber' }
	];
</script>

<svelte:head>
	<title>Verity AI - Autonomous Business Generator</title>
</svelte:head>

<div class="container mx-auto px-4 py-8 max-w-7xl">
	<!-- Header -->
	<header class="mb-12">
		<div class="flex items-center justify-between mb-6">
			<div>
				<h1 class="text-5xl font-bold mb-2 gradient-text">Verity AI</h1>
				<p class="text-zinc-400 text-lg">Autonomous Business Generator Platform</p>
			</div>
			<AIThinkingIndicator />
		</div>
		
		<!-- Stats Grid -->
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
			{#each stats as stat}
				<GlassCard class="p-6 glass-hover">
					<div class="flex items-center justify-between">
						<div>
							<p class="text-zinc-400 text-sm mb-1">{stat.label}</p>
							<p class="text-3xl font-bold">{stat.value}</p>
						</div>
						<div class="p-3 rounded-lg bg-{stat.color}-500/10">
							<svelte:component this={stat.icon} class="w-6 h-6 text-{stat.color}-400" />
						</div>
					</div>
				</GlassCard>
			{/each}
		</div>
	</header>

	<!-- Main Content Grid -->
	<div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
		<!-- Opportunities Feed -->
		<div class="lg:col-span-2 space-y-4">
			<h2 class="text-2xl font-bold mb-4">Live Opportunities</h2>
			<OpportunityCard />
		</div>
		
		<!-- Sidebar -->
		<div class="space-y-6">
			<PipelineVisualization />
			<CapabilityRegistry />
		</div>
	</div>
	
	<!-- Meta-Proof Log -->
	<MetaProofLog />
</div>