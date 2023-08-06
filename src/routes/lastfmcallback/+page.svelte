<script>
    import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import {setCookie} from '$lib/cookieUtils.js';

  onMount(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const accessToken = searchParams.get("token");
    console.log(accessToken);
    setCookie('LastFmToken', accessToken, 0.04);
    goto('/');
  });
</script>

<main>
  <h1>Callback Page</h1>
  <p>Processing the LastFM redirect...</p>
</main>
