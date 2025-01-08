$(document).ready(function() {
  $('#cosmetic_id').select2({
    ajax: {
      url: '/search_cosmetics/',  // 正しいURLを設定
      dataType: 'json',
      delay: 250,
      data: function(params) {
        return {
          keyword: params.term // 検索キーワード
        };
      },
      processResults: function(data) {
        return {
          results: data.results.map(function(cosmetic) {
            return { id: cosmetic.id, text: cosmetic.name };
          })
        };
      },
      cache: true
    },
    placeholder: 'コスメを選択または検索',
    minimumInputLength: 1,
    templateResult: formatCosmetic,
    templateSelection: formatCosmeticSelection
  });

  function formatCosmetic(cosmetic) {
    if (cosmetic.loading) {
      return cosmetic.text;
    }
    var markup = `<div>${cosmetic.text}</div>`;
    return markup;
  }

  function formatCosmeticSelection(cosmetic) {
    return cosmetic.text || cosmetic.id;
  }
});

