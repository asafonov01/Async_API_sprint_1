from fastapi import Query


async def common_list_params(
    page: int = Query(title='page number', default=1, ge=1),
    limit: int = Query(title='page size', default=50, ge=1)
):
    from_ind: int = (page - 1) * limit
    return {'from_ind': from_ind, 'limit': limit}
