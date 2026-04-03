def paginate_queryset(queryset, request, page_size=10):
    """
    Reusable pagination utility.
    Pass any queryset + request → returns paginated data + metadata.
    """
    try:
        page = int(request.query_params.get('page', 1))
        size = int(request.query_params.get('page_size', page_size))
    except (ValueError, TypeError):
        page = 1
        size = page_size

    total = queryset.count()
    total_pages = max(1, (total + size - 1) // size)
    page = max(1, min(page, total_pages))

    start = (page - 1) * size
    end = start + size

    return {
        'queryset': queryset[start:end],
        'meta': {
            'total': total,
            'page': page,
            'page_size': size,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1,
        }
    }