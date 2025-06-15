from collections import deque, defaultdict
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

def knuth_morris_pratt(text: str, keywords: list[str]) -> list[dict]:
    if not keywords:
        return []
    results = []
    for keyword in keywords:
        if not keyword:
            continue
            
        border = border_function(keyword)
        j = 0
        count = 0
        
        for i in range(len(text)):
            while j > 0 and text[i] != keyword[j]:
                j = border[j - 1]
            if text[i] == keyword[j]:
                j += 1
            if j == len(keyword):
                count += 1
                j = border[j - 1]
        
        if count == 0:
            continue
        results.append({"keyword": keyword, "occurrences": count})
    
    return results


# --- Boyer-Moore algorithm ---
def get_last_occ(pattern: str) -> dict:
    last_occurrence = {}
    for i, char in enumerate(pattern):
        last_occurrence[char] = i
    return last_occurrence


def boyer_moore(text: str, keywords: list[str]) -> list[dict]:
    if not keywords:
        return []
    
    results = []
    
    for keyword in keywords:
        if not keyword:
            continue
            
        last_occurence = get_last_occ(keyword)
        i = 0
        count = 0
        
        while i <= len(text) - len(keyword):
            j = len(keyword) - 1

            while j >= 0 and text[i + j] == keyword[j]:
                j -= 1
            
            if j < 0:
                count += 1
                i += 1  
            else:
                mismatch_char = text[i + j]
                last = last_occurence.get(mismatch_char, -1)
                i += max(1, j - last)
        
        if count == 0:
            continue

        results.append({"keyword": keyword, "occurrences": count})
    
    return results



def levenshtein_distance(a: str, b: str) -> float:
    """
    Calculate the Levenshtein distance for fuzzy match between two strings. Returns
    the matching percentage as a float between 0 and 100 (%), where 100% means perfect match.
    """

    m, n = len(a), len(b)
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
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,       # delete
                dp[i][j - 1] + 1,       # insert
                dp[i - 1][j - 1] + cost # substitute
            )

    return (1 - dp[m][n] / max(m, n)) * 100

def fuzzy_match(text: str, keywords: list[str], threshold: float = 80.0) -> list[dict]:
    """
    Perform fuzzy matching of keywords in the text using Levenshtein distance.
    Returns a list of dictionaries with keyword and its occurrences.
    """
    if not keywords:
        return []
    
    results = []
    
    for keyword in keywords:
        if not keyword:
            continue
            
        occurrences = 0
        words = text.split()
        
        for word in words:
            match_percentage = levenshtein_distance(word.lower(), keyword.lower())
            if match_percentage >= threshold:
                occurrences += 1
        
        if occurrences > 0:
            results.append({"keyword": keyword, "occurrences": occurrences})
    
    return results


class AhoCorasickNode:
    def __init__(self):
        self.children = {}
        self.failure = None
        self.output = []
        self.is_end = False

class AhoCorasick:
    def __init__(self):
        self.root = AhoCorasickNode()
    
    def build_trie(self, keywords):
        """Build the trie structure from keywords"""
        for keyword in keywords:
            node = self.root
            for char in keyword.lower():  # Case insensitive
                if char not in node.children:
                    node.children[char] = AhoCorasickNode()
                node = node.children[char]
            node.is_end = True
            node.output.append(keyword)
    
    def build_failure_function(self):
        """Build failure function using BFS"""
        queue = deque()
        
        # Initialize failure function for depth 1 nodes
        for child in self.root.children.values():
            child.failure = self.root
            queue.append(child)
        
        # Build failure function for deeper nodes
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                queue.append(child)
                
                # Find failure node
                failure_node = current.failure
                while failure_node is not None and char not in failure_node.children:
                    failure_node = failure_node.failure
                
                if failure_node is not None:
                    child.failure = failure_node.children[char]
                else:
                    child.failure = self.root
                
                # Add output from failure node
                child.output.extend(child.failure.output)
    
    def search(self, text):
        """Search for all occurrences of keywords in text"""
        matches = defaultdict(int)
        node = self.root
        
        for i, char in enumerate(text.lower()):  # Case insensitive
            # Follow failure links until we find a match or reach root
            while node is not None and char not in node.children:
                node = node.failure
            
            if node is None:
                node = self.root
                continue
            
            node = node.children[char]
            
            # Add all matches ending at current position
            for keyword in node.output:
                matches[keyword] += 1
        
        return matches

def aho_corasick(text: str, keywords: list) -> list:
    if not keywords or not text:
        return []
    
    # Filter out empty keywords
    keywords = [k for k in keywords if k.strip()]
    if not keywords:
        return []
    
    # Build Aho-Corasick automaton
    ac = AhoCorasick()
    ac.build_trie(keywords)
    ac.build_failure_function()
    
    # Search for patterns
    matches = ac.search(text)
    
    # Format output
    keywords_data = []
    for keyword in keywords:
        occurrences = matches.get(keyword, 0)
        if occurrences != 0:
            keywords_data.append({
                "keyword": keyword,
                "occurrences": occurrences
            })
    
    return keywords_data

# Example usage  
# text = "I love React and Express. HTML and CSS are great with React."
# keywords = ["React", "Express", "HTML", "CSS", "JavaScript"]

# result = aho_corasick(text, keywords)
# print(result)
# Output:
# [
#     {"keyword": "React", "occurrences": 2},
#     {"keyword": "Express", "occurrences": 1}, 
#     {"keyword": "HTML", "occurrences": 1},
#     {"keyword": "CSS", "occurrences": 1},
#     {"keyword": "JavaScript", "occurrences": 0}
# ]