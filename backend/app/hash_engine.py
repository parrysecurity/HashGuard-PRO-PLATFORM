import re
import base64
import math
from typing import List, Dict, Any

class HashInfo:
    def __init__(self, name, pattern, length, bit_length, common_uses, tools, security_rating):
        self.name = name
        self.pattern = pattern
        self.length = length
        self.bit_length = bit_length
        self.common_uses = common_uses
        self.tools = tools
        self.security_rating = security_rating

class HashIdentifier:
    def __init__(self):
        self.hash_types = self._initialize_hash_types()
    
    def _initialize_hash_types(self):
        return {
            'MD5': HashInfo(
                'MD5', r'^[a-fA-F0-9]{32}$', 32, 128,
                ['File integrity checks', 'Password hashing (legacy)'],
                {'hashcat': 0, 'john': 'raw-md5', 'rainbow_tables': True},
                'CRITICAL - Broken'
            ),
            'SHA1': HashInfo(
                'SHA1', r'^[a-fA-F0-9]{40}$', 40, 160,
                ['Git commits', 'SSL certificates (legacy)'],
                {'hashcat': 100, 'john': 'raw-sha1', 'rainbow_tables': True},
                'CRITICAL - Collision attacks possible'
            ),
            'SHA224': HashInfo(
                'SHA224', r'^[a-fA-F0-9]{56}$', 56, 224,
                ['Digital signatures', 'Hash-based message authentication'],
                {'hashcat': 1300, 'john': 'raw-sha224', 'rainbow_tables': False},
                'SECURE'
            ),
            'SHA256': HashInfo(
                'SHA256', r'^[a-fA-F0-9]{64}$', 64, 256,
                ['Blockchain', 'Digital signatures', 'Password hashing'],
                {'hashcat': 1400, 'john': 'raw-sha256', 'rainbow_tables': False},
                'SECURE - Recommended'
            ),
            'SHA384': HashInfo(
                'SHA384', r'^[a-fA-F0-9]{96}$', 96, 384,
                ['High security applications', 'TLS certificates'],
                {'hashcat': 10800, 'john': 'raw-sha384', 'rainbow_tables': False},
                'SECURE - Recommended'
            ),
            'SHA512': HashInfo(
                'SHA512', r'^[a-fA-F0-9]{128}$', 128, 512,
                ['High security applications', 'Digital certificates'],
                {'hashcat': 1700, 'john': 'raw-sha512', 'rainbow_tables': False},
                'SECURE - Recommended'
            ),
            'NTLM': HashInfo(
                'NTLM', r'^[a-fA-F0-9]{32}$', 32, 128,
                ['Windows password hashing'],
                {'hashcat': 1000, 'john': 'nt', 'rainbow_tables': True},
                'WEAK - Use stronger hash'
            ),
            'bcrypt': HashInfo(
                'bcrypt', r'^\$2[aby]\$\d+\$[./A-Za-z0-9]{53}$', 60, 184,
                ['Password storage', 'Web applications'],
                {'hashcat': 3200, 'john': 'bcrypt', 'rainbow_tables': False},
                'SECURE - Recommended for passwords'
            ),
            'Argon2': HashInfo(
                'Argon2', r'^\$argon2(id|d|i)\$v=\d+\$m=\d+,t=\d+,p=\d+\$[A-Za-z0-9+/]+$', 0, 0,
                ['Modern password hashing', 'Cryptocurrency'],
                {'hashcat': 0, 'john': 'argon2', 'rainbow_tables': False},
                'SECURE - Best choice'
            ),
            'Whirlpool': HashInfo(
                'Whirlpool', r'^[a-fA-F0-9]{128}$', 128, 512,
                ['Legacy systems', 'File integrity'],
                {'hashcat': 6100, 'john': 'whirlpool', 'rainbow_tables': False},
                'SECURE'
            ),
            'CRC32': HashInfo(
                'CRC32', r'^[a-fA-F0-9]{8}$', 8, 32,
                ['Checksums', 'Error detection'],
                {'hashcat': 11500, 'john': 'crc32', 'rainbow_tables': True},
                'NOT FOR SECURITY - Checksum only'
            ),
            'MySQL': HashInfo(
                'MySQL', r'^[a-fA-F0-9]{16}$', 16, 64,
                ['MySQL password hashing (old)'],
                {'hashcat': 200, 'john': 'mysql', 'rainbow_tables': True},
                'WEAK'
            ),
        }
    
    def identify_hash(self, hash_string: str) -> List[Dict[str, Any]]:
        results = []
        hash_string = hash_string.strip()
        
        for hash_name, hash_info in self.hash_types.items():
            if re.match(hash_info.pattern, hash_string, re.IGNORECASE):
                confidence = self._calculate_confidence(hash_string, hash_info)
                results.append({
                    'type': hash_name,
                    'confidence': confidence,
                    'bit_length': hash_info.bit_length,
                    'length': len(hash_string),
                    'common_uses': hash_info.common_uses,
                    'tools': hash_info.tools,
                    'security_rating': hash_info.security_rating
                })
        
        # Check for encoded hashes
        encoded_matches = self._check_encoded_hashes(hash_string)
        results.extend(encoded_matches)
        
        # Sort by confidence
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results
    
    def _calculate_confidence(self, hash_string: str, hash_info: HashInfo) -> float:
        confidence = 90.0
        
        # Check character distribution
        unique_chars = len(set(hash_string))
        if unique_chars / len(hash_string) > 0.8:
            confidence += 5
        
        # Check entropy
        entropy = self._calculate_entropy(hash_string)
        if entropy > 3.0:
            confidence += 5
        
        return min(confidence, 100.0)
    
    def _calculate_entropy(self, s: str) -> float:
        freq = {}
        for c in s:
            freq[c] = freq.get(c, 0) + 1
        
        entropy = 0
        length = len(s)
        for count in freq.values():
            prob = count / length
            entropy -= prob * math.log2(prob)
        return entropy
    
    def _check_encoded_hashes(self, hash_string: str) -> List[Dict[str, Any]]:
        results = []
        
        # Check Base64
        try:
            decoded = base64.b64decode(hash_string)
            decoded_str = decoded.hex()
            for hash_name, hash_info in self.hash_types.items():
                if re.match(hash_info.pattern, decoded_str, re.IGNORECASE):
                    results.append({
                        'type': f'Base64 > {hash_name}',
                        'confidence': 75.0,
                        'bit_length': hash_info.bit_length * 2,
                        'encoding': 'Base64',
                        'decoded_value': decoded_str
                    })
        except:
            pass
        
        return results

class BulkHashAnalyzer:
    def __init__(self, hash_identifier):
        self.hash_identifier = hash_identifier
    
    def analyze_bulk(self, hashes: List[str]) -> Dict[str, Any]:
        results = {
            'total': len(hashes),
            'valid': 0,
            'invalid': 0,
            'duplicates': 0,
            'by_type': {},
            'results': []
        }
        
        unique_hashes = list(dict.fromkeys(hashes))
        results['duplicates'] = len(hashes) - len(unique_hashes)
        
        for hash_string in unique_hashes:
            hash_string = hash_string.strip()
            if not hash_string:
                continue
            
            identifications = self.hash_identifier.identify_hash(hash_string)
            if identifications:
                results['valid'] += 1
                hash_type = identifications[0]['type']
                results['by_type'][hash_type] = results['by_type'].get(hash_type, 0) + 1
                results['results'].append({
                    'hash': hash_string,
                    'identifications': identifications
                })
            else:
                results['invalid'] += 1
        
        return results
