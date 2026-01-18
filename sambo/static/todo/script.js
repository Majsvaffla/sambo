if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.documentElement.classList.add("wa-dark");
}

window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", event => {
    document.documentElement.classList.toggle("wa-dark", event.matches);
});
