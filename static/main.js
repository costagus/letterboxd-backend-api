document.addEventListener('DOMContentLoaded', () => {
    let page = 1;

    // Alterna a tela e carrega os dados conforme a hash (#users/1 ou vazia)
    async function navegar() {
        const hash = window.location.hash;
        const reviewsView = document.getElementById('reviewsView');
        const userView = document.getElementById('userView');

        // Se a URL tiver #users/ID, carrega o perfil do utilizador
        if (hash.startsWith('#users/')) {
            reviewsView.style.display = 'none';
            userView.style.display = 'block';

            const userId = hash.replace('#users/', '');
            const res = await fetch(`/users/${userId}`);
            
            if (!res.ok) {
                document.getElementById('userContainer').innerHTML = '<p style="color: #e91e63;">Usuário não encontrado.</p>';
                return;
            }

            const user = await res.json();

            document.getElementById('userContainer').innerHTML = `
                <div class="profile-card">
                    <img src="${user.avatar_url || 'https://via.placeholder.com/150'}" class="profile-avatar">
                    <div>
                        <h2>${user.name} (@${user.username})</h2>
                        <p style="color: #8a99ad;">${user.bio || 'Sem biografia.'}</p>
                    </div>
                </div>
                <h3 style="margin: 30px 0 15px 0;">Avaliações de ${user.name} (${user.reviews.length})</h3>
                <div class="grid">
                    ${user.reviews.map(r => `
                        <div class="card">
                            <img src="${r.poster_url || 'https://via.placeholder.com/220x300'}">
                            <div class="card-body">
                                <div class="card-title">${r.movie_title}</div>
                                <div class="rating">★ ${r.rating}/10</div>
                                <div class="content">${r.content}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            // Se não tiver #users/, exibe a lista de reviews com busca e paginação
            userView.style.display = 'none';
            reviewsView.style.display = 'block';

            const busca = document.getElementById('searchInput').value.trim();
            const res = await fetch(`/reviews?q=${encodeURIComponent(busca)}&page=${page}&limit=6`);
            const data = await res.json();

            document.getElementById('pageInfo').textContent = `Página ${page}`;
            const grid = document.getElementById('reviewsGrid');
            grid.innerHTML = data.results.length ? '' : '<p style="color: #8a99ad; grid-column: 1/-1; text-align: center;">Nenhum filme encontrado.</p>';

            data.results.forEach(r => {
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <img src="${r.poster_url || 'https://via.placeholder.com/220x300'}">
                    <div class="card-body">
                        <div class="card-title">${r.movie_title}</div>
                        <div class="card-author">
                            Por <a href="#users/${r.user_id}" class="user-link">@${r.user_username}</a>
                        </div>
                        <div class="rating">★ ${r.rating}/10</div>
                        <div class="content">${r.content}</div>
                    </div>
                `;
                grid.appendChild(card);
            });
        }
    }

    // eventos de clique e navegação
    document.getElementById('searchBtn').onclick = () => { page = 1; navegar(); };
    document.getElementById('searchInput').onkeypress = (e) => { if (e.key === 'Enter') { page = 1; navegar(); } };
    document.getElementById('prevBtn').onclick = () => { if (page > 1) { page--; navegar(); } };
    document.getElementById('nextBtn').onclick = () => { page++; navegar(); };
    document.getElementById('backBtn').onclick = () => { window.location.hash = ''; };
    document.getElementById('navHome').onclick = () => { window.location.hash = ''; };

    window.onhashchange = navegar;
    navegar();
});