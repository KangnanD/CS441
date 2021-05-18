  $('#search_posts')
  .search({
    apiSettings: {
      url: '/api/search_posts?name={query}'
    },
    fields: {
      results : 'results',
      title   : 'title',
      description : 'content',
      content : 'content',
      url     : 'post_url',
    },
    minCharacters : 3
  });

  $('#search_courses')
  .search({
    apiSettings: {
      url: '/api/courses?name={query}'
    },
    fields: {
      results : 'results',
      title   : 'name',
      url     : 'course_url',
      image   : 'image_url',
    },
    minCharacters : 3
  });

