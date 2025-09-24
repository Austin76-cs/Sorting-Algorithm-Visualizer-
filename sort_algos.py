import time
from typing import List

# Highlighting Colors for Sorting
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

def bubble_sort(arr, ascending=True):
    n = len(arr)
    local_arr = list(arr) 
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            yield local_arr, {j: RED, j + 1: RED}
            if (local_arr[j] > local_arr[j + 1] and ascending) or \
               (local_arr[j] < local_arr[j + 1] and not ascending):
                local_arr[j], local_arr[j+1] = local_arr[j+1], local_arr[j]
                swapped = True
                yield local_arr, {j: GREEN, j + 1: GREEN}
        if not swapped:
            break
    yield local_arr, {} 

def insertion_sort(arr, ascending=True):
    local_arr = list(arr)
    for i in range(1, len(local_arr)):
        key = local_arr[i]
        j = i - 1
        
        yield local_arr, {i: RED, j: RED} 

        while j >= 0 and ((local_arr[j] > key and ascending) or \
                          (local_arr[j] < key and not ascending)):
            local_arr[j + 1] = local_arr[j]
            j -= 1
            yield local_arr, {j + 1: RED, j: RED} 
        local_arr[j+1] = key

        yield local_arr, {j+1: GREEN}
    yield local_arr, {} 


def merge_sort(arr, ascending=True):
    local_arr = list(arr)

    def _merge_sort_recursive(sub_arr, start, end):
        if start < end:
            mid = (start + end) // 2
            yield from _merge_sort_recursive(sub_arr, start, mid)
            yield from _merge_sort_recursive(sub_arr, mid + 1, end)

            left_half = sub_arr[start:mid + 1]
            right_half = sub_arr[mid + 1:end + 1]
            i = j = 0
            k = start

            while i < len(left_half) and j < len(right_half):
                yield sub_arr, {start + i: RED, mid + 1 + j: RED} 
                if (left_half[i] <= right_half[j] and ascending) or \
                   (left_half[i] > right_half[j] and not ascending):
                    sub_arr[k] = left_half[i]
                    i += 1
                else:
                    sub_arr[k] = right_half[j]
                    j += 1
                k += 1
                yield sub_arr, {k-1: GREEN}
            
            while i < len(left_half):
                sub_arr[k] = left_half[i]
                i += 1
                k += 1
                yield sub_arr, {k-1: GREEN}

            while j < len(right_half):
                sub_arr[k] = right_half[j]
                j += 1
                k += 1
                yield sub_arr, {k-1: GREEN}
    
    yield from _merge_sort_recursive(local_arr, 0, len(local_arr) - 1)
    yield local_arr, {} 


def quick_sort(arr, ascending=True, low=0, high=None):
    local_arr = list(arr)

    if high is None:
        high = len(local_arr) - 1

    stack = [(low, high)]

    while stack:
        low, high = stack.pop()

        if low < high:
            pivot_index = high
            pivot = local_arr[pivot_index]
            i = low - 1

            yield local_arr, {pivot_index: GREEN}

            for j in range(low, high):
                yield local_arr, {j: RED, pivot_index: GREEN}
                if (local_arr[j] <= pivot and ascending) or \
                   (local_arr[j] > pivot and not ascending):
                    i += 1
                    local_arr[i], local_arr[j] = local_arr[j], local_arr[i]
                    yield local_arr, {i: GREEN, j: GREEN, pivot_index: GREEN} 
            
            local_arr[i + 1], local_arr[high] = local_arr[high], local_arr[i + 1]
            pi = i + 1
            yield local_arr, {pi: GREEN, high: GREEN}

            stack.append((low, pi - 1))
            stack.append((pi + 1, high))
    
    yield local_arr, {} 

def heap_sort(arr, ascending=True):
    local_arr = list(arr)
    n = len(local_arr)

    def heapify(arr_ref, n_ref, i_ref):
        root_idx = i_ref
        left = 2 * i_ref + 1
        right = 2 * i_ref + 2

        highlights = {root_idx: GREEN}
        if left < n_ref: highlights[left] = RED
        if right < n_ref: highlights[right] = RED
        yield arr_ref, highlights

        if ascending:
            if left < n_ref and arr_ref[root_idx] < arr_ref[left]:
                root_idx = left
            if right < n_ref and arr_ref[root_idx] < arr_ref[right]:
                root_idx = right
        else:
            if left < n_ref and arr_ref[root_idx] > arr_ref[left]:
                root_idx = left
            if right < n_ref and arr_ref[root_idx] > arr_ref[right]:
                root_idx = right
        
        if root_idx != i_ref:
            arr_ref[i_ref], arr_ref[root_idx] = arr_ref[root_idx], arr_ref[i_ref]
            yield arr_ref, {i_ref: GREEN, root_idx: GREEN}
            yield from heapify(arr_ref, n_ref, root_idx)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(local_arr, n, i)

    for i in range(n - 1, 0, -1):
        yield local_arr, {i: GREEN, 0: RED} 
        local_arr[i], local_arr[0] = local_arr[0], local_arr[i]
        yield local_arr, {i: GREEN, 0: GREEN}
        yield from heapify(local_arr, i, 0)
    
    yield local_arr, {} 

def _counting_sort_by_digit(a: List[int], exp: int, base: int = 10) -> None:
    n = len(a)
    output = [0] * n
    count = [0] * base

    for i in range(n):
        digit = (a[i] // exp) % base
        count[digit] += 1

    for d in range(1, base):
        count[d] += count[d - 1]

    for i in range(n - 1, -1, -1):
        digit = (a[i] // exp) % base
        pos = count[digit] - 1
        output[pos] = a[i]
        count[digit] -= 1

    for i in range(n):
        a[i] = output[i]

def radix_sort_lsd_nonneg(a: List[int], base: int = 10) -> List[int]:
    if not a:
        return a
    max_val = max(a)
    exp = 1
    while max_val // exp > 0:
        _counting_sort_by_digit(a, exp, base)
        exp *= base
    return a

def radix_sort_lsd(a: List[int], base: int = 10) -> List[int]:
    if not a:
        return a
    neg = [-x for x in a if x < 0]
    pos = [x for x in a if x >= 0]

    if neg:
        radix_sort_lsd_nonneg(neg, base)
    if pos:
        radix_sort_lsd_nonneg(pos, base)
    neg_sorted = [-x for x in reversed(neg)]
    out = neg_sorted + pos
    return out

def radix_sort(arr, ascending=True):

    local_arr = list(arr)
    
    if not local_arr:
        yield local_arr, {}
        return
    
    if any(x < 0 for x in local_arr):
        min_val = min(local_arr)
        offset = -min_val if min_val < 0 else 0
        
        for i in range(len(local_arr)):
            local_arr[i] += offset
            yield local_arr, {i: RED}

        yield from _radix_sort_with_visualization(local_arr, ascending)
        
        for i in range(len(local_arr)):
            local_arr[i] -= offset
            yield local_arr, {i: GREEN}
    else:
        yield from _radix_sort_with_visualization(local_arr, ascending)
    
    yield local_arr, {}

def _radix_sort_with_visualization(local_arr, ascending=True):
    max_val = max(local_arr)
    exp = 1
    
    while max_val // exp > 0:
        yield local_arr, {i: YELLOW for i in range(len(local_arr))}
        
        n = len(local_arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            digit = (local_arr[i] // exp) % 10
            count[digit] += 1
            yield local_arr, {i: RED}

        for d in range(1, 10):
            count[d] += count[d - 1]

        for i in range(n - 1, -1, -1):
            digit = (local_arr[i] // exp) % 10
            pos = count[digit] - 1
            output[pos] = local_arr[i]
            count[digit] -= 1
            yield local_arr, {i: GREEN}
        
        for i in range(n):
            local_arr[i] = output[i]
            yield local_arr, {i: BLUE}
        
        exp *= 10

    if not ascending:
        local_arr.reverse()
        yield local_arr, {i: PURPLE for i in range(len(local_arr))}

def bucket_sort(arr, ascending=True):
    """Bucket Sort with visualization support"""
    local_arr = list(arr)
    n = len(local_arr)
    
    if n == 0:
        yield local_arr, {}
        return

    min_val = min(local_arr)
    max_val = max(local_arr)
    
    if min_val == max_val:
        yield local_arr, {}
        return

    num_buckets = n
    buckets = [[] for _ in range(num_buckets)]

    for i, val in enumerate(local_arr):
        normalized = (val - min_val) / (max_val - min_val)
        bucket_index = min(int(normalized * num_buckets), num_buckets - 1)
        buckets[bucket_index].append(val)
        
        yield local_arr, {i: RED}

    result = []
    for bucket in buckets:
        if bucket:
            bucket.sort()
            result.extend(bucket)
            yield result + local_arr[len(result):], {}
    if not ascending:
        result.reverse()

    for i in range(len(result)):
        local_arr[i] = result[i]
        yield local_arr, {i: GREEN}
    
    yield local_arr, {}

def partition(arr: List[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low
    for j in range(low, high):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    return i


def selection_sort(arr, ascending=True):
    local_arr = list(arr)
    n = len(local_arr)
    
    for i in range(n):
        min_idx = i

        for j in range(i + 1, n):
            yield local_arr, {i: RED, j: RED, min_idx: GREEN}
            
            if (local_arr[j] < local_arr[min_idx] and ascending) or \
               (local_arr[j] > local_arr[min_idx] and not ascending):
                min_idx = j

        if min_idx != i:
            local_arr[i], local_arr[min_idx] = local_arr[min_idx], local_arr[i]
            yield local_arr, {i: GREEN, min_idx: GREEN}
    
    yield local_arr, {}

def counting_sort(arr, ascending=True):
    local_arr = list(arr)
    
    if not local_arr:
        yield local_arr, {}
        return
    
    max_val = max(local_arr)
    min_val = min(local_arr)
    k = max_val - min_val + 1
    count = [0] * k
    
    for i, num in enumerate(local_arr):
        count[num - min_val] += 1
        yield local_arr, {i: RED}

    output = []
    for i, freq in enumerate(count):
        value = i + min_val
        output.extend([value] * freq)
        if len(output) <= len(local_arr):
            for j in range(len(output)):
                if j < len(local_arr):
                    local_arr[j] = output[j]
            yield local_arr, {len(output)-1: GREEN}
    if not ascending:
        output.reverse()

    for i in range(len(output)):
        local_arr[i] = output[i]
        yield local_arr, {i: GREEN}
    
    yield local_arr, {}