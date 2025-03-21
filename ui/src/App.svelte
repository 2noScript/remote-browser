<script>
  import { wrap } from "svelte-spa-router/wrap";
  import Router from "svelte-spa-router";
  import { link } from "svelte-spa-router";
  import Home from "./pages/Home.svelte";
  import About from "./pages/About.svelte";
  import "./app.css";

  const routes = {
    "/": wrap({ component: Home }),
    "/about": wrap({ component: About }),
  };
</script>


<svelte:head>
  <!-- Fonts -->
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/icon?family=Material+Icons"
  />
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,600,700"
  />

  <!-- Material Typography -->
  <link
    rel="stylesheet"
    href="https://unpkg.com/@material/typography@14.0.0/dist/mdc.typography.css"
  />

  <!-- SMUI -->
  <link rel="stylesheet" href="https://unpkg.com/svelte-material-ui/bare.css" />
</svelte:head>
<nav>
  <a href="/" use:link >Home</a>
  <a href="/about" use:link>About</a>
</nav>
<main>


  <Router {routes} />
</main>
