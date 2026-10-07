document.addEventListener('DOMContentLoaded', () => {
    let page = 1;

    // function auxiliar para mudar a URL no navegador sem recarregar e sem usar spa/#
    function irPara(url) {
        window.history.pushState({}, '', url);
        navegar();
    }

    // alternando a tela e carregando os dados conforme a rota da URL (/users/1 ou /reviews)
    async function navegar() {
        const path = window.location.pathname;
        const search = window.location.search;
        const params = new URLSearchParams(search);

        const reviewsView = document.getElementById('reviewsView');
        const userView = document.getElementById('userView');

        // checa se a URL for /users/ID ou ?user=ID, carregando o perfil do usuário
        const userId = params.get('user') || (path.startsWith('/users/') ? path.replace('/users/', '') : null);
        if (userId) {
            reviewsView.style.display = 'none';
            userView.style.display = 'block';

            const res = await fetch(`/users/${userId}`, { headers: { 'Accept': 'application/json' } });            
            
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
            // mas se for a tela inicial ou de busca, exibe as reviews com paginação
            userView.style.display = 'none';
            reviewsView.style.display = 'block';

            // agr pega o termo e a página direto dos parâmetros da URL se existirem
            const buscaInput = document.getElementById('searchInput').value.trim();
            const termo = params.get('termo') || params.get('q') || buscaInput;
            page = parseInt(params.get('page')) || page;

            document.getElementById('searchInput').value = termo;
            document.getElementById('pageInfo').textContent = `Página ${page}`;

            const res = await fetch(`/reviews?termo=${encodeURIComponent(termo)}&page=${page}&limit=6`);
            const data = await res.json();

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
                            Por <a href="/users/${r.user_id}" class="user-link">@${r.user_username}</a>
                        </div>
                        <div class="rating">★ ${r.rating}/10</div>
                        <div class="content">${r.content}</div>
                    </div>
                `;

                // clicando no autor p atualizar a URL para /users/ID sem recarregar a tela
                card.querySelector('.user-link').onclick = (e) => {
                    e.preventDefault();
                    irPara(`/users/${r.user_id}`);
                };

                grid.appendChild(card);
            });
        }
    }

    // aqui temos os eventos de clique e busca atualizando a URL certinha (/reviews?termo=...&page=...)
    function dispararBusca() {
        const busca = document.getElementById('searchInput').value.trim();
        page = 1;
        irPara(`/reviews?termo=${encodeURIComponent(busca)}&page=${page}&limit=6`);
    }

    document.getElementById('searchBtn').onclick = dispararBusca;
    document.getElementById('searchInput').onkeypress = (e) => { 
        if (e.key === 'Enter') dispararBusca(); 
    };

    document.getElementById('prevBtn').onclick = () => { 
        if (page > 1) { 
            page--; 
            const busca = document.getElementById('searchInput').value.trim();
            irPara(`/reviews?termo=${encodeURIComponent(busca)}&page=${page}&limit=6`);
        } 
    };

    document.getElementById('nextBtn').onclick = () => { 
        page++; 
        const busca = document.getElementById('searchInput').value.trim();
        irPara(`/reviews?termo=${encodeURIComponent(busca)}&page=${page}&limit=6`);
    };

    // botões de voltar para a página inicial
    document.getElementById('backBtn').onclick = () => irPara('/');
    document.getElementById('navHome').onclick = () => irPara('/');

    //  botões de voltar/avançar do navegador
    window.onpopstate = navegar;
    navegar();
});