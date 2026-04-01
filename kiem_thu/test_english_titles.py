import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ung_dung.xu_ly_ai.xu_ly_noi_dung import tao_tieu_de_doan

def test_titles():
    test_cases = [
        {
            "name": "Definition Heuristic",
            "text": "Artificial Intelligence is defined as the simulation of human intelligence processes by machines.",
            "expected_keywords": ["Concept", "Definition"]
        },
        {
            "name": "Application Heuristic",
            "text": "Python is widely used for data analysis, machine learning, and web development.",
            "expected_keywords": ["Applications", "Usage"]
        },
        {
            "name": "History Heuristic",
            "text": "The history of the internet began with the development of electronic computers in the 1950s.",
            "expected_keywords": ["Historical", "Background"]
        },
        {
            "name": "Smart Template (Keyword: Machine Learning)",
            "text": "Machine Learning algorithms build a model based on sample data, known as training data. Machine Learning is a subset of AI.",
            "expected_keywords": ["Machine Learning", "Understanding", "Overview", "Role", "Aspects"]
        },
        {
            "name": "Smart Template (Keyword: Neural Networks)",
            "text": "Neural networks are computing systems inspired by the biological neural networks. These networks learn tasks by considering examples.",
            "expected_keywords": ["Neural Networks"]
        }
    ]

    print("\n=== TESTING ENGLISH SMART TITLES ===\n")
    
    for case in test_cases:
        print(f"Testing: {case['name']}")
        print(f"Input: {case['text'][:60]}...")
        title = tao_tieu_de_doan(case['text'])
        print(f"Generated Title: {title}")
        
        # Simple verification
        if any(k in title for k in case['expected_keywords']):
            print("✅ PASSED")
        else:
            print(f"❌ FAILED (Expected one of {case['expected_keywords']})")
        print("-" * 50)

if __name__ == "__main__":
    test_titles()
