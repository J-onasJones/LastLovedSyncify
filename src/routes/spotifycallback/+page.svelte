<script>
    import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import {setCookie} from '$lib/cookieUtils.js';

  onMount(() => {
    console.log('Callback page mounted');
    const hashParams = new URLSearchParams(window.location.hash.substr(1));
    const accessToken = hashParams.get("access_token");
    setCookie('SpotifyToken', accessToken, 0.04);
    goto('/');
  });
</script>

<main>
  <h1>Callback Page</h1>
  <p>Processing the Spotify redirect...</p>
</main>
