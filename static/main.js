document.addEventListener('DOMContentLoaded', () => {

    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const reviewsGrid = document.getElementById('reviewsGrid');

    // pega os elementos que vamos usar na pagina:
    // campo de pesquisa, botao de pesquisar e local onde os cards vao aparecer


    // funcao para buscar as avaliacoes na api
    // recebe o que foi pesquisado e envia para o backend
    async function fetchReviews(query = '') {
        try {
            // chama a rota do reviews do backend
            // envia o termo pesquisado, a pagina e a quantidade de resultados
            const response = await fetch(`/reviews?q=${encodeURIComponent(query)}&page=1&limit=10`);
            const data = await response.json();

            reviewsGrid.innerHTML = '';

            // verifica se a pesquisa nao encontrou nenhum filme
            // se nao encontrar, mostra uma mensagem e para a funcao
            if (data.results.length === 0) {
                reviewsGrid.innerHTML = '<p style="color: #8a99ad; text-align: center; grid-column: 1/-1;">Nenhum filme encontrado.</p>';
                return;
            }

            // passa por cada review encontrada
            // para cada uma, cria um card com as informacoes do filme
            data.results.forEach(review => {
                const card = document.createElement('div');
                card.className = 'card';

                // coloca dentro do card a capa, titulo, usuario, nota e comentario
                // se o filme nao tiver capa, usa uma imagem padrao
                card.innerHTML = `
                    <img src="${review.poster_url || 'https://via.placeholder.com/220x300'}" alt="${review.movie_title}">
                    <div class="card-body">
                        <div class="card-title">${review.movie_title}</div>
                        <div class="card-author">Por @${review.user_username}</div>
                        <div class="rating">★ ${review.rating}/10</div>
                        <div class="content">${review.content}</div>
                    </div>
                `;

                // coloca o card pronto dentro do grid da pagina
                reviewsGrid.appendChild(card);
            });

        // caso aconteca algum erro na busca, mostra o erro no console
        // e uma mensagem para o usuario na tela
        } catch (error) {
            console.error('Erro ao buscar reviews:', error);
            reviewsGrid.innerHTML = '<p style="color: #e91e63;">Erro ao carregar os dados.</p>';
        }
    }


    // quando clicar no botao pesquisar, pega o que foi digitado
    // tira os espacos desnecessarios e chama a funcao de busca
    searchBtn.addEventListener('click', () => {
        fetchReviews(searchInput.value.trim());
    });


    // permite fazer a pesquisa apertando enter
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            fetchReviews(searchInput.value.trim());
        }
    });


    // faz uma busca assim que a pagina abre
    fetchReviews();
});