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
  

// 検索処理
function performSearch() {
  const keyword = document.getElementById('keyword-input').value;
  const category = document.getElementById('category-select').value;

  fetch(`/search/?keyword=${keyword}&category=${category}`)
      .then(response => response.json())
      .then(data => {
          const resultsContainer = document.getElementById('search-results');
          resultsContainer.innerHTML = ''; // 初期化

          data.results.forEach(item => {
              const div = document.createElement('div');
              div.className = 'search-result-item';
              div.textContent = `${item.cosmetic_name} (${item.category} - ${item.subcategory})`;
              div.dataset.id = item.id; // コスメIDをデータ属性に追加
              resultsContainer.appendChild(div);
          });
      });
}

// 検索結果をクリックしたときにフォームに反映
document.getElementById('search-results').addEventListener('click', (e) => {
  if (e.target.classList.contains('search-result-item')) {
      const cosmeticId = e.target.dataset.id; // データ属性からIDを取得
      document.getElementById('cosmetic_id').value = cosmeticId; // フォームにセット
  }
});

