



def hit_rate_at_k(retrieved_pages:list[int],target_pages:list[int],k:int):
    considering = retrieved_pages[:k]

    for index,val in enumerate(considering):
        if val in target_pages:
            return 1
    return 0

def mrr_at_k(retrieved_pages:list[int],target_pages:list[int],k:int):
    considering = retrieved_pages[:k]

    for index,val in enumerate(considering,start=1):
        if val in target_pages:
            score  = 1.0/index
            return score
    return 0