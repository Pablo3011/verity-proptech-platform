<script lang="ts">
	import GlassCard from './GlassCard.svelte';
	import { TrendingUp, Users, DollarSign, CheckCircle2, ExternalLink } from 'lucide-svelte';
	import type { Opportunity } from '$types';
	
	// Mock data - will be replaced with real API data
	const opportunities: Opportunity[] = [
		{
			id: '1',
			title: 'AI-Powered Customer Service Platform',
			description: 'Automated customer support using GPT-4 for e-commerce businesses',
			market: 'SaaS / Customer Service',
			score: 92,
			trend: 47,
			competition: 'low',
			revenue_potential: '$500K - $2M ARR',
			validated: true,
			source: 'Google Trends',
			discovered_at: '2 hours ago'
		},
		{
			id: '2',
			title: 'Sustainable Packaging Marketplace',
			description: 'B2B marketplace connecting eco-friendly packaging suppliers with retailers',
			market: 'E-commerce / Sustainability',
			score: 87,
			trend: 35,
			competition: 'medium',
			revenue_potential: '$300K - $1.5M ARR',
			validated: true,
			source: 'Semrush',
			discovered_at: '5 hours ago'
		},
		{
			id: '3',
			title: 'Remote Team Wellness App',
			description: 'Mental health and wellness platform for distributed teams',
			market: 'HR Tech / Wellness',
			score: 84,
			trend: 28,
			competition: 'medium',
			revenue_potential: '$200K - $1M ARR',
			validated: false,
			source: 'Market Analysis',
			discovered_at: '1 day ago'
		}
	];
	
	function getCompetitionColor(competition: string) {
		switch (competition) {
			case 'low': return 'text-green-400';
			case 'medium': return 'text-amber-400';
			case 'high': return 'text-red-400';
			default: return 'text-zinc-400';
		}
	}
</script>

<div class="space-y-4">
	{#each opportunities as opp}
		<GlassCard class="p-6 glass-hover cursor-pointer animate-slide-up">
			<div class="flex items-start justify-between mb-4">
				<div class="flex-1">
					<div class="flex items-center gap-2 mb-2">
						<h3 class="text-lg font-semibold">{opp.title}</h3>
						{#if opp.validated}
							<CheckCircle2 class="w-4 h-4 text-green-400" />
						{/if}
					</div>
					<p class="text-sm text-zinc-400 mb-3">{opp.description}</p>
					<p class="text-xs text-zinc-500">{opp.market}</p>
				</div>
				<div class="text-right">
					<div class="text-2xl font-bold gradient-text mb-1">{opp.score}</div>
					<div class="text-xs text-zinc-500">Score</div>
				</div>
			</div>
			
			<div class="grid grid-cols-3 gap-4 py-3 border-t border-zinc-800">
				<div class="flex items-center gap-2">
					<TrendingUp class="w-4 h-4 text-blue-400" />
					<div>
						<div class="text-sm font-medium">+{opp.trend}%</div>
						<div class="text-xs text-zinc-500">Trend</div>
					</div>
				</div>
				
				<div class="flex items-center gap-2">
					<Users class="w-4 h-4 {getCompetitionColor(opp.competition)}" />
					<div>
						<div class="text-sm font-medium capitalize">{opp.competition}</div>
						<div class="text-xs text-zinc-500">Competition</div>
					</div>
				</div>
				
				<div class="flex items-center gap-2">
					<DollarSign class="w-4 h-4 text-teal-400" />
					<div>
						<div class="text-sm font-medium">{opp.revenue_potential.split(' ')[0]}</div>
						<div class="text-xs text-zinc-500">Potential</div>
					</div>
				</div>
			</div>
			
			<div class="flex items-center justify-between pt-3 border-t border-zinc-800">
				<div class="flex items-center gap-2 text-xs text-zinc-500">
					<span>Source: {opp.source}</span>
					<span>•</span>
					<span>{opp.discovered_at}</span>
				</div>
				<button class="flex items-center gap-1 text-sm text-blue-400 hover:text-blue-300 transition-colors">
					Explore
					<ExternalLink class="w-3 h-3" />
				</button>
			</div>
		</GlassCard>
	{/each}
</div>