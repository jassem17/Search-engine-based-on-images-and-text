def index_search(es, index: str, keywords: str, size: int) -> dict:
    """
    Args:
        es: Elasticsearch client instance.
        index: Name of the index we are going to use.
        keywords: Search keywords.
        filters: Tag name to filter medium stories.
        from_i: Start index of the results for pagination.
        size: Number of results returned in each search.
    """
    # search query
    body = {

        'query': {
            'match': {
                'tags': {
                    'query': keywords,
                    'fuzziness': 'AUTO'
                }
            },
        },

        'highlight': {
            'pre_tags': ['<b>'],
            'post_tags': ['</b>'],
            'fields': {'tags': {}}
        },
        'size': size,

    }


    res = es.search(index=index, body=body)

    return res

