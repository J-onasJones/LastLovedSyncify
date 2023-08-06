<script>

    import { goto } from '$app/navigation';
  import {getCookie} from '$lib/cookieUtils.js';
  
    const SpotifyclientId = 'd01716d4caf143e28ffce2c0ebab6f4b';
    const SpotifyRedirectUri = 'http://localhost:5173/spotifycallback';
    const SpotifyApiScopes = 'user-library-read';
    const LastFmApiKey = '2753b46a0cababd06a7fcb3c5881072a';
    const LastFmRedirectUri = 'http://localhost:5173/lastfmcallback';
    /**
     * @type {any[]}
     */
    export let likedSongs = [];
    let currentPage = 1;
    let totalItems = 1;
    export let itemsPerPage = 10;
    /**
     * @type {any[]}
     */
     export let items = [];
    export let totalPages = Math.ceil(totalItems / itemsPerPage);
    export let fetched = false;
  
    const handleSpotifyLogin = () => {
      // Spotify Authorization URL
      const authorizeUrl = `https://accounts.spotify.com/authorize?client_id=${SpotifyclientId}&redirect_uri=${encodeURIComponent(SpotifyRedirectUri)}&response_type=token&scope=${encodeURIComponent(SpotifyApiScopes)}`;
  
      // Open Spotify authorization page
      goto(authorizeUrl);
    };

    const handleLastFmLogin = () => {
      // LastFM Authorization URL
      const authorizeUrl = `http://www.last.fm/api/auth/?api_key=${LastFmApiKey}&cb=${encodeURIComponent(LastFmRedirectUri)}`;

      // Open LastFM authorization page
      goto(authorizeUrl);
    }

    /**
     * @param {string} accessToken
     */
    async function apiSongGetter(accessToken, offset = 0, limit= 1) {
      try {
      const response = await fetch(`https://api.spotify.com/v1/me/tracks?market=DE&limit=${limit}&offset=${offset}`, {
        headers: {
          "Authorization": `Bearer ${accessToken}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        console.error("Failed to fetch liked songs:", response.statusText);
      }
      } catch (error) {
        console.error("Error fetching liked songs:", error);
      }
    }

    /**
     * @param {string} accessToken
     */
    async function getLikedSongs(accessToken) {
      // @ts-ignore
      document.getElementById("main").style.display = "none";
      // @ts-ignore
      document.getElementById("loading").style.display = "block";
      let total = await getLikedLength(accessToken);
      let limit = 50;
      //loop through all pages of liked songs
      for (let offset = 0; offset < total; offset += 50) {
        likedSongs = likedSongs.concat(await getnextLikedSongs(accessToken, offset, limit = 50));
      }
      // @ts-ignore
      document.getElementById("loading").style.display = "none";
      // @ts-ignore
      document.getElementById("main").style.display = "block";
      refreshItems(1);
      fetched = true;
    }

    /**
     * @param {string} accessToken
     */
    async function getLikedLength(accessToken) {
      const data = await apiSongGetter(accessToken, 0, 1);
      totalItems = data.total;
      refreshItems(1);
      return data.total;
    }
  
    /**
     * @param {string} accessToken
     */
    async function getnextLikedSongs(accessToken, offset = 0, limit = 50) {
      
      const data = await apiSongGetter(accessToken, offset, limit);
      return data.items.map((/** @type {{ track: any; }} */ item) => {
        const track = item.track;
        return {
          name: track.name,
          artist: track.artists[0].name
        };
      });
  }

  /**
     * @param {{ target: { value: string | number; }; }} event
     */
  function changePage(event) {
    currentPage = +event.target.value;
  }

  /**
     * @param {{ target: { value: string | number; }; }} event
     */
  function changeItemsPerPage(event) {
    itemsPerPage = +event.target.value;
    currentPage = 1;
    refreshItems(currentPage);
  }

  /**
     * @param {number} newpage
     */
  function refreshItems(newpage) {
    currentPage = newpage;
    totalPages = Math.ceil(totalItems / itemsPerPage);
    //given the likedsongs list, select the currently visible items in the list
    items = likedSongs.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
  }


  </script>
  <link rel="stylesheet" href="/+page.css">
  <h1>Last Loved Syncify</h1>
  <main id="main">
    <button on:click={handleSpotifyLogin}>Log in with Spotify</button>
    <button on:click={handleLastFmLogin}>Log in with LastFM</button>
    <button on:click={() => getLikedSongs(getCookie('SpotifyToken'))}>Get Liked Songs</button>
    
    <div class="pagination">
      <span>Page:</span>
      <select bind:value={currentPage} on:change={changePage}>
        {#each Array(totalPages) as _, i}
          <option value={i + 1}>Page {i + 1}</option>
        {/each}
      </select>
    
      <span>Items per page:</span>
      <select on:change={changeItemsPerPage}>
        <option value="5">5</option>
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="50">50</option>
      </select>
    
      <div class="pagination-buttons">
        <button on:click={() => refreshItems(currentPage = 1)} disabled={currentPage === 1}>First</button>
        <button on:click={() => refreshItems(currentPage -= 1)} disabled={currentPage === 1}>Previous</button>
    
        {#if currentPage - 2 >= 1}
          <button on:click={() => refreshItems(currentPage -= 2)}>{currentPage - 2}</button>
        {/if}
    
        {#if currentPage - 1 > 1}
          <button on:click={() => refreshItems(currentPage -= 1)}>{currentPage - 1}</button>
        {/if}
    
        <button class="current-page" disabled>{currentPage}</button>
    
        {#if currentPage + 1 <= totalPages}
          <button on:click={() => refreshItems(currentPage += 1)}>{currentPage + 1}</button>
        {/if}
    
        {#if currentPage + 2 <= totalPages}
          <button on:click={() => refreshItems(currentPage += 2)}>{currentPage + 2}</button>
        {/if}
    
        <button on:click={() => refreshItems(currentPage += 1)} disabled={currentPage === totalPages}>Next</button>
        <button on:click={() => refreshItems(currentPage = totalPages)} disabled={currentPage === totalPages}>Last</button>
      </div>
    </div>
    <h2>Liked Songs</h2>
    {#each items as song}
      <p>{song.name} by {song.artist}</p>
    {/each}
  </main>

  <p id="loading" style="display: none;">Loading your liked songs. This process may take a few seconds (and in rare cases even up to minutes) depending on how many songs you've liked.</p>