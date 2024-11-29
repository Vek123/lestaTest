def merge_sort(arr: list):
    def helper(start: int, end: int):
        if start == end:
            return [arr[start]]
        elif end - start == 1:
            l = arr[start]
            r = arr[end]
            return [l, r] if l < r else [r, l]
        merged_arr = []
        middle = round((start + end) / 2)
        left_half = helper(start, middle)
        right_half = helper(middle+1, end)
        left = len(left_half) - 1
        right = len(right_half) - 1
        while left >= 0 and right >= 0:
            l = left_half[left]
            r = right_half[right]
            if l > r:
                merged_arr.insert(0, l)
                left = left-1
            else:
                merged_arr.insert(0, r)
                right = right-1
        while right >= 0:
            merged_arr.insert(0, right_half[right])
            right -= 1
        while left >= 0:
            merged_arr.insert(0, left_half[left])
            left -= 1
        return merged_arr

    return helper(0, len(arr)-1)


print(merge_sort([5, 1, 2, 5, 6, 8, 1, 3, 7]))
