document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const container = document.querySelector('.com');

    // Create and insert a loader element
    const loader = document.createElement('div');
    loader.classList.add('loader');
    loader.style.display = 'none';
    loader.innerHTML = `
        <div class="spinner"></div>
        <p style="color: black;">Collecting Video Information Please Wait....</p>
    `;
    container.appendChild(loader);

    // Show loader on form submit
    form.addEventListener('submit', () => {
        loader.style.display = 'block';
    });

    // Scroll to content when results are loaded
    if (window.location.href.includes('#result')) {
        document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
    }
});
