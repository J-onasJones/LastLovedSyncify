<script>

    import { goto } from '$app/navigation';
  import {getCookie} from '$lib/cookieUtils.js';
  import { page } from '$app/stores';
  
    const SpotifyclientId = 'd01716d4caf143e28ffce2c0ebab6f4b';
    const SpotifyRedirectUri = $page.url + 'spotifycallback';
    console.log(SpotifyRedirectUri);
    const SpotifyApiScopes = 'user-library-read';
    const LastFmApiKey = '2753b46a0cababd06a7fcb3c5881072a';
    const LastFmRedirectUri = 'http://localhost:5173/lastfmcallback';
    /**
     * @type {any[]}
     */
    export let likedSongs = [];
    /**
     * @type {number[]}
     */
    export let selectedSongs = [];
    export let selectAll = false;
    export let apireturnlength = 69;
    let currentPage = 1;
    let totalItems = 1;
    export let itemsPerPage = 10;
    /**
     * @type {any[]}
     */
     export let items = [];
    export let totalPages = Math.ceil(totalItems / itemsPerPage);
    export let fetched = false;

    /**
     * @param {number} songNumber
     */
    function toggleSelection(songNumber) {
    if (selectedSongs.includes(songNumber)) {
      selectedSongs = selectedSongs.filter(num => num !== songNumber);
    } else {
      selectedSongs = [...selectedSongs, songNumber];
    }
  }

  function toggleSelectAll() {
    if (selectAll) {
      selectedSongs = [];
    } else {
      selectedSongs = items.map(song => song.number);
    }
    selectAll = !selectAll;
  }



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
      //document.getElementById("main").style.display = "none";
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
      // @ts-ignore
      document.getElementById("displaysongtablediv").style.display = "block";
      // @ts-ignore
      document.getElementById("instructionbuttons").style.display = "none";
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
      apireturnlength = data.total;
      return data.total;
    }
  
    /**
     * @param {string} accessToken
     * @param {number} offset
     */
    async function getnextLikedSongs(accessToken, offset, limit = 50) {
    const data = await apiSongGetter(accessToken, offset, limit);
    
    let counter = offset + 1; // Initialize counter with the starting offset
    
    const result = data.items.map((/** @type {{ track: any; }} */ item) => {
      const track = item.track;
      const mappedItem = {
        name: track.name,
        artist: track.artists[0].name,
        number: counter
      };
      counter++; // Increment the counter for the next item
      return mappedItem;
    });

    return result;
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
    <p>Sync your Spotify liked songs to LastFM</p>
    <div id="instructionbuttons">
      <div style="width: 30%;float:left;clear:none">
        <h3>1. Log in with Spotify</h3>
        <button on:click={handleSpotifyLogin}>Spotify</button>
      </div>
      <div style="width: 30%;float:left;clear:none">
        <h3>2. Log in with LastFM</h3>
        <button on:click={handleLastFmLogin}>LastFM</button>
      </div>
      <div style="width: 30%;float:left;clear:none">
        <h3>3. Load Your Liked Songs</h3>
        <button on:click={() => getLikedSongs(getCookie('SpotifyToken'))}>Start Loading</button>
      </div>
    </div>
    
    <div id="displaysongtablediv" style="display: none">
      <h3>These are Your Liked Songs:</h3>
      <p>Select Songs to add to your LastFM loved songs</p>
      <p>Are you done?</p>
      <button>Sync Selected Songs</button>
      <button>Sync All Songs</button>
      <div class="pagination">
        <span>Page:</span>
        <select bind:value={currentPage} on:change={refreshItems(currentPage)}>
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
          <option value="100">100</option>
        </select>
    
        <div class="pagination-buttons">
          <button on:click={() => refreshItems(currentPage = 1)} disabled={currentPage === 1}>&lt;&lt;</button>
          <button on:click={() => refreshItems(currentPage -= 1)} disabled={currentPage === 1}>&lt;</button>
      
          {#if currentPage - 2 >= 1}
            <button on:click={() => refreshItems(currentPage -= 2)}>{currentPage - 2}</button>
          {:else}
            <button>-</button>
          {/if}
      
          {#if currentPage - 1 >= 1}
            <button on:click={() => refreshItems(currentPage -= 1)}>{currentPage - 1}</button>
          {:else}
            <button>-</button>
          {/if}
      
          <button class="current-page" disabled>{currentPage}</button>
      
          {#if currentPage + 1 <= totalPages}
            <button on:click={() => refreshItems(currentPage += 1)}>{currentPage + 1}</button>
          {:else}
            <button>-</button>
          {/if}
      
          {#if currentPage + 2 <= totalPages}
            <button on:click={() => refreshItems(currentPage += 2)}>{currentPage + 2}</button>
          {:else}
            <button>-</button>
          {/if}
      
          <button on:click={() => refreshItems(currentPage += 1)} disabled={currentPage === totalPages}>&gt;</button>
          <button on:click={() => refreshItems(currentPage = totalPages)} disabled={currentPage === totalPages}>&gt;&gt;</button>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>
              <label>
                <input type="checkbox"  on:change={toggleSelectAll} />
              </label>
            </th>
            <th>Nr.</th>
            <th>Name</th>
            <th>Artist</th>
          </tr>
        </thead>
        <tbody>
          {#each items as song}
            <tr>
              <td>
                <input
                  type="checkbox"
                  checked={selectedSongs.includes(song.number)}
                  on:change={() => toggleSelection(song.number)}
                />
              </td>
              <td>{song.number}</td>
              <td>{song.name}</td>
              <td>{song.artist}</td>
            </tr>
          {/each}
        </tbody>
      </table>
      <div class="pagination">
        <span>Page:</span>
        <select bind:value={currentPage} on:change={refreshItems(currentPage)}>
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
          <option value="100">100</option>
        </select>
    
        <div class="pagination-buttons">
          <button on:click={() => refreshItems(currentPage = 1)} disabled={currentPage === 1}>&lt;&lt;</button>
          <button on:click={() => refreshItems(currentPage -= 1)} disabled={currentPage === 1}>&lt;</button>
      
          {#if currentPage - 2 >= 1}
            <button on:click={() => refreshItems(currentPage -= 2)}>{currentPage - 2}</button>
          {:else}
            <button>-</button>
          {/if}
      
          {#if currentPage - 1 >= 1}
            <button on:click={() => refreshItems(currentPage -= 1)}>{currentPage - 1}</button>
          {:else}
            <button>-</button>
          {/if}
      
          <button class="current-page" disabled>{currentPage}</button>
      
          {#if currentPage + 1 <= totalPages}
            <button on:click={() => refreshItems(currentPage += 1)}>{currentPage + 1}</button>
          {:else}
            <button>-</button>
          {/if}
      
          {#if currentPage + 2 <= totalPages}
            <button on:click={() => refreshItems(currentPage += 2)}>{currentPage + 2}</button>
          {:else}
            <button>-</button>
          {/if}
      
          <button on:click={() => refreshItems(currentPage += 1)} disabled={currentPage === totalPages}>&gt;</button>
          <button on:click={() => refreshItems(currentPage = totalPages)} disabled={currentPage === totalPages}>&gt;&gt;</button>
        </div>
      </div>
    </div>
  </main>
  <div id="loading">
    <img src="/loading.gif" alt="Loading" height="30%"/>
    <p>{likedSongs.length}/{apireturnlength}</p>
    <p>Loading your liked songs...</p>
    <div class="progress-bar">
      <div class="progress" style="width: {likedSongs.length/apireturnlength * 100}%"><p style="position:absolute;left:47%;top:148px">{Math.round(likedSongs.length/apireturnlength * 100)}% {Math.round(likedSongs.length / apireturnlength * 100) === 69 ? "nice!" : ""}</p></div>
    </div>
    <p></p>
  </div>
  