from rapidfuzz import fuzz
from typing import Dict, Tuple

class SimilarityService:
    
    def calculate_similarity(self, form_data: Dict, extracted_data: Dict) -> Tuple[int, Dict]:
        scores = {}
        
        scores['first_name'] = self._string_similarity(
            form_data.get('first_name', ''),
            extracted_data.get('first_name', '')
        )
        
        scores['last_name'] = self._string_similarity(
            form_data.get('last_name', ''),
            extracted_data.get('last_name', '')
        )
        
        scores['nationality'] = self._nationality_similarity(
            form_data.get('nationality', ''),
            extracted_data.get('nationality', '')
        )
        
        scores['date_of_birth'] = self._string_similarity(
            form_data.get('date_of_birth', ''),
            extracted_data.get('date_of_birth', '')
        )
        
        avg_score = sum(scores.values()) / len(scores) if scores else 0
        final_score = self._map_to_scale(avg_score)
        
        return final_score, scores
    
    def _string_similarity(self, str1: str, str2: str) -> float:
        if not str1 or not str2:
            return 0.0
        return fuzz.ratio(str1.lower(), str2.lower()) / 100.0
    
    def _nationality_similarity(self, nat1: str, nat2: str) -> float:
        if not nat1 or not nat2:
            return 0.0
        
        nat1_lower = nat1.lower()
        nat2_lower = nat2.lower()
        
        if nat1_lower == nat2_lower:
            return 1.0
        
        if nat1_lower in nat2_lower or nat2_lower in nat1_lower:
            return 0.8
        
        return self._string_similarity(nat1, nat2) * 0.7
    
    def _map_to_scale(self, score: float) -> int:
        if score >= 0.9:
            return 5
        elif score >= 0.75:
            return 4
        elif score >= 0.5:
            return 3
        elif score >= 0.25:
            return 2
        else:
            return 1

