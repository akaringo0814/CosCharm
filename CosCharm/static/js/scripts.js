function performSearch() {
    // キーワード検索ロジックをここに記述
  }
  
  function filterByCategory() {
    // カテゴリフィルタリングロジックをここに記述
  }
  
  function confirmSelection() {
    // 選択されたコスメのIDを取得
    var selectedCosmeticId = document.getElementById('cosmetic_id').value;
  
    // 使用状況を取得
    var usageStatus = document.querySelector('input[name="usage_status"]:checked').value;
  
    // お気に入りチェックボックスの状態を取得
    var isFavorite = document.getElementById('is_favorite').checked;
  
    // 確認メッセージを表示
    alert("選択されたコスメID: " + selectedCosmeticId + "\n使用状況: " + usageStatus + "\nお気に入り登録: " + isFavorite);
  
    // 追加の処理をここに記述 (例: フォームデータの送信など)
  }
  
  function performSearch() {
    var keyword = document.getElementById('keyword-input').value.toLowerCase();
    var category = document.getElementById('category-select').value;
    var resultsContainer
  }
  $(function(){
    $('.search-section').select2();
});

function performSearch() {
  const keyword = document.getElementById('keyword-input').value;
  const category = document.getElementById('category-select').value;

  fetch(`/search/?keyword=${encodeURIComponent(keyword)}&category=${encodeURIComponent(category)}`)
      .then(response => response.json())
      .then(data => {
          const resultsContainer = document.getElementById('search-results');
          resultsContainer.innerHTML = '';

          if (data.results.length > 0) {
              data.results.forEach(item => {
                  const div = document.createElement('div');
                  div.classList.add('result-item');
                  div.innerHTML = `
                      <h5>${item.name}</h5>
                      <p>ブランド: ${item.brand}</p>
                      <p>カテゴリ: ${item.category}</p>
                      <p>価格: ¥${item.price.toLocaleString()}</p>
                  `;
                  resultsContainer.appendChild(div);
              });
          } else {
              resultsContainer.textContent = '該当するコスメが見つかりません。';
          }
      })
      .catch(error => console.error('Error:', error));
}
