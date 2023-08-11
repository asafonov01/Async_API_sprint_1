async def common_list_params(page: int = 1, limit: int = 50):
    from_ind: int = (page - 1) * limit
    return {'from_ind': from_ind, 'limit': limit}
