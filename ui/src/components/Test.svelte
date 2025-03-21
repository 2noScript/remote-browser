<script>
    import {apiClient} from '../utils'
    const res = apiClient.get('/ping');
</script>

{#await res}
	<!-- promise is pending -->
	<p>waiting for the promise to resolve...</p>
{:then value}
	<!-- promise was fulfilled or not a Promise -->
	<p>The value is {JSON.stringify(value.data)}</p>
{:catch error}
	<!-- promise was rejected -->
	<p>Something went wrong: {error.message}</p>
{/await}