<script lang="ts">
	import '../app.css';
	import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';

	const queryClient = new QueryClient({
		defaultOptions: {
			queries: {
				retry: 1,
				refetchOnWindowFocus: false,
				staleTime: 5 * 60 * 1000 // 5 minutes
			}
		}
	});
</script>

<QueryClientProvider client={queryClient}>
	<div class="min-h-screen w-full noise-texture">
		<slot />
	</div>
</QueryClientProvider>