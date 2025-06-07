# --- algorithms for searching and matching patterns in text ---

# --- Knuth-Morris-Pratt (KMP) algorithm ---
def border_function(pattern: str) -> list:
    n = len(pattern)
    boders = [0] * n

    for i in range(1, n):
        j = boders[i - 1]
        while j > 0 and pattern[i] != pattern[j]:
            j = boders[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        boders[i] = j
    return boders

def knuth_morris_pratt(text: str, pattern: str) -> bool:
    if not pattern:
        return True

    border = border_function(pattern)

    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = border[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            return True
    return False


# --- Boyer-Moore algorithm ---
def get_last_occ(pattern: str) -> dict:
    last_occurrence = {}
    for i, char in enumerate(pattern):
        last_occurrence[char] = i
    return last_occurrence

def boyer_moore(text: str, pattern: str) -> bool:
    last_occurence = get_last_occ(pattern)

    i = 0
    
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        
        if j < 0:
            return True
        
        mismatch_char = text[i + j]
        last = last_occurence.get(mismatch_char, -1)
        i += max(1, j - last)

    return False



def levenshtein_distance(pattern: str, text: str) -> float:
    """
    Calculate the Levenshtein distance for fuzzy match between two strings. Returns
    the matching percentage as a float between 0 and 100 (%), where 100% means perfect match.
    """

    m, n = len(pattern), len(text)
    if m == 0:
        return 100.0 if n == 0 else 0.0

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # base case
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # DP computation
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if pattern[i - 1] == text[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,       # delete
                dp[i][j - 1] + 1,       # insert
                dp[i - 1][j - 1] + cost # substitute
            )

    return (1 - dp[m][n] / max(m, n)) * 100