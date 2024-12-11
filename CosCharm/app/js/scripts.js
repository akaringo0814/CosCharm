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
